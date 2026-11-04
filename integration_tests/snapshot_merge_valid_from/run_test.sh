#!/usr/bin/env bash
# Test a snapshot macro set against stock dbt.
#   MACROS=proposal      macros/snowflake_snapshot_merge_valid_from.sql.proposal (upstream proposal, default)
#   MACROS=improvements  macros/snowflake_snapshot_improvements.sql (adds the surrogate key)
# Arm A runs stock dbt. Arm B runs the selected macros. Each arm runs from a temporary copy
# of this project. Both arms snapshot the same source after each change, then the script compares them.
# Requires: dbt (Core or Fusion) with target "test" (ps_snowsecure), and the Snowflake CLI.
# Set SNOW_CONNECTION to use a different connections.toml entry for the same account.
# Usage: MACROS=improvements integration_tests/snapshot_merge_valid_from/run_test.sh
set -euo pipefail
cd "$(dirname "$0")"

DB=DFLIPPO_DEV
SCH=SNAPSHOT_MERGE_TEST
CONN=${SNOW_CONNECTION:-ps_snowsecure_keypair}
# Set DBT to run another dbt engine, for example: DBT="uvx --from dbt-snowflake dbt"
DBT=${DBT:-dbt}
MACROS=${MACROS:-proposal}

sql() { snow sql -c "$CONN" --role DFLIPPO_ROLE --warehouse DFLIPPO_WH --format json -q "$1"; }

# Make the two project copies. Remove them on exit.
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
for arm in A B; do
  mkdir -p "$WORK/$arm/macros"
  cp -R dbt_project.yml snapshots "$WORK/$arm"/
  cp macros/generate_schema_name.sql "$WORK/$arm/macros/"
done
case "$MACROS" in
  proposal)
    cp ../../macros/snowflake_snapshot_merge_valid_from.sql.proposal "$WORK/B/macros/snapshot_override.sql"
    SURROGATE=false ;;
  improvements)
    cp ../../macros/snowflake_snapshot_improvements.sql ../../macros/sequence_nextval_as_surrogate_key.sql "$WORK/B/macros/"
    SURROGATE=true ;;
  *) echo "Unknown MACROS=$MACROS"; exit 2 ;;
esac

snap_both() {
  for arm in A B; do
    $DBT snapshot --target test --project-dir "$WORK/$arm" --quiet \
      --vars "{arm: $arm, surrogate: $SURROGATE}"
  done
}

echo "Step 0: reset the test schemas and load the source"
sql "create or replace schema $DB.$SCH;
     drop schema if exists $DB.${SCH}_A; drop schema if exists $DB.${SCH}_B;
     create table $DB.$SCH.SRC (id int, grp varchar, name varchar, amt number(10,2), updated_at timestamp_ntz);
     insert into $DB.$SCH.SRC values
       (1,'x','alpha',10,'2026-01-01'), (2,'x','beta',20,'2026-01-01'),
       (3,'y','gamma',30,'2026-01-01'), (4,'y','delta',40,'2026-01-01'),
       (6,'y','zeta',60,null);" >/dev/null
snap_both

echo "Step 1: update 1, delete 2, delete 6 (null updated_at, so null dbt_valid_from), insert 5"
sql "update $DB.$SCH.SRC set name='alpha2', updated_at='2026-02-01' where id=1;
     delete from $DB.$SCH.SRC where id in (2, 6);
     insert into $DB.$SCH.SRC values (5,'y','epsilon',50,'2026-02-01');" >/dev/null
snap_both

echo "Step 2: update 1 again, put 2 back, change amt on 3 only"
sql "update $DB.$SCH.SRC set amt=11, updated_at='2026-03-01' where id=1;
     insert into $DB.$SCH.SRC values (2,'x','beta',20,'2026-03-01');
     update $DB.$SCH.SRC set amt=31 where id=3;" >/dev/null
snap_both

echo "Step 3: run again with no source change"
snap_both

echo "Compare arm A and arm B"
fail=0
tables="SNAP_TS_IGNORE SNAP_CHECK_INVALIDATE SNAP_TS_NEW_RECORD SNAP_TS_VALID_TO_CURRENT
        SNAP_CHECK_COMPOSITE_KEY SNAP_TS_RENAMED_COLS"
[ "$SURROGATE" = true ] && tables="$tables SNAP_SK_CHECK_INVALIDATE SNAP_SK_TS_NEW_RECORD"
for t in $tables; do
  if [ "$t" = SNAP_TS_RENAMED_COLS ]; then
    meta="scd_id, row_updated_at, valid_from, valid_to"; vto=valid_to
  else
    meta="dbt_scd_id, dbt_updated_at, dbt_valid_from, dbt_valid_to"; vto=dbt_valid_to
  fi
  # Stock dbt ignores the surrogate key, so only arm B has the SK column.
  meta_b=$meta; case $t in SNAP_SK_*) meta_b="$meta, sk" ;; esac
  # Run-time columns differ between arms, so compare the business columns and the row state.
  q="select * exclude (META),
            iff($vto is null or $vto = '9999-12-31', 'current', 'closed') as row_state
     from $DB.${SCH}_ARM.$t"
  qa=${q//ARM/A}; qa=${qa//META/$meta}
  qb=${q//ARM/B}; qb=${qb//META/$meta_b}
  res=$(sql "select
      (select count(*) from $DB.${SCH}_A.$t) as rows_a,
      (select count(*) from $DB.${SCH}_B.$t) as rows_b,
      (select count(*) from ($qa minus $qb)) as only_a,
      (select count(*) from ($qb minus $qa)) as only_b,
      (select count(*) - count(distinct id, grp) from $DB.${SCH}_B.$t
         where $vto is null or $vto = '9999-12-31') as dup_current_b")
  echo "$t $res"
  echo "$res" | grep -q '"ONLY_A": 0' && echo "$res" | grep -q '"ONLY_B": 0' \
    && echo "$res" | grep -q '"DUP_CURRENT_B": 0' || fail=1
  case $t in SNAP_SK_*)
    # Every row has its own key, and closing a row must not change its key.
    res=$(sql "select count(*) - count(sk) as null_sk, count(*) - count(distinct sk) as dup_sk
               from $DB.${SCH}_B.$t")
    echo "$t surrogate key $res"
    echo "$res" | grep -q '"NULL_SK": 0' && echo "$res" | grep -q '"DUP_SK": 0' || fail=1 ;;
  esac
done

echo "Check that arm B ran the new join"
res=$(sql "select count(*) as merges_b from table($DB.information_schema.query_history_by_user(result_limit => 1000))
  where query_type = 'MERGE' and query_text ilike '%${SCH}_B%'
    and query_text ilike '%DBT_INTERNAL_SOURCE.dbt_valid_from is not distinct from DBT_INTERNAL_DEST.dbt_valid_from%'
    and start_time > dateadd(hour, -1, current_timestamp())")
echo "$res"
echo "$res" | grep -q '"MERGES_B": 0' && fail=1

[ "$fail" = 0 ] && echo "PASS" || { echo "FAIL"; exit 1; }
