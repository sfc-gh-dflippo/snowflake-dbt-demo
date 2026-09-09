# Orchestration SQL: Block Tags & Task Hierarchy

## Tag Format

SnowConvert's ETL orchestration output uses SQL comment tags to delimit tasks inside a generated `.sql` file. There are three tag types:

| Tag | Pattern | Meaning |
|-----|---------|---------|
| **Start block** | `---- Start block '<FullName>'` | Opens a **container** task (may hold inner tasks) |
| **Start** | `---- Start '<FullName>'` | Opens a **non-container** (leaf) task |
| **End block** | `---- End block '<FullName>'` | Closes a container task |

Non-container tasks (`Start`) have **no** closing tag — they end when the next tag appears or the parent block ends.

`<FullName>` is a backslash-separated path like `Package\SequenceContainer\ExecuteSQLTask`.

## Replacement Boundaries

When replacing element content in the orchestration SQL:

- **Container** (`---- Start block '<name>'`): replace everything between the `---- Start block` and matching `---- End block` tags. Preserve both boundary tags.
- **Non-container** (`---- Start '<name>'`): replace everything from the `---- Start` tag up to (but not including) the next `---- Start`, `---- Start block`, or `---- End block` tag. Preserve the Start tag.

## Task Types

| Type | Tag Pattern | Description |
|------|------------|-------------|
| **container** | `Start block` / `End block` pair | Wraps other tasks |
| **non-container** | `Start` only (no closing tag) | Leaf task with actual SQL logic |
| **auto-setup** | No tags at all | `CREATE TASK`/`CREATE PROCEDURE` with no inner structure (e.g., variable initialization boilerplate) |
