/**
 * Integration tests to verify complete skill discovery from multiple repositories
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { SkillScanner } from '../src/skill-scanner.js';
import { SkillsDatabase } from '../src/database.js';
import { AgentsMdGenerator } from '../src/agents-md-generator.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('Integration: Multi-Repository Skill Discovery', () => {
  let tempDir: string;
  let scanner: SkillScanner;
  let db: SkillsDatabase;
  let agentsMdGenerator: AgentsMdGenerator;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-integration-'));
    scanner = new SkillScanner();
    db = new SkillsDatabase(path.join(tempDir, 'test.db'));
    agentsMdGenerator = new AgentsMdGenerator();
  });

  afterEach(() => {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  it('should discover skills from .claude/skills directories in cloned repos', () => {
    // Create a mock repository structure with .claude/skills
    const repoRoot = path.join(tempDir, '.skills', 'repositories', 'test-repo');
    const claudeSkillsDir = path.join(repoRoot, '.claude', 'skills', 'test-skill');
    fs.mkdirSync(claudeSkillsDir, { recursive: true });

    // Create a SKILL.md file in .claude (should be found)
    const skillContent = `---
name: test-skill
description: A test skill in .claude directory within a cloned repo
---

# Test Skill

This skill is inside a cloned repository.
`;
    fs.writeFileSync(path.join(claudeSkillsDir, 'SKILL.md'), skillContent, 'utf-8');

    // Scan the repository - should find the skill in .claude
    const skills = scanner.scanRepositoryForSkills(repoRoot, 'test-repo');

    expect(skills.length).toBe(1);
    expect(skills[0].name).toBe('test-skill');
    expect(skills[0].relativePath).toContain('.claude/skills/test-skill/SKILL.md');
  });

  it('should discover skills from multiple nested directories (including .claude)', () => {
    // Create multiple skill directories
    const repoRoot = path.join(tempDir, '.skills', 'repositories', 'multi-repo');
    
    // Create skills in .claude/skills (should be found)
    const claudeSkills = [
      { name: 'skill-1', dir: '.claude/skills/skill-1' },
      { name: 'skill-2', dir: '.claude/skills/skill-2' },
    ];

    // Create skills in regular directories (should also be found)
    const regularSkills = [
      { name: 'skill-3', dir: 'skills/skill-3' },
      { name: 'skill-4', dir: 'my-skills/skill-4' },
    ];

    for (const skill of [...claudeSkills, ...regularSkills]) {
      const skillDir = path.join(repoRoot, skill.dir);
      fs.mkdirSync(skillDir, { recursive: true });
      
      const skillContent = `---
name: ${skill.name}
description: Description for ${skill.name}
---

# ${skill.name}
`;
      fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent, 'utf-8');
    }

    // Scan the repository - should find ALL skills including those in .claude
    const skills = scanner.scanRepositoryForSkills(repoRoot, 'multi-repo');

    expect(skills.length).toBe(4);
    expect(skills.map(s => s.name).sort()).toEqual(['skill-1', 'skill-2', 'skill-3', 'skill-4']);
  });

  it('should skip only technical directories (.git, .github, node_modules)', () => {
    const repoRoot = path.join(tempDir, '.skills', 'repositories', 'skip-test');
    
    // Create skills in allowed directories (including .claude and .hidden)
    const allowedDirs = [
      'skills/allowed-1',
      'my-skills/allowed-2',
      '.claude/skills/allowed-3',
      '.skills/allowed-4',
      '.hidden/allowed-5',
    ];

    // Create skills in technical directories (should be skipped)
    const skippedDirs = [
      '.git/skills/skipped-1',
      '.github/skills/skipped-2',
      'node_modules/skills/skipped-3',
    ];

    for (const dir of [...allowedDirs, ...skippedDirs]) {
      const skillDir = path.join(repoRoot, dir);
      fs.mkdirSync(skillDir, { recursive: true });
      
      const skillName = path.basename(dir);
      const skillContent = `---
name: ${skillName}
description: Skill in ${dir}
---

# ${skillName}
`;
      fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent, 'utf-8');
    }

    // Scan the repository
    const skills = scanner.scanRepositoryForSkills(repoRoot, 'skip-test');

    // Should find all skills except those in .git, .github, node_modules
    expect(skills.length).toBe(5);
    const names = skills.map(s => s.name).sort();
    expect(names).toEqual(['allowed-1', 'allowed-2', 'allowed-3', 'allowed-4', 'allowed-5']);
  });

  it('should update AGENTS.md with skills from multiple repositories', () => {
    // Create AGENTS.md with markers
    const agentsMdPath = path.join(tempDir, 'AGENTS.md');
    fs.writeFileSync(agentsMdPath, `# Agent Instructions

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
`, 'utf-8');

    // Add two repositories to database
    const repo1Id = db.updateRepositoryHash('https://github.com/org/repo1', 'repo1', 'hash1');
    const repo2Id = db.updateRepositoryHash('https://github.com/org/repo2', 'repo2', 'hash2');

    // Add skills from repo1
    db.updateSkillHash(repo1Id, {
      name: 'skill-a',
      description: 'Skill A from repo1',
      path: '/path/to/skill-a/SKILL.md',
      relativePath: 'skills/skill-a/SKILL.md',
      repoName: 'repo1',
      fileHash: 'hash-a',
    }, 1);

    db.updateSkillHash(repo1Id, {
      name: 'skill-b',
      description: 'Skill B from repo1',
      path: '/path/to/skill-b/SKILL.md',
      relativePath: 'skills/skill-b/SKILL.md',
      repoName: 'repo1',
      fileHash: 'hash-b',
    }, 1);

    // Add skills from repo2
    db.updateSkillHash(repo2Id, {
      name: 'skill-c',
      description: 'Skill C from repo2',
      path: '/path/to/skill-c/SKILL.md',
      relativePath: '.claude/skills/skill-c/SKILL.md',
      repoName: 'repo2',
      fileHash: 'hash-c',
    }, 1);

    // Update AGENTS.md
    const allSkills = db.getAllSkills();
    const allRepos = db.getAllRepositories();
    agentsMdGenerator.updateAgentsMdWithSkills(tempDir, allSkills, allRepos, []);

    // Verify AGENTS.md content
    const content = fs.readFileSync(agentsMdPath, 'utf-8');
    
    expect(content).toContain('### repo1');
    expect(content).toContain('### repo2');
    expect(content).toContain('skill-a');
    expect(content).toContain('skill-b');
    expect(content).toContain('skill-c');
    expect(content).toContain('Skill A from repo1');
    expect(content).toContain('Skill C from repo2');
    
    // Verify it's grouped by repository
    const repo1Index = content.indexOf('### repo1');
    const repo2Index = content.indexOf('### repo2');
    const skillAIndex = content.indexOf('skill-a');
    const skillCIndex = content.indexOf('skill-c');
    
    expect(skillAIndex).toBeGreaterThan(repo1Index);
    expect(skillCIndex).toBeGreaterThan(repo2Index);
  });

  it('should count total skills correctly across repositories', () => {
    const repo1Id = db.updateRepositoryHash('https://github.com/org/repo1', 'repo1', 'hash1');
    const repo2Id = db.updateRepositoryHash('https://github.com/org/repo2', 'repo2', 'hash2');

    // Add 3 skills to repo1
    for (let i = 1; i <= 3; i++) {
      db.updateSkillHash(repo1Id, {
        name: `repo1-skill-${i}`,
        description: `Skill ${i} from repo1`,
        path: `/path/skill-${i}/SKILL.md`,
        relativePath: `skills/skill-${i}/SKILL.md`,
        repoName: 'repo1',
        fileHash: `hash-1-${i}`,
      }, 1);
    }

    // Add 2 skills to repo2
    for (let i = 1; i <= 2; i++) {
      db.updateSkillHash(repo2Id, {
        name: `repo2-skill-${i}`,
        description: `Skill ${i} from repo2`,
        path: `/path/skill-${i}/SKILL.md`,
        relativePath: `.claude/skills/skill-${i}/SKILL.md`,
        repoName: 'repo2',
        fileHash: `hash-2-${i}`,
      }, 1);
    }

    const allSkills = db.getAllSkills();
    expect(allSkills.length).toBe(5);

    const skillCountByRepo = db.getSkillCountByRepo();
    expect(skillCountByRepo.get(repo1Id)).toBe(3);
    expect(skillCountByRepo.get(repo2Id)).toBe(2);
  });
});

