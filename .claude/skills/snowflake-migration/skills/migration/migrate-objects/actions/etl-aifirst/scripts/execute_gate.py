#!/usr/bin/env python3
"""STAGE 6 -- run the generated dbt project against a real Snowflake account.

WHY THIS EXISTS. Every previous run of this pipeline reported `SQL UNVERIFIED -- 0 of 4
models`, and the cause was not laziness: the engine emits a dbt project that is a TEMPLATE,
not a runnable artifact. `profiles.yml` ships `role: ROLE`, `account: ACCOUNT`,
`database: DATABASE`; `dbt_project.yml` ships `name: YOUR_PROJECT_NAME`. So dbt reached the
warehouse, failed to authenticate against the literal string "ACCOUNT", and never analysed a
line of SQL. Nothing in this project has ever executed.

WHAT THIS STAGE CLAIMS, AND WHAT IT DOES NOT. It claims the generated SQL *runs* -- that
Snowflake parses it, that the relations resolve, that the DAG builds in dependency order. It
does NOT claim the SQL is *correct*: no rows are compared against a source system, which is
out of scope by owner decision. A tree that runs is not a tree that is right.

WHAT THE HARNESS SUPPLIES vs WHAT THE MIGRATION PRODUCED -- state this plainly, because the
distinction is the difference between a real result and a rigged one:

  SUPPLIED BY THIS HARNESS (deployment binding, which the artifact deliberately leaves open)
    - a real profiles.yml (account, user, role, warehouse, database, schema)
    - dbt_project.yml `name` and `profile`, which ship as YOUR_PROJECT_NAME
    - the source schema binding: sources.yml deliberately omits database/schema, and its own
      header says naming one "would assert a destination the migration has not chosen"
    - the source TABLE and three rows of synthetic data

  PRODUCED BY THE MIGRATION, AND EXECUTED UNMODIFIED
    - every .sql file under models/ and macros/. NOT ONE BYTE IS EDITED. The stage asserts
      this by hashing the model tree before and after staging and refusing to proceed if a
      single model differs.

THE MATERIALISATION COUNT, because an inflated one would be the easiest lie to tell here.
`dbt_project.yml` sets intermediate/+materialized: ephemeral, so the two int_ models are
inlined as CTEs and never become relations. Four models compile; TWO materialise (a staging
view and an incremental mart). This stage reports both numbers. "4/4 executed" would be
false and is exactly the shape of claim four earlier gates in this project made before being
found incapable of failing.

THE NULL ROW IS THE POINT. One seeded row carries MiddleName = NULL. The emitted expression
is `FirstName || ' ' || MiddleName || ' ' || LastName`, and Snowflake's `||` propagates NULL,
so that row's FullName must come back NULL. DataStage's `:` operator also propagates, so this
is FAITHFUL -- and it is the first time this project observes a concatenation-NULL outcome in
DATA rather than reasoning about it from a dialect sheet. If that row comes back non-NULL,
something rewrote the expression and the stage says so.

Usage:
    execute_gate.py <output-tree> --connection <name> [--keep] [--break-model <name>]

    --keep         do not drop the scratch schema (for debugging a failure)
    --break-model  corrupt one model's SQL before running. THE NEGATIVE TEST: the stage must
                   report failure and exit non-zero. A gate never seen to fail is not a gate.

Exit codes:
    0  the project executed and every assertion held
    1  it ran and something failed -- a finding
    2  it could not run at all -- UNMEASURED, which is neither a pass nor a fail
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

MODEL_EXT = (".sql", ".yml")

# THE NEGATIVE TEST's actual corruption string. A test that reimplements this append
# instead of calling corrupt_model() can drift from what the stage really does; pin it here
# so both the stage and its regression test read the same marker.
BREAK_MODEL_MARKER = "THIS IS NOT SQL AND MUST FAIL"

# dbt never sees this password on disk: profiles.yml references it via env_var() instead
# of embedding it, so a leftover staged project (e.g. --keep) does not carry a live secret.
PROFILE_PASSWORD_ENV = "AIFIRST_EXECUTE_GATE_PASSWORD"

_SAFE_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def sh(cmd, cwd=None, timeout=900):
    """Run a command, returning (rc, stdout+stderr). Never raises on non-zero."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds: %s" % (timeout, " ".join(cmd))
    except FileNotFoundError as e:
        return 127, "command not found: %s" % e


