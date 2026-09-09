---
name: register-code-units
description: Register source code into the migration project — either by extracting from a live database or importing local SQL files.
license: Proprietary. See License-Skills for complete terms
---

# Register Source Code

## On Entry

Tell the user:
> **Register Source Code** — We need to get your source database objects into the project so they can be converted. You can extract them directly from your database or import local SQL files.

## Step 1: Ask How to Register

The setup machine asks this at `chooseCodeSource` and persists the answer, so
read `code_source` from the session first and do not ask twice. Only when it is
unset — this skill can be entered outside setup — ask:

> "How would you like to add source code?"
> 1. **Extract from database** - Pull DDL/code from a connected source database
> 2. **I already have my code locally** - Import SQL files from a local directory

## Step 2: Route

- `code_source=extract`, or **Extract from database** → Load `extract-code-units/SKILL.md`
- `code_source=local`, or **I already have my code locally** → Load `add-code-units/SKILL.md`

Extracting needs a source connection; importing local files does not. Don't
offer to set one up here — the machine routes through
`../setup/configure-source-connection.md` before this task on the extract path,
and testing and data migration ask for it themselves when they need it.

## Sub-Skills

| Sub-skill | Location |
|-----------|----------|
| extract-code-units | `extract-code-units/SKILL.md` |
| add-code-units | `add-code-units/SKILL.md` |
