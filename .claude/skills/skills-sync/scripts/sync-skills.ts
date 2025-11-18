#!/usr/bin/env node
/**
 * Skills Sync Script - Sync AI agent skills from GitHub repositories using Git.
 * Uses git clone/pull for efficiency. Local SKILL.md files take precedence.
 * Configure repositories in .claude/skills/repos.txt (created automatically).
 * Zero external dependencies - only uses Node.js built-ins.
 */

import * as fs from "fs";
import * as path from "path";
import * as child_process from "child_process";
import { promisify } from "util";

const exec = promisify(child_process.exec);

function findProjectRoot(): string {
  let current = path.dirname(new URL(import.meta.url).pathname);

  // Walk up directory tree (max 10 levels)
  for (let i = 0; i < 10; i++) {
    // Check for project root indicators
    if (fs.existsSync(path.join(current, ".claude", "skills", "repos.txt"))) {
      return current;
    }
    if (fs.existsSync(path.join(current, ".git"))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) {
      // Reached filesystem root
      break;
    }
    current = parent;
  }

  // Fallback to current working directory
  return process.cwd();
}

// Configuration
const PROJECT_ROOT = findProjectRoot();
const SKILLS_DIR = path.join(PROJECT_ROOT, ".claude", "skills", "repositories");
const CONFIG_FILE = path.join(PROJECT_ROOT, ".claude", "skills", "repos.txt");
const AGENTS_MD = path.join(PROJECT_ROOT, "AGENTS.md");
const START_MARKER = "<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->";
const END_MARKER = "<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->";

interface Skill {
  name: string;
  path: string;
  description: string;
  source: string;
}

async function checkGitInstalled(): Promise<void> {
  try {
    await exec("git --version");
  } catch (error) {
    console.error("Error: Git is not installed. Please install Git.");
    process.exit(1);
  }
}

function ensureGitignore(): void {
  const skillsDir = path.join(PROJECT_ROOT, ".claude", "skills");
  const gitignorePath = path.join(skillsDir, ".gitignore");
  const gitignoreEntry = "repositories/";

  // Ensure .claude/skills directory exists
  fs.mkdirSync(skillsDir, { recursive: true });

  if (fs.existsSync(gitignorePath)) {
    const content = fs.readFileSync(gitignorePath, "utf-8");
    // Check if entry already exists
    if (
      !content.includes(gitignoreEntry) &&
      !content.includes("repositories")
    ) {
      // Add entry with a comment
      let newContent = content;
      if (!content.endsWith("\n")) {
        newContent += "\n";
      }
      newContent +=
        "# Cloned skill repositories (managed by sync-skills script)\n";
      newContent += `${gitignoreEntry}\n`;
      fs.writeFileSync(gitignorePath, newContent);
      console.log("  Added repositories/ to .claude/skills/.gitignore");
    }
  } else {
    // Create new .gitignore in .claude/skills/
    let content =
      "# Cloned skill repositories (managed by sync-skills script)\n";
    content += `${gitignoreEntry}\n`;
    fs.writeFileSync(gitignorePath, content);
    console.log("  Created .claude/skills/.gitignore");
  }
}

function readRepoList(): string[] {
  if (!fs.existsSync(CONFIG_FILE)) {
    fs.mkdirSync(path.dirname(CONFIG_FILE), { recursive: true });
    fs.writeFileSync(CONFIG_FILE, "https://github.com/anthropics/skills\n");
  }

  return fs
    .readFileSync(CONFIG_FILE, "utf-8")
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"));
}

