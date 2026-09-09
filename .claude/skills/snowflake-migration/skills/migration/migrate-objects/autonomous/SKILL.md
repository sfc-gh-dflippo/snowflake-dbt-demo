---
name: migrate-objects-auto
description: Autonomous version of migrate-objects — dispatches one subagent per ready task group, refills as they finish, and only stops to ask when a subagent is stuck. Triggers: autonomous migration, run unattended, migrate objects automatically, auto-pilot the wave, migrate everything in parallel, swarm the objects.
parent_skill: migrate-objects
license: Proprietary. See License-Skills for complete terms
---

# Migrate Objects — Autonomous

## On Entry **IMPORTANT DO NOT SKIP**

Tell the user:

> **Autonomous mode.** I'll work the wave by giving each object its own subagent,
> which walks it the whole way — convert, deploy, tests, fixes — and I'll refill as
> they finish. I'll interrupt you only when an agent is stuck, when a dependency
> needs a human decision, and before any data moves. Say "stop" at any point and
> I'll let in-flight work land.

## Step 0: Preflight

1. `configure(project_dir=<project dir>, subagent_mode=true, snowflake_connection=<the configure connection the first prompt named>)`. Read the appended migration-status block. Bring
   the shared data infrastructure up: `data_infrastructure(mode="up")`. Relay its
   `cost_reminder`. `status="not_ready"` is not a green light — a first local bring-up 
   runs every schema migration and can need more than one call, so follow its `remediation` 
   and call `up` again until it reports `ready`. Once means one *successful* bring-up for
   the wave, not one call.
2. If `configure()` reports setup is not finished, read
   [../../setup/SKILL.md](../../setup/SKILL.md) then come back here.

`subagent_mode` attributes writes per Cortex conversation. Set it once here; it lasts the
life of the server and cannot be turned off. Cortex stamps identity on every MCP call —
do not pass `agent_id`. The parent hook injects `0000` while this latch is on: park a looping
object, reset a remediated transient failure, and relay non-terminal guidance.
Acknowledge unreviewed notes only in Step 3 (`review`), never in the dispatch
loop. Object-level outcomes stay parked for a person in an interactive session.
`deploy`, `migrate_data`, and `validate_data` are not binding-checked — keep
each agent on its own object.

## Step 1: Ask how many subagents to run at once

Offer 2 / 4 / 6, recommend **4**. State the
trade-off: more slots finish the wave faster, burn proportionally more tokens,
and produce more escalations competing for their attention. Call it `N`. Never
exceed it, and never quietly raise it.

**Wait for the user's response — do not dispatch until they answer.**

## Step 2: The loop