def snow_sql(conn, sql, timeout=300):
    return sh(["snow", "sql", "-c", conn, "-q", sql, "--format", "json"], timeout=timeout)


def snow_connection(name):
    """The named connection's settings, read from the `snow` CLI's own connections.toml.

    Reading the CLI's config rather than requiring exported env vars keeps the credential
    in exactly one place and means the profile references the key FILE by path -- no secret
    is ever written into a generated profile or into this repo.
    """
    import tomllib
    for cand in ("~/.snowflake/connections.toml", "~/.snowflake/config.toml"):
        p = os.path.expanduser(cand)
        if not os.path.exists(p):
            continue
        with open(p, "rb") as fh:
            data = tomllib.load(fh)
        if name in data:
            return data[name]
        conns = data.get("connections", {})
        if name in conns:
            return conns[name]
    return None


def find_project(tree):
    """The dbt project is the directory holding dbt_project.yml."""
    for root, _dirs, files in os.walk(tree):
        if "dbt_project.yml" in files and os.path.isdir(os.path.join(root, "models")):
            return root
    return None


def validate_identifier(name, what="identifier"):
    """Reject anything that is not a plain identifier before it reaches DDL/DML.

    `tbl`/`src_name` come from parsing source('a','b') out of the migration's OWN generated
    SQL, not from a human typing a table name -- so this is the last checkpoint before a
    string neither of us wrote is spliced, quoted, into a query.
    """
    if not name or not _SAFE_IDENTIFIER.match(name):
        raise ValueError("unsafe %s: %r" % (what, name))
    return name


def sql_literal(value):
    """A single-quoted SQL string literal, with embedded quotes doubled.

    SEED_ROWS is a hardcoded module constant today, so nothing here is attacker-reachable
    yet -- but building the INSERT's VALUES list by bare `'%s' % value` interpolation (as
    this used to) reopens exactly the injection shape CWE-89 flags the moment that constant
    stops being hardcoded. Doubling embedded quotes is the standard SQL escape and costs
    nothing while the values are still trusted.
    """
    return "'%s'" % str(value).replace("'", "''")


def find_model_file(proj, break_model):
    """Locate the model file --break-model names, under proj/models."""
    hit = None
    for root, _d, files in os.walk(os.path.join(proj, "models")):
        for f in files:
            if f.endswith(".sql") and break_model in f:
                hit = os.path.join(root, f)
    return hit


def corrupt_model(path):
    """THE NEGATIVE TEST's actual corruption: append text no SQL parser accepts."""
    with open(path, "a") as fh:
        fh.write("\n%s\n" % BREAK_MODEL_MARKER)


def dbt_verdict(rc, out):
    """(success count, error-line count, overall ok) from dbt's own per-model verdicts.

    Counts the runner's per-model lines rather than pattern-matching a summary sentence --
    see the SUCCESS DETECTION note below for why that distinction mattered in practice.
    """
    succ = len(re.findall(r"^\s*Success\s+models/", out, re.M))
    errs = len(re.findall(r"^\s*(?:Error|Failure|Failed)\b", out, re.M))
    ok = rc == 0 and succ > 0 and errs == 0
    return succ, errs, ok


