---
name: confirm-project-dir
description: Confirm the project directory with the user before initialization
license: Proprietary. See License-Skills for complete terms
---

# Confirm Project Directory

Ask the user:

> "Set up the migration project in `<project_dir>`?"
>
> 1. **Yes, use it** — Proceed with the current directory.
> 2. **Use a different location** — I'll ask for a path.

**If option 1:**

```
configure(project_dir_confirmed=true)
```

**If option 2:** Ask the user: "What path should I use for the migration project?" Then call:

```
configure(project_dir=<path>)
```

The machine will re-check and re-confirm the new path.