The unit of dispatch is an **object**: one subagent takes one object and walks it
through as many tasks as it takes, then stops. You hold no migration state —
[the server does](#where-the-state-lives). Track the Cortex `resume` id only as
a backup; **liveness comes from `my_objects_board`** (`flight` on each row,
`walkerRunning` for slots), not from who you remember spawning. A row's
`agentId` is the live Cortex session when a walker exists (`task` returns
it as `agentId` — a UUID). Do not copy an `agentId` into prompts or MCP
calls; Cortex stamps the child's session id.

### 2a. Read the board

```
migration_status(mode="my_objects_board")
migration_status(mode="escalations")
```

`my_objects_board` is the only status shape you read for dispatch. Each row is
one object: `objectId`, `name`, `type`, `agentId`, `bucket`
(`ready` | `blocked` | `done` | `escalated` | `errored`), and `flight`
(`running` | `idle` | `none`). `walkerRunning` is the live-child slot count;
`walkerIdle` is yielded walkers. Do not overlay `hub(mode="status")` for
dispatch — the board already stamped walker liveness (running wins over idle).
Two live children on one object are forbidden: if `flight` is `running` or
`idle`, do not first-send another.

Do not call `my_objects_summary`, `my_objects_details`, `next_task`, or
`task_views`. Those name the current task and why it is waiting; they are for
interactive sessions and for the child walking the object.

`escalations` is the human queue. Read `escalations` (open asks) and `answered`
(`guidance`). Do not pass `details=true`. Do not read `notes[].asks`
/ `choice` or `overrideAcceptedCases` — default payloads omit those bodies.
`unreviewedCount` is a tally for Step 3, not a reason to stop.

Re-read both every time a child **returns**.

### 2b. Top off the object pool

A slot is occupied only by a **live Cortex child**. Read that from
`my_objects_board.walkerRunning`, not from memory. `waiting` on a
relay job, `stuck` / `escalated` parks, leftover claims from a dead session,
and `completed` objects do not occupy one — those children are **idle**
(`flight=idle`) or gone (`flight=none`). `free_slots` is `N` minus
`walkerRunning`. When it is greater than zero, pull:

```
migration_status(mode="next_objects", limit=<free_slots>)
```

The board lists only claimed objects. Unclaimed work is invisible there —
`next_objects` is the only way to see it. It returns objects whose current
walk is not blocked — the same verdict `next_task` would give — or comes
back empty. Do not skip this pull because a leftover looks blocked on a
sibling still in flight. Do not wait for the flight to empty.

`next_objects` also returns `leftover_claims`: open claims with **no walker**
in the ledger (`flight` would be `none`). Live or parked walkers are omitted —
those are not leftovers. Each entry is `{object_id, name}` — no `agentId`.
**Before** waiting, first-send every leftover (a **new** child, no `resume`).
That child's `begin` reclaims the dead conversation's hold. Do not first-send
a leftover that already has `flight` running or idle on the board — the
server already filtered those out. Count those first-sends against
`free_slots`, then spawn from `objects` for whatever slots remain.

Each `objects` entry has `object_id`, `name`, `display_name`, and `type`.
Hand the object ids to the subagents you dispatch — **each subagent claims
its own object**. You never call `transition_status(status="begin")`
yourself: the agent that does the work owns the claim. A spawn that dies
*before* `begin` leaves the object unclaimed (2b will offer it again). A
child that dies *after* `begin` still has an open claim — first-send a new
child from `leftover_claims` (or from 2d when the child returns `completed`
without `done`).

Keep the pair — object id, Cortex `resume` id — only to match a wake line
to `task(resume=…)`. Prefer the board `agentId` when `flight` is running or idle.
A leftover first-send is a new conversation; do not resume a dead child.

> **Claim narrowly.** [../actions/claim_objects.md](../actions/claim_objects.md)
> forbids auto-claiming because a claim hides an object from every teammate's
> picker. Autonomous mode claims without asking, so keep the batch small: only the
> free slots, only ids from this turn's `next_objects`, never a category `where`
> predicate. The user authorized `N` slots, not the whole wave.

### 2c. Dispatch

**One object per subagent, and the agent is always
[`general-task`](../../../../agents/general-task.md).** It walks its object through
every task the machine offers — convert, deploy, tests, fixes — and stops when the
object is done or needs a human. You do not route by task, and there is no
per-task agent to choose.

Up to `N` in flight. First send and later send are different `task` calls.

**First send** — you have no Cortex `resume` id for this object. Spawn in a
single turn, one prompt each, and always pass `description` (a short object
label). Do not pass `resume` or `fork_conversation_history`.

```
Migrate this object end-to-end, following your agent definition.

objectId:           <a single id>
projectDir:         <absolute project_dir>
pluginDir:          <absolute plugin root — the directory this skill was loaded from, above skills/migration/>
snowflakeConnection: <Cortex `sql_execute` `-c` from the first prompt — often a reader account, not the configure connection>
snowflakeDatabase:  <the session `snowflake_database` from configure — the Snowflake target>
guidance:           <verbatim words from `answered` — only when there are some>
```

`task` returns an `agentId` (UUID). Store it as this object's `resume` id. That
is the conversation, and it is the `agent_id` you pass to `agent_output` when
the board later shows `flight=idle`. A later `task(resume=…)` returns a
**different** UUID — a wait handle for that send only. Do not overwrite the
stored `resume` id with it, and do not pass that handle to `agent_output`.

One imperative line, then values. The line matters: four bare `key: value` pairs
read as context rather than a request, and an agent handed only context asks
what you want — which nobody is there to answer. Say what to do, once, and leave
what to do it with to the definition.

Those values are the rest of the first prompt. `pluginDir` is among them because
`executor.skill` values are relative to the plugin's `skills/migration/` directory and
the subagent cannot locate that on its own. Do not put `agentId` in the prompt —
Cortex stamps the child's session id on every MCP call. `snowflakeConnection`
on the first-send is Cortex `sql_execute` `-c` and may be a **reader** account.
MCP writes use the parent `configure(snowflake_connection=…)` connection, which
can differ. Without `snowflakeConnection` the child omits `-c`
and hits Cortex's default account; without `snowflakeDatabase` it qualifies SQL
with the source catalog name.
Do not tell the child to load `snowflake-migration:migration` — that is the
interactive router; its contract is [`general-task`](../../../../agents/general-task.md).
The agent definition is the contract — it already carries the loop, the fix-loop
thresholds, the escalation test, and the return schema — and anything the prompt
adds competes with it instead of replacing it. A prompt that invents a retry limit,
names a field the tools do not return, or specifies its own return shape leaves the
agent choosing between two sets of rules; a prompt that tells it not to escalate
converts a decision that needed a human into a silent guess.

**Later send** — you already have a `resume` id. The child finished a turn
(`waiting` / `partial` / `stuck`) and this conversation still has the walk.
Call `task` with `resume` set to that stored UUID, `description` set, and a
prompt that is **only the new line**. Do not repeat `objectId` / `projectDir` /
`pluginDir` / `snowflakeConnection` / `snowflakeDatabase` / the migrate-this-object line — they are
already in that conversation. Do not pass `fork_conversation_history`.

```
relay_wake: <the wake line, verbatim>
```

or, after a person answered:

```
guidance: <verbatim words from `answered`>
```

or, when the board says `ready` again after a `partial` / remediated `reset`:

```
Continue this object from the machine's next task.
```

Store the UUID this `task` call returned as the wait handle. Do not wait yet —
finish every other first send and wake for this turn, then wait once in 2d.
Keep resuming the stored id.

If you have lost the `resume` id, this is a first send: full prompt, no
`resume`. That is the killed-session path, not a wake.

**One live child per object, never two at once.** Two live conversations on
one object race on the same files and the same registry entries. Board
`flight` is the check, not memory. Resuming the same conversation
is the sequential reuse; a leftover first-send is only for a child with
`flight=none`. The skill forbids two live children on one
object — the server will reclaim a dead holder's claim, not referee two
live ones.

**Never dispatch two agents for one object.** Because an agent walks the whole
pipeline, an object it is mid-walk on will keep resolving to a *new* task each time
you re-read the board. Track in-flight by **object id**, not by task: the object is
the unit of work and the only safe key. Two agents on one object race on the same
files and the same registry entries. A `resume` call is not a second agent.

**Check `answered` before every send.** An answered escalation has already
un-parked its object, so it comes back looking like ordinary work with no sign that
a person decided anything. If `migration_status(mode="escalations")` lists the
object under `answered`, the next send is a later send when you have its
`resume` id (prompt is the `guidance:` line) and a first send when you do not.
An answered object is claimed by nobody, so a first send claims it like any
other work. Dropping the guidance
sends an agent to make a decision that was already made for it.

`N` is the only dispatch limit you control. Do not inspect why a sibling is
`blocked` or which task it is on.

### 2d. Refill

This session is headless: ending the turn exits the process and kills every
child. Keep it alive with **one wait per turn**, and only after this turn has
filled every free slot.

**Top off, reap, then wait.** Re-read the board (2a) and pull `next_objects`
(2b) before every wait — after a child returns, after a wake, after empty
hub wakes. First-send every `leftover_claims` entry (new child, no
`resume`), then spawn every other first send and every pending wake in
this turn (background `task` calls). Reap every `flight=idle` row (below)
before the wait. Do not start a wait while leftovers, free slots, or
unreaped idle rows remain. A live Cortex child on one object does not
block filling the other slots. Neither does a `waiting` object or an
escalation.

**Reap idle children before any wait.** `flight=idle` means the walker has
yielded and its return JSON is sitting in Cortex. Pull it with:

```
agent_output(agent_id="<the row's agentId>")
```

Pass only `agent_id`. Do not pass `wait`. `wait=true` is denied in
`subagent_mode`: it blocks this session until one child finishes and starves
the other slots. Omitting `wait` is the reap; `wait=false` is the same.

Call that once per `flight=idle` row **before** `bash sleep` or
`hub(mode="wait")`. A `Background agent finished` line, a Monitor
`wake up 0000`, and `bash sleep` are not a reap — they do not return
`objectId` / `result`. After every reap, 2a and 2b. Helpers
(`test_case_verifier`, `task-invalidate`) do not stamp `flight` — do not
poll them.

Wait once, after this turn has filled every free slot. **Liveness is
`my_objects_board`, not memory:**
- If `walkerRunning > 0`: `bash sleep 30`, re-read the board, reap every
  `flight=idle` row, then 2a/2b. Repeat. Sleep only paces the next board
  read. Do not call `agent_output` on `flight=running` — that peeks a live
  transcript.
- If `walkerRunning` is 0 **and** 2b returned nothing (or `free_slots` is
  0): `hub(mode="wait", confirm=true, cursor=<last>)` instead of ending the
  turn (`job_status(wait=true)` is the same gate). Without `confirm=true`
  the tool returns a reminder and does not block — that is not a wake.
  Empty `wakes` means go back to 2a/2b, not wait again with idle slots.
  Do not call `hub(mode="wait")` while 2b would still return objects.

Arm **one** Monitor for the wave: `orchestrator_watch.watch_command` from
`configure`, `hub(mode="status")`, or `job_status(monitor=true)`,
`persistent: true`. Each line is an instruction. Do not open the job, call
`job_status` on it, or read the relay log.

A wake looks like `wake up 550e8400-e29b-41d4-a716-446655440000 and ask it to check new event from relay. …`.
That is a later send: `task(resume=<that UUID>)` with the `relay_wake:` line
(the UUID is the child's `agentId`). Do not spawn a new `general-task`
for it. That later send is the live child; it occupies a slot only while
the board lists it `flight=running`. A `wake up 0000 …` line means reap
every `flight=idle` row with `agent_output(agent_id=…)` (omit `wait`), then
2a/2b. Do not inspect the event. Sleep is not that reap.

When `agent_output` returns, read only these keys from its result JSON:
`objectId`, `tasksCompleted`, `result`, `reopenedCodeUnits`. Ignore `Recent Output`, `task`,
`failed`, `blocked`, `evidence`, `asks`, and `notes`. Then 2a and 2b
**before** you send a wake or wait again.

Report one line per return (`dbo.Customers: done, 4 tasks`) and the running
tally.

| `result` | What you do |
|---|---|
| `completed` | Re-read the board. `done` → drop the `resume` id. Anything else → the child died holding the claim. First send again (new child, no `resume`). |
| `partial` | Re-read the board. `blocked` → leave it. `ready` → later send (the machine routed recovery). `escalated` → 2e. |
| `stuck` | 2e. Do not send again until a person answers. |
| `waiting` | Keep the `resume` id; drop the slot. The object is on a relay job — its own migrate/validate, or a dependency the machine registered. Later send only on a wake for that stored `resume` id. |
| `reopened` | Keep the waiter's `resume` id; drop the slot. First-send each id in `reopenedCodeUnits` that is not already `flight` running or idle. Do not later-send the waiter until those walks finish. This is not a 2e interrupt. |

Do not send again for a `partial` whose board bucket is still `blocked`.

Reset only from evidence you already have — infrastructure now reports ready,
or a shared job reached terminal — never from the child's `failed` payload:

```
transition_status(status="reset", task="<task>", where="id = '<id>'")
```

Then a later send of the same object, once.
Record the remediation or clearing evidence in your report. If nothing changed,
leave an existing escalation open; if the object is not parked yet, park it with
the exact failure and the repair needed before a rerun.

Deterministic row mismatches, schema drift, invalid identifiers or compilation
errors in generated SQL, and a tool invocation that fails the same way on repeat are
not transient infrastructure failures. Park them rather than resetting or
sending the unchanged task again. `reset` clears both the stamp and escalation
marker, so using it before remediation erases the durable record of a failure the
next run will reproduce.

### 2e. Escalate

Escalation is the only reason to interrupt the user. An escalated object does
not occupy a slot — keep dispatching up to `N` live children while they read.

**Read the queue, don't rely on what came back.** A subagent returning `stuck` is
one source; the authoritative one is:

```
migration_status(mode="escalations")
```

Check it on every board read (2a), not only when an agent returns. It is
project-wide, so it also surfaces escalations raised by another person's agents,
and answers recorded in an earlier session — including one you were killed in the
middle of.

Present each **open** row: object, task, `causeClass` if set, and the numbered
choices from `asks`. That is the only time you read inside an object. Batch
them. Do not open `notes` or `overrideAcceptedCases`.

**Record the decision with one call — the user's decision, never your own.** An
escalation exists because the agent that raised it judged the choice not to be an
agent's to make, and `answer` records *a person's* choice: the row names who
decided. Do not settle one by reading the escalating agent's skill and writing
guidance back yourself. If the queue cannot be answered without the user, the run
terminates with it open — 2f allows that.

The call closes the escalation *and* un-parks the object:

```
transition_status(status="answer", where="id IN (...)", task="<task>",
                  resolution="guidance|decompose|needs_repair",
                  reason="<the user's words>")
```

The parent hook stamps `0000` here, on a remediated `reset`, on `escalate`, and on `review`. That is the id that
says a person decided — the row records which agent recorded the answer, so
answering under a subagent's id would attribute the user's decision to the agent that
asked.

| The user says | `resolution` | Then you |
|---|---|---|
| Try again, here's how | `guidance` | Later send with their words as the `guidance:` line. `reason` is required. |
| It's too big — split it | `decompose` | Decompose per [LONG_PROCEDURE.md](../migrate-object/references/LONG_PROCEDURE.md), then later send. |
| Leave it for a human | `needs_repair` | Nothing. It stays parked but leaves the open queue, so it stops being re-offered every cycle. |
| Apply an object-level outcome | — | Leave it parked. Putting an object out of scope or accepting its current state belongs to the interactive migration flow. |

`skip` remains a human-interactive out-of-scope action. It is not an autonomous
`answer` resolution; leave that choice parked for the interactive session.

**Do not send again without answering first.** `error="human"` has no failure
transition, so the object stays parked until the stamp is cleared: `next_task` keeps
resolving `needsHuman`, and the agent you sent reads that and returns `stuck`
having done nothing. `guidance` and `decompose` are the two resolutions that un-park;
the response reports `unparked` so you can tell it happened.

One thing parked here is not a decision to make: a transient failure whose condition
has demonstrably cleared. The remediated `reset` in 2d un-parks it without recording
that anybody chose anything. Every other way out of the queue is a person answering.

A missing dependency (`reason: "missing"`) needs the register / stub / out-of-scope
menu from [../SKILL.md](../SKILL.md) Step 2c. Register and stub are work you can
dispatch. Keep choices that determine the object's scope or unmet requirements
parked for the interactive migration flow.

Not every escalation is a failure. An agent that stops on a design decision — no
Snowflake equivalent, a definition missing from the source, two readings that
differ in row count — has done the right thing and has nothing to show you but the
ambiguity. Those arrive with no `causeClass`.

**Stop the loop** is still an option at any point: let in-flight agents land, then
Step 3.

### 2f. Termination

The loop ends when all four hold:

- nothing is in flight (`walkerRunning` is 0, idle walkers reaped,
  and no object `waiting` on a relay job — that job is still the wave, even
  though it does not occupy a slot),
- the board has no `ready` objects (`escalated` / `blocked` do not block
  termination, and waiting for them to empty would hang the run on an
  unanswered question),
- `next_objects` is empty,
- every remaining object is `escalated`, `blocked`, `done`, `errored`, or
  out of scope.

A leftover whose child is gone and whose object is not `done` is
none of those: first-send a new child (2d `completed`, or `leftover_claims` in
2b). Do not treat `next_objects.objects` being empty as the wave being empty
while `leftover_claims` is non-empty or you still hold those pairs.
Credential / OAuth expiry is not a human question — do not escalate it;
the run cannot continue until the owner refreshes auth.

A `ready` object with nothing in flight is none of those: dispatch it or park
it, but never report around it. An object that returns `ready` again with an
empty `tasksCompleted` must not be dispatched again until the board changes.
If there is no concrete remediation or clearing evidence, park it:

```
transition_status(status="escalate", task="<the task it keeps returning on>",
                  asks=["<the choice you cannot make for the user>"],
                  cause="<sql|infra, from the agent's failed.error — omit it otherwise>",
                  reason="<what the two dispatches tried>", where="id = '<id>'")
```

It leaves `ready` because it is parked, which meets the fourth condition, and the
user gets a question they can answer instead of an object no board read would have
shown them.

Then run Step 3. If the board still has `escalated` rows or `openCount` is
non-zero at that point, say so in the report — the run finished, the wave did
not.

## Where the state lives

You keep no ledger. Every question about the run has an authoritative answer
somewhere else, and re-reading beats remembering:

| Question | Source |
|---|---|
| What claimed work is ready? | `my_objects_board` → `bucket=ready` |
| What unclaimed object can take a free slot? | `next_objects` |
| Which Cortex children are live vs yielded? | `my_objects_board` → `flight` (`running` / `idle` / `none`); `walkerRunning` is the slot count |
| How to reap a yielded child? | `agent_output(agent_id=<board agentId>)` — omit `wait`. Only `flight=idle`. Sleep / `0000` / `Background agent finished` are not a reap. `wait=true` is denied. |
| What is parked on a person? | `my_objects_board` → `bucket=escalated`, and `escalations` for the asks |
| What is claimed, by whom? | `my_objects_board` → `agentId` (live walker session when `flight` is not `none`) |
| Who to wake for a relay event? | The wake line (`resume` that UUID). `0000` → `agent_output(agent_id=…)` on each `flight=idle` row, omit `wait`. Do not read the job. |
| Is an object done? | `bucket=done` — the machine closes a verified terminal (`isDone`) |
| What is waiting on a human, and what did they decide? | `escalations` → `escalations` and `answered` |
| Unreviewed judgments (count only, mid-loop) | `escalations` → `unreviewedCount` |

Do not call `next_task`, `my_objects_details`, or `task_views`. You do not
need where an object is in its pipeline or why it failed.

Do not keep a private live-child set. Board `flight=idle` (including a child
that returned `waiting`) is yielded; counting it as live from memory parks
the wave on sleeps while Monitor's wake is already consumed. A leftover
first-send vs resume is still: new child when `flight=none`;
`task(resume=<board agentId>)` when it is idle and a wake names that UUID.

Escalations survive the session — read them, don't remember them.

## Step 3: Report

Call `migration_status()` and report as [../SKILL.md](../SKILL.md) Step 3 does,
plus what autonomous mode adds: objects finished without intervention, objects
escalated (open asks, as in 2e), unreviewed notes as **object + task** only
(do not pass `details=true`; do not quote SQL or choice text), then
`transition_status(status="review", …)` in one batch.
Also: subagents dispatched, remediated tasks reset, and outcomes stamped by
an agent because the machine could not observe them.

A stage count is not a done count. Take the finished number from the
`migration_status()` you already called — `objects_done` — and leave `stage_totals`
out of it: an object can be deployed, data-migrated, and still not finished, so
adding stage counts together counts one object several times. `objects_done` is
project-wide, which is what a wave total should be; `doneCount` on
`my_objects_board` counts only what you hold a claim on.

Build every line the board can confirm from the board. A returning agent's `result`
is a claim, not a finding: report what you cannot confirm as what that agent said,
attributed to it, and never let one agent's `completed` become a report line of its
own. Nothing counts remediated resets for you — take those from the board and
what you recorded when you reset, and if you cannot tell how many there were,
say what you saw instead of a number.

Then tear down: `data_infrastructure(mode="down")`, or
[../../data-infrastructure/teardown/SKILL.md](../../data-infrastructure/teardown/SKILL.md)
when the project configured a `compute_pool` and data work ran.

## Resuming an interrupted run

A killed session loses your dispatch bookkeeping and nothing else. Claims live in
Snowflake, task stamps in the registry, merges in git, escalations and their
answers in Snowflake. Re-enter this skill: Step 0, then 2a, and the board shows
exactly where the wave stands — including objects whose subagent died mid-task,
which resolve back to that task as pending (`reclaimed_from_other_sessions` names
the ones taken back from the dead session). Nothing needs manual cleanup.

Read `migration_status(mode="escalations")` before dispatching anything. A question
you asked before the session died is still open, and an answer the user gave is
still waiting to be acted on — sending those objects again without answering them
first just parks them again. The Cortex `resume` ids died with the session, so
every object is a first send.