def write_profiles_yml(proj, prof, role, warehouse, database, schema):
    """Write profiles.yml for the staged project; return the secret to export via
    PROFILE_PASSWORD_ENV, or None if auth is by key file (no secret to protect).

    A private key is referenced by path (never copied). A password would otherwise be
    written to disk in plaintext, so it goes out as a dbt env_var() reference instead --
    the caller is responsible for setting PROFILE_PASSWORD_ENV in the dbt subprocess's
    environment. The file is chmod 0600 either way, so a leftover --keep tree never leaves
    a profile group/other-readable.
    """
    auth = ""
    secret = None
    if prof.get("private_key_file"):
        auth = "      private_key_path: %s\n" % prof["private_key_file"]
    elif prof.get("password"):
        secret = prof["password"]
        auth = "      password: \"{{ env_var('%s') }}\"\n" % PROFILE_PASSWORD_ENV
    else:
        raise ValueError("connection has neither private_key_file nor password")
    path = os.path.join(proj, "profiles.yml")
    with open(path, "w") as fh:
        fh.write(
            "aifirst_mvp:\n  target: dev\n  outputs:\n    dev:\n"
            "      type: snowflake\n"
            "      account: %s\n      user: %s\n%s"
            "      role: %s\n      warehouse: %s\n      database: %s\n"
            "      schema: %s\n      threads: 1\n"
            % (prof.get("account", ""), prof.get("user", ""), auth,
               role, warehouse, database, schema))
    os.chmod(path, 0o600)
    return secret


def hash_models(project):
    """Fingerprint every model/macro file. Guards the no-byte-edited claim above."""
    out = {}
    for sub in ("models", "macros"):
        d = os.path.join(project, sub)
        if not os.path.isdir(d):
            continue
        for root, _dirs, files in os.walk(d):
            for f in sorted(files):
                if f.endswith(MODEL_EXT):
                    p = os.path.join(root, f)
                    rel = os.path.relpath(p, project)
                    with open(p, "rb") as fh:
                        out[rel] = hashlib.sha256(fh.read()).hexdigest()
    return out


def model_inventory(project):
    """(all models, ephemeral ones) read off dbt_project.yml's materialisation config.

    Deliberately NOT a file count. `intermediate: +materialized: ephemeral` means those
    models never become relations, so a file count would overstate what executed.
    """
    cfg = ""
    with open(os.path.join(project, "dbt_project.yml")) as fh:
        cfg = fh.read()
    ephemeral_dirs = set()
    cur = None
    for line in cfg.split("\n"):
        m = re.match(r"^\s{4}(\w+):\s*$", line)
        if m:
            cur = m.group(1)
        if "+materialized:" in line and "ephemeral" in line and cur:
            ephemeral_dirs.add(cur)
    models, ephemeral = [], []
    mroot = os.path.join(project, "models")
    for root, _dirs, files in os.walk(mroot):
        for f in sorted(files):
            if not f.endswith(".sql"):
                continue
            rel = os.path.relpath(os.path.join(root, f), mroot)
            models.append(rel)
            if rel.split(os.sep)[0] in ephemeral_dirs:
                ephemeral.append(rel)
    return models, ephemeral


def source_refs(project):
    """Every source('a','b') the models actually reference."""
    found = set()
    mroot = os.path.join(project, "models")
    for root, _dirs, files in os.walk(mroot):
        for f in files:
            if f.endswith(".sql"):
                with open(os.path.join(root, f)) as fh:
                    for m in re.finditer(r"source\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\)",
                                         fh.read()):
                        found.add((m.group(1), m.group(2)))
    return sorted(found)


# ==================================================================================================
# THE SEED SHAPE IS DERIVED FROM THE MODELS, NOT DECLARED HERE.
#
# It used to be declared: every source relation was created as
# `(FirstName STRING, MiddleName STRING, LastName STRING, BirthDate DATE)`, the LoadDim person
# fixture. On any other workload that table has none of the columns the models select, so the run
# could never have succeeded -- and because the CREATE used QUOTED lowercase identifiers while a dbt
# `source()` resolves UNQUOTED to uppercase, the models did not even find the table to fail against.
# MEASURED (m1-ready re-run, 2026-08-19): three models errored with
# `Object '...CORP_FILESHARE_ETL_SALES_CUSTOMERS_CSV' does not exist` on the same relations the line
# above reported as seeded. Two defects, one visible symptom, and the execute bar was unmeasurable on
# every platform whose fixture is not LoadDim.
#
# So: columns come from the staging model that reads each source, and identifiers are written
# UNQUOTED so they normalise exactly the way `source()` does.
# ==================================================================================================