function urlToRepoName(url: string): string {
  const urlObj = new URL(url);
  const hostname = urlObj.hostname.replace(/\./g, "-");
  const pathParts = urlObj.pathname
    .replace(/^\//, "")
    .replace(/\.git$/, "")
    .split("/");
  return `${hostname}/${pathParts.join("-")}`;
}

async function getCurrentCommit(repoPath: string): Promise<string | null> {
  try {
    const { stdout } = await exec("git rev-parse HEAD", { cwd: repoPath });
    return stdout.trim();
  } catch {
    return null;
  }
}

async function cloneOrPullRepo(
  url: string,
  targetPath: string,
): Promise<{ changed: boolean; commit: string }> {
  if (fs.existsSync(path.join(targetPath, ".git"))) {
    // Repo exists, pull
    const oldCommit = await getCurrentCommit(targetPath);
    await exec("git pull --quiet", { cwd: targetPath });
    const newCommit = await getCurrentCommit(targetPath);
    const changed = oldCommit !== newCommit;

    if (changed) {
      console.log(
        `  Updated: ${oldCommit?.slice(0, 7)} → ${newCommit?.slice(0, 7)}`,
      );
    } else {
      console.log(`  No changes`);
    }

    return { changed, commit: newCommit! };
  } else {
    // Clone new repo
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    await exec(`git clone --depth 1 "${url}" "${targetPath}"`);
    const commit = await getCurrentCommit(targetPath);
    console.log(`  Cloned: ${commit?.slice(0, 7)}`);
    return { changed: true, commit: commit! };
  }
}

function parseFrontmatter(
  content: string,
): { name?: string; description?: string } | null {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!match || !match[1]) return null;

  const frontmatter = match[1];
  const data: any = {};

  for (const line of frontmatter.split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line
        .slice(colonIdx + 1)
        .trim()
        .replace(/^["']|["']$/g, "");
      data[key] = value;
    }
  }

  return data;
}

function scanAllSkills(
  projectRoot: string,
  repoPaths: Record<string, string>,
): {
  localSkills: Record<string, Skill>;
  repoSkills: Record<string, Skill>;
} {
  const localSkills: Record<string, Skill> = {};
  const repoSkills: Record<string, Skill> = {};
  const excludeDirs = new Set(["node_modules", ".git", "venv", "__pycache__"]);
  const repositoriesDir = SKILLS_DIR;

  function scan(dir: string): void {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });

      for (const entry of entries) {
        if (excludeDirs.has(entry.name)) continue;

        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
          scan(fullPath);
        } else if (entry.name === "SKILL.md") {
          try {
            const content = fs.readFileSync(fullPath, "utf-8");
            const data = parseFrontmatter(content);
            if (!data?.name || !data?.description) continue;

            const relPath = path.relative(projectRoot, fullPath);

            // Check if this skill is inside .claude/skills/repositories/
            const isInRepositories = fullPath.startsWith(
              repositoriesDir + path.sep,
            );

            if (isInRepositories) {
              // Find which repo it belongs to
              let repoName: string | null = null;
              for (const [rname, rpath] of Object.entries(repoPaths)) {
                if (fullPath.startsWith(rpath + path.sep)) {
                  repoName = rname;
                  break;
                }
              }

              if (repoName) {
                repoSkills[data.name] = {
                  name: data.name,
                  path: relPath,
                  description: data.description,
                  source: repoName,
                };
              }
            } else {
              // It's a local skill (anywhere else in the project)
              localSkills[data.name] = {
                name: data.name,
                path: relPath,
                description: data.description,
                source: "local",
              };
            }
          } catch (error) {
            console.warn(`Warning: Failed to parse ${fullPath}`);
          }
        }
      }
    } catch (error) {
      // Ignore directories we can't read
    }
  }

  scan(projectRoot);
  return { localSkills, repoSkills };
}

