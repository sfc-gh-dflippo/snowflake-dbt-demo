# Snowflake migration plugin setup

This project uses the Snowflake AIM migration plugin (`snowflake-migration`) in Claude Code. The
plugin supplies the migration skills, the slash commands, the session hooks, and the MCP server. The
MCP server does assessment, conversion, validation, and deployment.

A setup script installs the plugin from its upstream repository. Run the script one time after you
clone this repository. Run the script again to install a newer version.

---

## Quick start

You must have `git`, Python 3.9 or later, and access to GitHub.

```bash
uv run .claude/setup_migration_plugin.py
```

Then restart Claude Code in this directory.

To confirm the result, run `/plugin`. The loaded list must show `snowflake-migration@skills-dir`.
Then start the work with `/snowflake-migration:migrate`.

The script uses `uv` because `uv` supplies its own interpreter. A plain interpreter gives the same
result:

```bash
python .claude/setup_migration_plugin.py     # or python3
```

### Installed files

The script clones the plugin from
[`Snowflake-Labs/cortex-code-migrations`](https://github.com/Snowflake-Labs/cortex-code-migrations).
It installs the plugin in `.claude/skills/snowflake-migration/`. The script tracks the `preview`
branch by default. To get the stable release, add `--ref main`. The script writes to this one
directory only.

For plugin documentation, refer to the
[SnowConvert migration skill](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/user-guide/snowconvert/migration-skill/skill).

---

## Updates

Run the same script. Then restart Claude Code in this directory:

```bash
uv run .claude/setup_migration_plugin.py
```

The script gets the most recent commit on the branch. It then installs the plugin again. Each run
replaces the complete install directory. The script also removes the files that upstream deleted.

### Options

```bash
# Show the actions, but do not do them
uv run .claude/setup_migration_plugin.py --dry-run

# Track the stable branch in place of preview
uv run .claude/setup_migration_plugin.py --ref main

# Show all the options
uv run .claude/setup_migration_plugin.py --help
```

---

## Session start behavior

The plugin has a `SessionStart` hook. The hook runs in each session in this directory. The hook does
these steps:

1. It installs [`uv`](https://docs.astral.sh/uv/), if `uv` is absent.
2. It installs the `scai` CLI, if `scai` is absent. If `scai` is present, it runs `scai update`.
3. It disables the `scai` auto-update function. The hook controls the updates.

This behavior is correct. It is not a configuration error. The `scai` binary contains the MCP
server. Thus `scai` must be present before the server can start. The first session needs
approximately one more minute. Subsequent sessions are faster. The hook writes the log to
`.claude/skills/snowflake-migration/logs/install-dependencies.log`.

The plugin also has a `UserPromptSubmit` hook. This hook runs one time in each session. It looks for
`.scai/config/project.yml`. It then tells the agent if a migration project is present in this
directory.

To prevent the global installation of the tools, disable the plugin in `/plugin`. Attention: the
migration skills do not function without `scai`.

---

## Troubleshooting

| Symptom                                                                        | Solution                                                                                                            |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `/plugin` does not show `snowflake-migration@skills-dir`, or a skill is absent | Run the script again. Then restart Claude Code.                                                                     |
| The plugin is in the list, but it is not loaded                                | Set the trust for the workspace again, or enable the plugin in `/plugin`.                                           |
| `clone failed`                                                                 | Make sure that you have network access and GitHub access.                                                           |
| `could not fetch 'preview'`                                                    | The branch name is incorrect, or the network is unavailable. The permitted branches are `preview` and `main`.       |
| The MCP tools are absent, and the status is `⏸ Pending approval`               | The workspace is not trusted. Refer to [Pending approval for the MCP server](#pending-approval-for-the-mcp-server). |
| The MCP tools are absent, and there is no pending status                       | The installation of `scai` can be in progress. Examine `logs/install-dependencies.log`. Then restart the session.   |
| The hook shows a permissions error                                             | Run the script again. The copy operation keeps the executable bit from the upstream repository.                     |

### Pending approval for the MCP server

The skills and the slash commands function correctly, but the MCP tools are absent:

```console
$ claude mcp list
plugin:snowflake-migration:mcp: scai mcp run - ⏸ Pending approval (run `claude` to approve)
```

The installation is correct. This directory is not trusted. A project-scope plugin does not connect
its MCP server until the directory is trusted. Only a session start sets the trust.

Restart Claude Code in this directory. Accept the workspace trust dialog. The restart also runs the
`SessionStart` hook. The server connects at the next session start.

The trust decision goes to `.claude/settings.local.json`:

```json
{ "enabledMcpjsonServers": ["plugin:snowflake-migration:mcp"] }
```
