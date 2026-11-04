#!/usr/bin/env bash
# Measure MERGE pruning: stock dbt (arm A) vs the override that merges on dbt_valid_from (arm B).
# The target has $KEYS keys with 1 to 10 versions each, loaded in dbt_valid_from order.
# SCENARIO=spread changes about 1,000 keys picked by hash, so their current rows sit anywhere in history.
# SCENARIO=recent changes the 1,000 keys whose current row is newest.
# Each arm merges into its own copy of the same target.
# Usage: integration_tests/snapshot_merge_valid_from/run_perf.sh
set -euo pipefail
cd "$(dirname "$0")"

DB=DFLIPPO_DEV
SCH=SNAPSHOT_MERGE_TEST
CONN=${SNOW_CONNECTION:-ps_snowsecure_keypair}
WH=${PERF_WAREHOUSE:-DFLIPPO_WH}
DBT=${DBT:-dbt}
KEYS=${KEYS:-10000000}
SCENARIO=${SCENARIO:-spread}
if [ "$SCENARIO" = recent ]; then
  CHANGED="id in (select id from $DB.$SCH.BIG_SRC order by updated_at desc limit 1000)"
else
  CHANGED="mod(hash(id), $((KEYS / 1000))) = 0"
fi

sql() { snow sql -c "$CONN" --role DFLIPPO_ROLE --warehouse "$WH" --format json -q "$1"; }

echo "Build the history table and the source"
sql "create schema if not exists $DB.$SCH;
     create schema if not exists $DB.${SCH}_A;
     create schema if not exists $DB.${SCH}_B;
     create or replace table $DB.$SCH.BIG_HIST as
     with keys as (select seq4() + 1 as id from table(generator(rowcount => $KEYS))),
     versions as (
       select k.id, v.n, 1 + mod(k.id, 10) as n_versions
       from keys k join (select seq4() as n from table(generator(rowcount => 10))) v
         on v.n < 1 + mod(k.id, 10)),
     dated as (
       select id, n, n_versions,
              dateadd(minute, mod(id * 7919, 525600) + n * 525600 / n_versions,
                      '2020-01-01'::timestamp_ntz) as vfrom
       from versions)
     select id, 'g' as grp, 'name_' || id || '_' || n as name, n::number(10,2) as amt,
            vfrom as updated_at,
            md5(coalesce(cast(id as varchar), '') || '|' || coalesce(cast(vfrom as varchar), '')) as dbt_scd_id,
            vfrom as dbt_updated_at, vfrom as dbt_valid_from,
            lead(vfrom) over (partition by id order by n) as dbt_valid_to
     from dated
     order by vfrom;
     create or replace table $DB.$SCH.BIG_SRC as
       select id, grp, name, amt, updated_at from $DB.$SCH.BIG_HIST where dbt_valid_to is null;
     update $DB.$SCH.BIG_SRC set name = name || '_chg', updated_at = '2026-06-01'
       where $CHANGED;
     create or replace table $DB.${SCH}_A.SNAP_BIG clone $DB.$SCH.BIG_HIST;
     create or replace table $DB.${SCH}_B.SNAP_BIG clone $DB.$SCH.BIG_HIST;" >/dev/null

sql "select count(*) as hist_rows, count(distinct id) as keys from $DB.$SCH.BIG_HIST"

# Make the two project copies: A = stock dbt, B = the upstream proposal macro. Remove them on exit.
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
for arm in A B; do
  mkdir -p "$WORK/$arm/macros"
  cp -R dbt_project.yml snapshots "$WORK/$arm"/
  cp macros/generate_schema_name.sql "$WORK/$arm/macros/"
done
cp ../../macros/snowflake_snapshot_merge_valid_from.sql.proposal "$WORK/B/macros/snapshot_override.sql"

for arm in A B; do
  echo "Arm $arm"
  $DBT snapshot --target test --project-dir "$WORK/$arm" --select snap_big --quiet \
    --vars "{arm: $arm, perf: true}"
done

echo "MERGE scan statistics"
for arm in A B; do
  qid=$(sql "select query_id from table($DB.information_schema.query_history_by_user(result_limit => 1000))
             where query_type = 'MERGE' and query_text ilike '%${SCH}_${arm}%SNAP_BIG%'
               and start_time > dateadd(minute, -30, current_timestamp())
             order by start_time desc limit 1" | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['QUERY_ID'])")
  sql "select '$arm' as arm, '$qid' as query_id,
          max(execution_time_breakdown:overall_percentage) as pct,
          sum(operator_statistics:pruning:partitions_scanned) as partitions_scanned,
          sum(operator_statistics:pruning:partitions_total) as partitions_total,
          sum(operator_statistics:io:bytes_scanned) as bytes_scanned,
          (select total_elapsed_time from table($DB.information_schema.query_history_by_user(result_limit => 1000))
            where query_id = '$qid') as elapsed_ms
       from table(get_query_operator_stats('$qid'))
       where operator_type = 'TableScan' and operator_attributes:table_name::string ilike '%${SCH}_${arm}%SNAP_BIG'"
done

echo "Check that both arms hold the same rows after the merge"
sql "select (select count(*) from (
           select * exclude (dbt_updated_at, dbt_valid_to) from $DB.${SCH}_A.SNAP_BIG
           minus select * exclude (dbt_updated_at, dbt_valid_to) from $DB.${SCH}_B.SNAP_BIG)) as only_a,
        (select count(*) from $DB.${SCH}_A.SNAP_BIG where dbt_valid_to is null) as current_a,
        (select count(*) from $DB.${SCH}_B.SNAP_BIG where dbt_valid_to is null) as current_b"
