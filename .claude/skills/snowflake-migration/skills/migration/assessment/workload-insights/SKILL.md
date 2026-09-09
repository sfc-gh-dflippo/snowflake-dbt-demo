---
name: workload-insights
description: Builds SQL Server Discovery from Extended Events `.xel` files by running `scai assessment workload-insights --input <file>`. SQL Server only. Reads captures in place.
parent_skill: assessment
license: Proprietary. See License-Skills for complete terms
---

# Discovery

Thin, non-interactive wrapper over `scai assessment workload-insights`. The
parent supplies absolute `.xel` paths. The command streams the captures and
writes timestamped JSON under the project. Never parse or rewrite the capture
or JSON. Never copy `.xel` files into the project. Never ask the user questions.

- **Supported dialect:** SQL Server. Any other dialect aborts with `ASM0034`;
  report `skipped`, not an error.
- **Input:** one or more binary Extended Events `.xel` files. Rollover files
  from the same capture are separate `--input` arguments. Any filename works.

## Run

```bash
scai assessment workload-insights \
  --input /abs/path/WorkloadReport_XE_0.xel \
  --input /abs/path/WorkloadReport_XE_1.xel
```

Run from `project_dir`. The command writes:

`<project_dir>/artifacts/assessment/workload-insights-YYYYMMDD_HHMMSS.json`

## Sub-agent contract

On entry, call `configure()` with `project_dir` from the parent's context
block. Take no user prompts. On completion return JSON only:

```json
{
  "sub_skill": "workload-insights",
  "status": "ok",
  "output_json": "<absolute path to workload-insights-*.json>",
  "summary": "<one line: databases, total events, user executions, errors>",
  "error": null
}
```

- Unsupported dialect (`ASM0034`): `status` `"skipped"`, `output_json` `null`,
  `error` `null`.
- Any other failure: `status` `"error"`, `output_json` `null`,
  `error` `"<message>"`.
- A large-file or long-running parse message on stdout is not an error. Exit
  code 0 plus a written artifact means `"ok"`; fold the message into `summary`.
- Do not include SQL text, parameters, or error messages in the response.

## Reference

`references/create-extended-events-session.sql` is the starter session SQL the
**parent** pastes when the user chooses to provide files later. This sub-skill
never runs it. `CREATE` leaves the session stopped; the user reviews all values,
replaces `YourDatabase`, and explicitly runs the commented `STATE = START`.