_SQL_WORDS = frozenset({
    "select", "from", "where", "as", "and", "or", "not", "null", "case", "when", "then", "else",
    "end", "distinct", "cast", "on", "join", "left", "right", "inner", "outer", "group", "order",
    "by", "having", "union", "all", "with", "is", "in", "like", "between", "true", "false",
})
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_DATEISH = re.compile(r"(date|datetime|timestamp|_dt)$", re.I)
_NUMISH = re.compile(r"(amount|amt|pct|percent|price|qty|quantity|count|number|num|revenue|total|"
                     r"days|tenure|id)$", re.I)

# The one shape whose VALUES encode designed experiments (a NULL middle name for NULL propagation,
# a birthdate below the filter's 1990 threshold). When a tree really does select these columns the
# original rows are used verbatim, so the LoadDim measurement is unchanged by this derivation.
_PERSON_SHAPE = ("firstname", "middlename", "lastname", "birthdate")


def _split_top(sql):
    """Split a SELECT list on commas that are not inside parentheses."""
    out, depth, cur = [], 0, []
    for ch in sql:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        out.append("".join(cur))
    return out


def derive_columns(project, src_name, tbl):
    """The columns a source relation must have, read off the model that selects from it.

    Returns [] when no model references the source or the statement is not in a shape this can
    read -- the caller REFUSES to seed rather than inventing a shape, because a guessed shape is
    how the declared fixture came to stand in for every platform.
    """
    call = re.compile(r"source\(\s*'%s'\s*,\s*'%s'\s*\)" % (re.escape(src_name), re.escape(tbl)))
    mroot = os.path.join(project, "models")
    for root, _dirs, files in os.walk(mroot):
        for f in sorted(files):
            if not f.endswith(".sql"):
                continue
            text = open(os.path.join(root, f)).read()
            m = call.search(text)
            if not m:
                continue
            head = text[:m.start()]
            fr = head.lower().rfind("from")
            if fr < 0:
                continue
            sel = head.lower().rfind("select", 0, fr)
            if sel < 0:
                continue
            body = head[sel + len("select"):fr]
            cols, seen = [], set()
            for entry in _split_top(body):
                entry = entry.strip().rstrip(",").strip()
                if not entry:
                    continue
                # `expr AS alias`: the SOURCE column lives in expr, never in the alias.
                parts = re.split(r"\s+as\s+", entry, flags=re.I)
                expr = parts[0]
                for ident in _IDENT.findall(expr):
                    if ident.lower() in _SQL_WORDS or ident.lower() == tbl.lower():
                        continue
                    if ident.lower() not in seen:
                        seen.add(ident.lower())
                        cols.append(ident)
            if cols:
                return cols
    return []


def seed_type(col):
    if _DATEISH.search(col):
        return "DATE"
    if _NUMISH.search(col):
        return "NUMBER"
    return "STRING"


def seed_rows_for(cols):
    """Four rows over COLS, preserving the two properties the declared fixture encoded: one NULL in
    a nullable column, and one date below a 1990 threshold so a filter is observed to remove
    something."""
    if tuple(c.lower() for c in cols) == _PERSON_SHAPE:
        return [tuple(("NULL" if v is None else "'%s'" % v) if seed_type(cols[i]) != "DATE"
                      else "'%s'::DATE" % v for i, v in enumerate(r)) for r in SEED_ROWS]
    dates = ["'2020-01-15'::DATE", "'2021-06-23'::DATE", "'2022-12-09'::DATE", "'1930-05-11'::DATE"]
    nullable = next((i for i, c in enumerate(cols) if seed_type(c) == "STRING"), None)
    rows = []
    for r in range(4):
        vals = []
        for i, c in enumerate(cols):
            t = seed_type(c)
            if t == "DATE":
                vals.append(dates[r])
            elif t == "NUMBER":
                vals.append(str((r + 1) * 10 + i))
            elif r == 2 and i == nullable:
                vals.append("NULL")          # the NULL-propagation probe, shape-independent
            else:
                vals.append("'%s_%d'" % (c[:12], r + 1))
        rows.append(tuple(vals))
    return rows


