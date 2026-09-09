---
name: validate-empty-dir
description: Handle a non-empty project directory — offer a subfolder or a custom path
license: Proprietary. See License-Skills for complete terms
---

# Validate Empty Directory

The current directory is not empty and cannot be used to initialize a new migration project.

Ask the user directly — do not describe or explain what is in the directory:

> "The current directory isn't empty, so the migration project can't be initialized here. Where should it go?"
>
> 1. **Create a `migration` subfolder** — Use `<project_dir>/migration`.
> 2. **Use a different location** — I'll ask for a path.

**If option 1:**

```
configure(project_dir=<project_dir>/migration, project_dir_confirmed=true)
```

**If option 2:** Ask the user: "What path should I use for the migration project?" Then call:

```
configure(project_dir=<path>, project_dir_confirmed=true)
```

The machine will re-check the new path automatically after either call.