function formatSkillsSection(
  localSkills: Record<string, Skill>,
  repoSkills: Record<string, Skill>,
): string {
  const lines: string[] = [];
  lines.push("## MCP-Managed Skills\n\n");
  lines.push(
    "This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.\n\n",
  );
  lines.push("# Skills\n\n");
  lines.push("**What are Skills?**\n\n");
  lines.push(
    "Skills are structured instruction sets that enhance AI assistant capabilities " +
      "for specific domains or tasks. Each skill is a folder containing:\n\n",
  );
  lines.push("- **SKILL.md** - Core instructions and guidelines\n");
  lines.push("- **references/** - Detailed documentation and examples\n");
  lines.push("- **scripts/** - Helper scripts and templates\n");
  lines.push("- **config/** - Configuration files\n\n");
  lines.push(
    "Skills provide domain-specific knowledge, best practices, " +
      "code templates, and troubleshooting strategies.\n\n",
  );
  lines.push("**Key Features:**\n\n");
  lines.push(
    "- Skills can be enabled `[x]` or disabled `[ ]` individually\n\n",
  );
  lines.push("**Available Skills:**\n\n");

  // Local skills
  if (Object.keys(localSkills).length > 0) {
    lines.push("### Local Skills\n\n");
    for (const name of Object.keys(localSkills).sort()) {
      const skill = localSkills[name];
      if (skill) {
        lines.push(
          `- [x] **[${name}](${skill.path})** - ${skill.description}\n`,
        );
      }
    }
    lines.push("\n");
  }

  // Repo skills grouped by source
  const repoGroups: Record<string, Skill[]> = {};
  for (const [name, skill] of Object.entries(repoSkills)) {
    if (!(name in localSkills)) {
      // Skip overridden
      if (!repoGroups[skill.source]) {
        repoGroups[skill.source] = [];
      }
      repoGroups[skill.source]?.push(skill);
    }
  }

  for (const repoName of Object.keys(repoGroups).sort()) {
    lines.push(`### ${repoName}\n\n`);
    const group = repoGroups[repoName];
    if (group) {
      for (const skill of group.sort((a, b) => a.name.localeCompare(b.name))) {
        lines.push(
          `- [x] **[${skill.name}](${skill.path})** - ${skill.description}\n`,
        );
      }
    }
    lines.push("\n");
  }

  return lines.join("");
}

function updateAgentsMd(content: string): void {
  if (!fs.existsSync(AGENTS_MD)) {
    const template =
      "# AI Agent Configuration\n\nContext and guidelines for AI coding agents.\n\n";
    fs.writeFileSync(AGENTS_MD, template);
  }

  let agentsContent = fs.readFileSync(AGENTS_MD, "utf-8");
  const startIdx = agentsContent.indexOf(START_MARKER);
  const endIdx = agentsContent.indexOf(END_MARKER);

  if (startIdx === -1 || endIdx === -1) {
    if (!agentsContent.endsWith("\n")) agentsContent += "\n";
    agentsContent += `\n${START_MARKER}\n${content}\n${END_MARKER}\n`;
  } else {
    const before = agentsContent.slice(0, startIdx + START_MARKER.length);
    const after = agentsContent.slice(endIdx);
    agentsContent = `${before}\n${content}\n${after}`;
  }

  fs.writeFileSync(AGENTS_MD, agentsContent);
}

async function main(): Promise<void> {
  await checkGitInstalled();
  ensureGitignore();

  console.log("Reading repository configuration...");
  const repos = readRepoList();
  console.log(`Configured repositories: ${repos.length}`);

  console.log("\nSyncing repositories...");
  const repoPaths: Record<string, string> = {};
  for (const url of repos) {
    const repoName = urlToRepoName(url);
    console.log(`  ${repoName}:`);
    const targetPath = path.join(SKILLS_DIR, repoName);
    await cloneOrPullRepo(url, targetPath);
    repoPaths[repoName] = targetPath;
  }

  console.log("\nScanning all SKILL.md files...");
  const { localSkills, repoSkills: allRepoSkills } = scanAllSkills(
    PROJECT_ROOT,
    repoPaths,
  );
  console.log(`  Found ${Object.keys(localSkills).length} local skills`);
  console.log(`  Found ${Object.keys(allRepoSkills).length} repository skills`);

  const overridden = Object.keys(localSkills).filter(
    (name) => name in allRepoSkills,
  );
  if (overridden.length > 0) {
    console.log(
      `\n  Local skills override ${overridden.length} repo skills: ${overridden.sort().join(", ")}`,
    );
  }

  console.log("\nUpdating AGENTS.md...");
  const content = formatSkillsSection(localSkills, allRepoSkills);
  updateAgentsMd(content);

  const uniqueRepoSkills = Object.keys(allRepoSkills).filter(
    (name) => !(name in localSkills),
  );
  const total = Object.keys(localSkills).length + uniqueRepoSkills.length;
  console.log(`\n✓ Synced ${total} total skills to AGENTS.md`);
  console.log(
    `  (${Object.keys(localSkills).length} local, ${uniqueRepoSkills.length} from repos)`,
  );
}

main().catch((error) => {
  console.error("Error:", error.message);
  process.exit(1);
});