# The seed data. Three rows, and the THIRD is the experiment: MiddleName NULL.
SEED_ROWS = [
    ("Ada", "Byron", "Lovelace", "1991-12-10"),
    ("Alan", "Mathison", "Turing",
     "1992-06-23"),
    ("Grace", None, "Hopper", "1990-12-09"),      # <- the NULL-propagation probe
]
# One row is deliberately BELOW the filter's 1990 threshold so the filter is observed to
# actually remove something. A filter that keeps every row is indistinguishable from
# `WHERE TRUE`, which is precisely the silent failure FilterTranslator falls into.
SEED_ROWS.append(("Edsger", "Wybe", "Dijkstra", "1930-05-11"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("--connection", required=True)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--break-model", default=None,
                    help="corrupt this model before running (negative test)")
    a = ap.parse_args()

    def unmeasured(why):
        print("   EXECUTION UNMEASURED -- %s" % why)
        print("   This is NOT a claim that the SQL runs, and NOT a claim that it does not.")
        return 2

    project = find_project(a.tree)
    if not project:
        return unmeasured("no dbt project (dbt_project.yml beside models/) under %s" % a.tree)
    if sh(["snow", "--version"])[0] != 0:
        return unmeasured("the `snow` CLI is not available")

    models, ephemeral = model_inventory(project)
    srcs = source_refs(project)
    will_materialise = [m for m in models if m not in ephemeral]
    if not models:
        return unmeasured("the project declares no models")

    rc, out = snow_sql(a.connection,
                       "select current_database() as d, current_warehouse() as w, "
                       "current_role() as r, current_user() as u")
    if rc != 0:
        return unmeasured("connection %r did not answer: %s" % (a.connection, out.strip()[:300]))
    try:
        ctx = json.loads(out)[0]
        database = ctx["D"]
        role, warehouse, user = ctx["R"], ctx["W"], ctx["U"]
    except Exception as e:
        return unmeasured("could not read the connection context (%s): %s" % (e, out[:200]))
    if not database:
        return unmeasured("connection %r has no current database" % a.connection)

    schema = "AIFIRST_MVP_%s_%d" % (time.strftime("%Y%m%d_%H%M%S"), os.getpid())
    print("   target       : %s.%s on %s as %s/%s" % (database, schema, warehouse, user, role))
    print("   models       : %d compiled, %d materialise, %d ephemeral (never become relations)"
          % (len(models), len(will_materialise), len(ephemeral)))
    print("   sources      : %s" % (", ".join("%s.%s" % s for s in srcs) or "none"))

    # ---- the scratch schema, and a drop that fires no matter what happens next ---------
    rc, out = snow_sql(a.connection, 'CREATE SCHEMA "%s"."%s"' % (database, schema))
    if rc != 0:
        return unmeasured("could not create the scratch schema: %s" % out.strip()[:300])
    dropped = [False]

    def drop():
        if dropped[0] or a.keep:
            if a.keep and not dropped[0]:
                print("   NOTE         : --keep, so %s.%s was LEFT BEHIND" % (database, schema))
            return
        drc, dout = snow_sql(a.connection, 'DROP SCHEMA IF EXISTS "%s"."%s" CASCADE'
                             % (database, schema))
        dropped[0] = True
        print("   cleanup      : %s" % ("dropped %s.%s" % (database, schema) if drc == 0
                                        else "*** DROP FAILED: " + dout.strip()[:200]))

    try:
        return run(a, project, models, ephemeral, will_materialise, srcs,
                   database, schema, role, warehouse, user)
    finally:
        drop()


def run(a, project, models, ephemeral, will_materialise, srcs,
        database, schema, role, warehouse, user):
    conn = a.connection
    before = hash_models(project)

    # ---- seed the source relations the models reference --------------------------------
    # IDENTIFIERS ARE UNQUOTED HERE, DELIBERATELY. A dbt `source()` renders unquoted and Snowflake
    # normalises that to upper case; creating `"corp_..._csv"` quoted makes a DIFFERENT object that
    # no model can find. This gate's own later information_schema check already assumed the unquoted
    # form (`{t.upper() for _s, t in srcs}`), so the two halves of the gate disagreed.
    seeded_n = 0
    for src_name, tbl in srcs:
        try:
            validate_identifier(src_name, "source name")
            validate_identifier(tbl, "source table name")
        except ValueError as e:
            print("   *** %s" % e)
            return 1
        cols = derive_columns(project, src_name, tbl)
        if not cols:
            print("   *** SEED SHAPE UNDERIVABLE for %s.%s -- no model selects from it in a shape "
                  "this gate can read. NOT seeding a guessed shape." % (src_name, tbl))
            return 1
        decl = ", ".join("%s %s" % (c, seed_type(c)) for c in cols)
        print("   seed shape   : %s (%s)" % (tbl, decl))
        rc, out = snow_sql(conn, "CREATE OR REPLACE TABLE %s.%s.%s (%s)"
                           % (database, schema, tbl, decl))
        if rc != 0:
            print("   *** could not create source %s: %s" % (tbl, out.strip()[:250]))
            return 1
        rows = seed_rows_for(cols)
        vals = ", ".join("(%s)" % ", ".join(r) for r in rows)
        rc, out = snow_sql(conn, "INSERT INTO \"%s\".\"%s\".\"%s\" VALUES %s"
                           % (database, schema, tbl, vals))
        if rc != 0:
            print("   *** could not seed %s: %s" % (tbl, out.strip()[:250]))
            return 1
        seeded_n = len(rows)
    print("   seeded       : %d row(s) into %s -- shape DERIVED from the models; one NULL in a "
          "nullable column, one date below the 1990 threshold"
          % (seeded_n, ", ".join(t for _s, t in srcs)))

    # ---- stage a RUNNABLE copy. Models are copied, never edited. -----------------------
    work = tempfile.mkdtemp(prefix="aifirst-exec-")
    try:
        proj = os.path.join(work, "project")
        shutil.copytree(project, proj)

        # dbt_project.yml ships `name: YOUR_PROJECT_NAME`. Bind it; touch nothing else.
        pj = os.path.join(proj, "dbt_project.yml")
        with open(pj) as fh:
            txt = fh.read()
        txt = txt.replace("YOUR_PROJECT_NAME", "aifirst_mvp").replace(
            "YOUR_PROFILE_NAME", "aifirst_mvp")
        with open(pj, "w") as fh:
            fh.write(txt)

        # A real profile, replacing the emitted placeholder. Read straight out of the
        # `snow` CLI's own connections.toml for the named connection, so nothing has to be
        # exported by hand and no secret is copied into this repo -- the profile references
        # the key FILE by path (or, for password auth, an env_var()), exactly as `snow` does.
        prof = snow_connection(conn)
        if not prof:
            print("   *** could not read connection %r from connections.toml" % conn)
            return 1
        try:
            secret = write_profiles_yml(proj, prof, role, warehouse, database, schema)
        except ValueError as e:
            print("   *** connection %r %s" % (conn, e))
            return 1

        # BIND THE SOURCE. sources.yml deliberately omits database/schema -- its own header
        # says naming one "would assert a destination the migration has not chosen". Binding
        # it at run time is the intended usage, not a workaround.
        for root, _d, files in os.walk(os.path.join(proj, "models")):
            for f in files:
                if f == "sources.yml":
                    p = os.path.join(root, f)
                    with open(p) as fh:
                        y = fh.read()
                    y = re.sub(r"(\n\s+- name: \w+\n)",
                               r"\1    database: %s\n    schema: %s\n" % (database, schema),
                               y, count=1)
                    with open(p, "w") as fh:
                        fh.write(y)

        # ---- the negative test -------------------------------------------------------
        if a.break_model:
            hit = find_model_file(proj, a.break_model)
            if not hit:
                print("   *** --break-model %r matched no model" % a.break_model)
                return 1
            corrupt_model(hit)
            print("   NEGATIVE TEST: corrupted %s -- this run MUST report failure"
                  % os.path.relpath(hit, proj))

        # The models under test are unchanged. Prove it rather than asserting it.
        after = hash_models(proj)
        drift = [k for k in before
                 if not k.endswith("sources.yml") and before[k] != after.get(k)]
        if drift and not a.break_model:
            print("   *** REFUSING TO RUN: staging altered %d model file(s): %s"
                  % (len(drift), ", ".join(sorted(drift)[:4])))
            return 1

        env = dict(os.environ)
        env["SNOWFLAKE_ACCOUNT"] = env.get("SNOWFLAKE_ACCOUNT", "")
        env.setdefault("DBT_PROFILES_DIR", proj)
        if secret is not None:
            env[PROFILE_PASSWORD_ENV] = secret

        # ---- run it ------------------------------------------------------------------
        rc, out = sh(["dbt", "build", "--project-dir", proj, "--profiles-dir", proj],
                     timeout=900)
        tail = "\n".join(out.strip().split("\n")[-14:])

        # SUCCESS DETECTION, and the first version of this got it WRONG IN THE SAFE
        # DIRECTION. It matched dbt-core's "Completed successfully"; the installed runner is
        # dbt-fusion 2.0.0-beta.14, which prints "Finished 'build' target 'dev' in 8s" and
        # one "Success models/<path>" per model. So a run where BOTH models succeeded was
        # reported FAILED. Wrong either way, but note which way: a false FAIL is loud and
        # gets fixed, a false PASS is the defect this project keeps finding.
        #
        # THE RUNNER'S COUNTS, READ TWO WAYS AND REQUIRED TO AGREE.
        #
        # This used to count `^\s*Success\s+models/` and `^\s*(?:Error|Failure|Failed)\b` only.
        # MEASURED (m1-ready re-run, 2026-08-19): this runner prints neither shape -- its per-model
        # lines are `[ERROR]: in model <name>` behind a timestamp and ANSI colour, and its closing
        # line is `Done. PASS=3 WARN=0 ERROR=3 SKIP=0 ...`. Both regexes matched zero, so the gate
        # reported `0 model(s) Success, 0 error line(s)` on a run Snowflake had told it PASS=3
        # ERROR=3. Two failures in one: the printed numbers were false, and because `ok` requires
        # `succ > 0`, a COMPLETELY CLEAN run would also have been reported FAILED. A gate that cannot
        # say yes is not a gate.
        #
        # The original comment's intent is kept: a single closing sentence is not trusted on its own.
        # It is cross-checked against the per-model error lines, and a DISAGREEMENT IS ITSELF A
        # FINDING. Printing it while still passing on the closing line was the same failure mode
        # this whole stage exists to remove: the run where `ERROR=0` sits above lines that name
        # models that errored is exactly the run a gate must not call clean, because whichever of
        # the two numbers is wrong, the gate cannot tell which -- and "cannot tell" is not "yes".
        plain = re.sub(r"\x1b\[[0-9;]*m", "", out)
        summary = re.search(r"\bPASS=(\d+)\s+WARN=(\d+)\s+ERROR=(\d+)\s+SKIP=(\d+)", plain)
        per_model_errs = len(set(re.findall(r"ERROR\]?:?\s+in model ([A-Za-z_0-9]+)", plain)))
        legacy_succ = len(re.findall(r"^\s*Success\s+models/", plain, re.M))
        disagreement = None
        if summary:
            succ, errs = int(summary.group(1)), int(summary.group(3))
            # Only NAMED per-model lines are evidence: a runner that prints none is silent, not
            # contradictory, and calling that a disagreement would fire on every failing run.
            if per_model_errs and per_model_errs != errs:
                disagreement = ("the closing line says ERROR=%d, the per-model lines name %d"
                                % (errs, per_model_errs))
                print("   *** COUNT DISAGREEMENT -- %s. The run is NOT reported clean: the gate "
                      "cannot tell which count is wrong, and that is not a pass." % disagreement)
        else:
            # No recognisable closing line. Fall back, and SAY the fallback was used rather than
            # letting a zero pass for a measurement.
            succ, errs = legacy_succ, per_model_errs
            print("   *** RUNNER SUMMARY NOT RECOGNISED -- no `PASS=.. ERROR=..` line found, so "
                  "these counts come from per-model lines alone and may undercount.")
        ok = rc == 0 and succ > 0 and errs == 0 and disagreement is None

        if not ok:
            print("   *** EXECUTION FAILED -- dbt rc=%d, %d model(s) Success, %d error(s)%s"
                  % (rc, succ, errs,
                     " -- counts disagree (%s)" % disagreement if disagreement else ""))
            for line in tail.split("\n"):
                print("       %s" % line[:150])
            print("   execution    : ran=yes built=%d/%d verdict=FAILED"
                  % (succ, len(will_materialise)))
            return 1
        print("   dbt           : rc=%d, %d model(s) reported Success, %d error line(s)"
              % (rc, succ, errs))

        # ---- verify what actually landed --------------------------------------------
        rc, out = snow_sql(conn,
                           "select table_name, table_type from %s.information_schema.tables "
                           "where table_schema = '%s' order by table_name"
                           % (database, schema))
        landed = []
        if rc == 0:
            try:
                landed = [(r["TABLE_NAME"], r["TABLE_TYPE"]) for r in json.loads(out)]
            except Exception as ex:
                print("   *** EXECUTION FAILED -- could not parse information_schema.tables "
                      "JSON (%s: %s). Not treated as 'materialised nothing'."
                      % (type(ex).__name__, ex))
                print("   execution    : ran=yes built=?/%d verdict=FAILED"
                      % len(will_materialise))
                return 1
        # the seeded source is one of them; do not count it as a model
        src_tables = {t.upper() for _s, t in srcs}
        model_rels = [(n, t) for n, t in landed if n.upper() not in src_tables]

        print("   relations    : %d created by the models -- %s"
              % (len(model_rels), ", ".join("%s(%s)" % (n, t.split()[0].lower())
                                            for n, t in model_rels) or "none"))

        # ---- THE NULL-PROPAGATION OBSERVATION ---------------------------------------
        mart = next((n for n, _t in model_rels if "summary" in n.lower()), None)
        null_verdict = "NOT CHECKED (no mart relation found)"
        if mart:
            rc, out = snow_sql(conn, 'select * from "%s"."%s"."%s"' % (database, schema, mart))
            rows = []
            if rc == 0:
                try:
                    rows = json.loads(out)
                except Exception as ex:
                    print("   *** mart JSON unreadable (%s: %s) — null-concat observation "
                          "UNMEASURED, not silently empty."
                          % (type(ex).__name__, ex))
                    rows = None
            if rows is None:
                null_verdict = "UNMEASURED (mart result JSON unreadable)"
            else:
                hopper = [r for r in rows
                          if any(str(v or "").upper() == "HOPPER" for v in r.values())]
                nulls = [r for r in rows if any(k.upper() == "FULLNAME" and v is None
                                                for k, v in r.items())]
                print("   mart rows    : %d" % len(rows))
                if nulls:
                    null_verdict = ("CONFIRMED IN DATA -- %d row(s) returned FullName NULL, "
                                    "because Snowflake's || propagates NULL. DataStage's `:` "
                                    "propagates too, so this is FAITHFUL." % len(nulls))
                elif hopper:
                    null_verdict = ("*** UNEXPECTED -- the NULL-MiddleName row came back with a "
                                    "non-NULL FullName. Something rewrote the expression.")
                else:
                    null_verdict = ("NOT OBSERVED -- the NULL-MiddleName row is not in the mart "
                                    "at all (the 1990 filter may have removed it).")
        print("   null concat  : %s" % null_verdict)

        built = len(model_rels)
        verdict = "EXECUTED" if built else "RAN BUT MATERIALISED NOTHING"
        print("   execution    : ran=yes built=%d/%d ephemeral=%d verdict=%s"
              % (built, len(will_materialise), len(ephemeral), verdict))
        print("   NOT a claim  : the SQL ran. Nothing here compares a row against the source")
        print("                  system, so this says nothing about whether it is CORRECT.")
        return 0 if built else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
