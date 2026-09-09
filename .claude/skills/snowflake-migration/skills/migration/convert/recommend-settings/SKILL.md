---
name: recommend-settings
description: Recommend per-language SnowConvert conversion settings based on the input source code. Reads the project's source SQL, matches constructs to the dialect's available settings, and proposes flags for `scai code convert` (user confirms). Load from `convert` or `code-conversion-only` before running the conversion. Triggers: recommend settings, conversion options, which flags, tune conversion, per-language settings.
parent_skill: migration
license: Proprietary. See License-Skills for complete terms
---

# Recommend Conversion Settings

Load this skill from `convert` (or `code-conversion-only`) right before running `scai code convert`. It inspects the input and proposes conversion settings for the user to confirm, then returns the chosen flags to the caller.

## On Entry

Tell the user:
> **Tuning conversion settings.** I'll scan your source and suggest SnowConvert options that fit what's in your code. You'll confirm before anything runs.

## Workflow

### Step 1: Load the settings catalog

Run:
```bash
scai code convert --list-settings --json
```
This returns `{ "sourceLanguage": "<Dialect>", "settings": [ { "longName", "shortName", "kind", "group", "helpText", "options", "default", "optional", "allowsMultiple", "min", "max", "currentValue" }, ... ] }`.

- `sourceLanguage` is the project's dialect — remember it as `<DIALECT>`.
- Treat `settings[]` as the ONLY valid options. Never propose a flag whose `longName` is not in this list.
- `currentValue` (when present) is what the project already has persisted — do not re-recommend a setting already at the value you'd suggest.

If the command fails, tell the user you couldn't load the catalog and skip recommendations (return no flags to the caller); do not block the conversion.

### Step 2: Load dialect hints

Look for a hint file at `./reference/<DIALECT-lowercase>.md` (e.g. `./reference/teradata.md`). If it exists, read it — it maps source-code signals to settings with rationale. If it does not exist, proceed using each setting's `helpText` as your only guide (general reasoning, fewer/weaker recommendations).

### Step 3: Sample the source

You do NOT need to read every file. To keep this cheap on large projects:
1. From the hint file's signal patterns (or, without hints, from setting names/help), grep `source/` for each signal, e.g. `grep -rIl -e 'PERIOD(' -e '.LOGON' source/`.
2. Open a representative sample — cap at ~20 files or ~200 KB total. Prefer files that matched signals plus a couple of the largest files.
3. Tell the user how many files you sampled out of the total (honest coverage, not "analyzed everything").

### Step 4: Build recommendations

For each catalog setting a signal supports, record:
- `longName` and the proposed value (for booleans: enable; for choice/text/int: the specific value).
- `currentValue` (from Step 1) if set.
- A one-line rationale grounded in what you found (e.g. "found `PERIOD(` in 3 files → split into begin/end").

Skip any setting whose `currentValue` already equals your proposal.

### Step 5: Confirm with the user

Present the recommendations as a table (Setting | Proposed | Current | Why), then ask via `ask_user_question` (`multiSelect = true`):

> "Which conversion settings should I apply? (You can select any subset, or none.)"
> - one option per recommended setting, labelled `--<longName> <value> — <short rationale>`

If there are no recommendations, tell the user the defaults look appropriate and return no flags.

### Step 6: Return flags to the caller

Turn each accepted setting into a CLI argument for `scai code convert`:
- Boolean settings: pass the presence flag only, e.g. `--comments`.
- Valued settings (choice/text/int/float/file): pass name + value, e.g. `--sessionMode Ansi`.

Hand the assembled flag string back to `convert` as `<SETTINGS_FLAGS>` (its Step 4 appends it to the convert command). Then return to the calling skill.

## Notes
- Recommend only; never run `scai code convert` from this skill.
- After conversion succeeds, `scai` auto-persists the accepted settings to `.scai/config/code-conversion-config.yaml`, so next run they show up as `currentValue`. You don't write that file.
