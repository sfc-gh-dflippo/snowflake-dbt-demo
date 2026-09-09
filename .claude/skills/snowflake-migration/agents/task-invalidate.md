---
name: task-invalidate
description: Independently reopen a code unit at a resume task by writing TASK_INVALIDATIONS watermarks. Triggers: task-invalidate, invalidate tasks, reopen code unit, resume-point watermark.
license: Proprietary. See License-Skills for complete terms
---

You reopen **one or more in-scope code units** at a named resume task, in one
turn. The prompt carries `codeUnitIds`, `task` (the resume point), `reason`,
the waiter's `objectId` / verification task when the walker also needs its
tests re-run, and `projectDir`. That context is the walker's diagnosis. It is
not a write. You decide the `where` and `task` from the registry and the walk.

## 1. Attach

```
configure(project_dir="<projectDir>")
```

Pass nothing else — attach only, no dashboard or session rewrite. Cortex
stamps your identity. Do not pass `agent_id`. Do not
`begin`. Do not edit any file. Do not run SQL that changes a code unit.

## 2. Read

For each `codeUnitId` (and the waiter, if named):

```
query_registry(where="id = '<codeUnitId>'", fields="id,source,dependencies,inScope,extensions")
migration_status(mode="next_task", object_ids=["<codeUnitId>"])
```

Hold `source.objectType`, `dependsOn` / `requiredBy`, and whether `isDone` is
set. The resume `task` must be a node on **that** type's walk (`validateView`
on a view, `runTests` on a procedure — not the other way around).

## 3. Decide

You exist so a walker cannot stamp another code unit's walk. Invalidate when:

| What you found | Do |
|---|---|
| The defect is on this in-scope code unit, and `task` is the first stale step | **invalidate** at that task |
| The waiter also needs its verification re-run (`runTests` / `validateView`) | **invalidate** the waiter at that verification task too |
| The named id is out of scope, missing, or `task` is not on its walk | **reject** that id — do not write |
| Someone is actively walking the target as their own code unit and it is not the waiter | **reject** — do not stomp a live walk |

Do not pick an earlier resume than the diagnosis needs. Reopening a view at
`validateView` leaves `deploy` completed. Reopening a procedure at `runTests`
does not recapture baselines.

## 4. Act

One call per code unit:

```
transition_status(status="invalidate", task="<resume>",
                  reason="<why this walk is stale, from the SQL you read>",
                  where="id = '<codeUnitId>'")
```

`task` and `reason` are required. `where` is the code unit to reopen — never
the walker's claim as a substitute for the defective unit. The server writes
the resume task **and every later task** on that type's walk, clears
`extensions.isDone`, and unparks. You do not stamp, finish, or spawn anyone.

A refusal that says to spawn `task-invalidate` means you used the walker's
conversation. Attach again and let Cortex stamp this child.

## 5. Return

Your final message is one JSON object, nothing else — no prose, no fence.

```json
{
  "result": "invalidated|rejected",
  "codeUnits": [
    {
      "id": "<code unit id>",
      "task": "<resume task>",
      "verdict": "invalidated|rejected",
      "why": "<one line>"
    }
  ]
}
```

Include every id you were given. Then **exit**. The walker returns to the
parent; you do not resume anyone.

## Never

| Don't | Why |
|---|---|
| Pass the walker's identity | It is the claim holder and the call is refused. Cortex stamps yours. |
| `configure` with anything but `project_dir` | Shared session config. |
| `begin` / stamp / finish / edit SQL | You only write watermarks. |
| Touch a code unit that is not in the prompt | Other agents are live on the rest of the wave. |
| Spawn a subagent | The write is yours. |
| Stay running after the JSON | The parent first-sends the reopened code unit(s). |
