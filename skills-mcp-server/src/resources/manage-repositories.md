# Managing Skills Repositories

## Add a Repository

To add a new GitHub repository to sync skills from:

1. **Edit `.skills/repos.txt`** in the project root and add the repository URL:
   ```text
   https://github.com/anthropics/skills
   https://github.com/your-org/your-skills-repo
   ```

2. **Run the sync script** to download and integrate the new repository:
   ```bash
   python3 sync-skills.py
   ```

## Remove a Repository

To remove a GitHub repository from skills syncing:

1. **Edit `.skills/repos.txt`** and delete or comment out the repository URL:
   ```text
   # https://github.com/old-repo/unwanted-skills
   ```

2. **Run the sync script** to update AGENTS.md:
   ```bash
   python3 sync-skills.py
   ```

3. **Clean up (optional)** - Delete the repository directory:
   ```bash
   rm -rf .skills/repositories/github-com/old-repo-unwanted-skills
   ```

## Configuration Format

- One repository URL per line
- Lines starting with `#` are comments
- HTTP or HTTPS URLs supported
- Private repos require Git credentials configured

## Example Configuration

```text
# Official Anthropic skills
https://github.com/anthropics/skills

# Custom organization skills
https://github.com/myorg/custom-skills

# Personal skills repository
https://github.com/myusername/my-skills
```

## What the Sync Script Does

The sync script will:
1. Clone new repositories to `.skills/repositories/`
2. Pull updates for existing repositories
3. Scan for SKILL.md files (local and remote)
4. Apply local skill precedence
5. Update AGENTS.md with the organized skills list

