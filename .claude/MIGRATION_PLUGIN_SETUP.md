# Snowflake migration plugin — setup

This project uses the **Snowflake AIM migration plugin** (`snowflake-migration`) in Claude Code. It
provides migration skills, slash commands, session hooks, and an MCP server for assessment,
conversion, validation, and deployment.

A setup script installs the plugin from its upstream repo. Run the script once after you clone, and
again to update.

---

## Quick start

Needs `git`, Python 3.9 or later, and access to GitHub.

```bash
uv run .claude/setup_migration_plugin.py
```

Then restart Claude Code in this directory, or run `/reload-plugins`.

Run `/plugin` to verify. You must see `snowflake-migration@skills-dir` loaded. Then start work with
`/snowflake-migration:migrate`.

`uv` supplies its own interpreter. A plain interpreter works identically:

```bash
python .claude/setup_migration_plugin.py     # or python3
```

### What the script installs

The script downloads the plugin from
[`Snowflake-Labs/cortex-code-migrations`](https://github.com/Snowflake-Labs/cortex-code-migrations)
and installs it to `.claude/skills/snowflake-migration/`. It tracks the `preview` branch by default.
Use `--ref main` for the stable release. That install directory is the single path the script writes
in this repo.

Git tracks the installed plugin, so you choose whether to commit it. Commit it for a reproducible
environment, such as a demo or a shared branch: a new clone then needs no setup step, and everyone
runs an identical version. The cost is about 360 upstream files in each diff that changes them.
Leave it untracked and each developer runs the script instead.

Upstream ships its own licence. Check that licence before you redistribute the files.

For plugin documentation, see the
[SnowConvert migration skill](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/migration-skill/skill).

---

## Updating

Re-run the script, then reload:

```bash
uv run .claude/setup_migration_plugin.py
/reload-plugins
```

The script fetches the latest commit on the branch and reinstalls the plugin. Each run replaces the
whole install directory, so files removed upstream are also removed here.

### Options

```bash
# Print every action, then exit
uv run .claude/setup_migration_plugin.py --dry-run

# Track the stable branch instead of preview
uv run .claude/setup_migration_plugin.py --ref main

# Full option list
uv run .claude/setup_migration_plugin.py --help
```

---

## Session start behavior

The plugin runs a `SessionStart` hook on each session in this directory. The hook:

1. Installs [`uv`](https://docs.astral.sh/uv/) if it is missing.
2. Installs the **`scai` CLI** if it is missing, or runs `scai update` if it is present.
3. Disables the `scai` auto-update, because the hook manages updates.

This is expected behavior, not a misconfiguration. The MCP server ships inside the `scai` binary, so
`scai` must exist before the server can start. The first session takes about one extra minute. Later
sessions are quick. Logs go to `.claude/skills/snowflake-migration/logs/install-dependencies.log`.

A `UserPromptSubmit` hook also runs once per session. It tells the agent whether a migration project
already exists here. It looks for `.scai/config/project.yml`.

To stop the hook from installing tools globally, disable the plugin in `/plugin`. The migration
skills do not work without `scai`.

---

## Troubleshooting

| Symptom                                                                         | Fix                                                                                              |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `/plugin` does not list `snowflake-migration@skills-dir`, or a skill is missing | Re-run the script, then `/reload-plugins`.                                                       |
| Listed but not loaded                                                           | Trust the workspace again, or enable the plugin in `/plugin`.                                    |
| `clone failed`                                                                  | Check network and GitHub access.                                                                 |
| `could not fetch 'preview'`                                                     | Branch name error, or no network. Valid branches are `preview` and `main`.                       |
| MCP tools unavailable, `⏸ Pending approval`                                     | The workspace is not trusted. See [MCP server pending approval](#mcp-server-pending-approval).   |
| MCP tools unavailable, no pending status                                        | `scai` can still be installing. Check `logs/install-dependencies.log`, then restart the session. |
| Hook errors about permissions                                                   | Re-run the script. The copy preserves the executable bit that git records upstream.              |

### MCP server pending approval

Symptom — skills and slash commands work, but MCP tools are missing:

```console
$ claude mcp list
plugin:snowflake-migration:mcp: scai mcp run - ⏸ Pending approval (run `claude` to approve)
```

The install is not broken. This directory is not trusted, and a project-scope plugin does not
connect its MCP server until you trust the directory. `/reload-plugins` does not create trust. Only
a session start does.

Fix, in order of preference:

1. **Restart Claude Code in this directory** and accept the workspace trust dialog. The server
   connects at the next session start.
2. **Enable the server in `/mcp`** if the panel offers `plugin:snowflake-migration:mcp`.
3. **Trust without a dialog.** Set this in `~/.claude.json`, your own config, not the repo:

   ```json
   { "projects": { "/absolute/path/to/this/repo": { "hasTrustDialogAccepted": true } } }
   ```

   Use option 3 only for a repo you trust. It skips the security prompt.

Approval writes the decision to `.claude/settings.local.json`:

```json
{ "enabledMcpjsonServers": ["plugin:snowflake-migration:mcp"] }
```

That file is gitignored. Each developer approves once per machine, and no approval is committed for
other people.
