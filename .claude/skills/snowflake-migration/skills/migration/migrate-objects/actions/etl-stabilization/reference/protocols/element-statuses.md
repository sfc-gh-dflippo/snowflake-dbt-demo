## Canonical Element Status List

All sub-skills MUST use only these statuses when updating elements via `track_status.py update`:

| Status | Set by | Meaning |
|--------|--------|---------|
| `pending` | init | Element has not been processed yet |
| `no-fix-needed` | test-gen | Zero EWI/FDM issues — element passed baseline with no failures and no fixes needed |
| `orch-tested` | orchestration-test-gen | Test generated and baseline run complete (may have expected failures) |
| `fixed` | orchestration-fixer | Fix applied to orchestration SQL by apply-fixes agent and verified |
| `test-passed` | orchestration-fixer | All assertions pass (with or without fixes applied) |
| `test-failed` | orchestration-fixer | Assertions still fail after max fix-test cycles |
| `skipped` | orchestration-test-gen or fixer | Element excluded — requires `--reason` (valid reasons: `disabled-in-source`, `container-only`, `file-io-noop`, `dbt-dependency`, `external-dependency`) |
| `needs-user` | orchestration-fixer | Fix requires user decision (e.g., "does this staging table exist?") |
| `auto-fixed-needs-review` | orchestration-fixer (autonomous) | Agent applied a best-guess fix in autonomous mode — orchestrator presents to user for review at phase end |
| `failed` | orchestration-fixer | Unrecoverable error (not a test failure — an infrastructure or tooling failure) |

### Terminal Statuses

A **terminal status** means the element is fully processed and will not change again in this phase. The orchestrator checks that ALL elements have a terminal status before marking a phase complete.

Terminal statuses: `test-passed`, `fixed`, `no-fix-needed`, `skipped`, `needs-user`, `auto-fixed-needs-review`, `failed`.

Non-terminal statuses: `pending`, `orch-tested`. Elements with these statuses require further processing.

**Status transitions:**
```
pending → orch-tested         (test-gen: baseline run complete)
pending → skipped             (test-gen: disabled-in-source, container-only, file-io-noop, dbt-dependency, external-dependency)
orch-tested → no-fix-needed   (fixer: zero issues, all assertions pass without changes)
orch-tested → test-passed     (fixer: assertions pass)
orch-tested → test-failed     (fixer: assertions fail after 3 cycles)
orch-tested → needs-user      (fixer: requires user input)
orch-tested → auto-fixed-needs-review  (fixer: autonomous best-guess)
orch-tested → fixed           (fixer: fix applied and verified by apply-fixes agent)
fixed → test-passed           (post-apply validation confirms)
fixed → test-failed           (post-apply validation fails)
Any → failed                  (unrecoverable error)
```
