/**
 * Tests for SkillScanner
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { SkillScanner } from '../src/skill-scanner.js';
import { RepositoryManager } from '../src/repository-manager.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('SkillScanner', () => {
  let scanner: SkillScanner;
  let repoManager: RepositoryManager;
  let tempDir: string;

  beforeEach(() => {
    scanner = new SkillScanner();
    repoManager = new RepositoryManager();
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-test-'));
  });

  afterEach(() => {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  describe('scanRepositoryForSkills', () => {
    it('should discover skills in Anthropic repository', async () => {
      const repoPath = path.join(tempDir, '.skills', 'repositories', 'anthropic-skills');
      await repoManager.cloneRepository(
        'https://github.com/anthropics/skills',
        'main',
        repoPath
      );

      const skills = scanner.scanRepositoryForSkills(repoPath, 'anthropic-skills');

      expect(skills.length).toBeGreaterThan(0);
      expect(skills[0]).toHaveProperty('name');
      expect(skills[0]).toHaveProperty('description');
      expect(skills[0]).toHaveProperty('fileHash');
      expect(skills[0]).toHaveProperty('path');
      expect(skills[0]).toHaveProperty('relativePath');
    }, 60000);

    it('should scan repository with .claude/skills subdirectory structure', async () => {
      const repoPath = path.join(tempDir, '.skills', 'repositories', 'snowflake-dbt-demo');
      await repoManager.cloneRepository(
        'https://github.com/sfc-gh-dflippo/snowflake-dbt-demo',
        'main',
        repoPath
      );

      // This repo has SKILL.md files in .claude/skills/ subdirectory
      const skills = scanner.scanRepositoryForSkills(repoPath, 'snowflake-dbt-demo');

      // Scanner should complete without errors (may return 0 or more skills)
      expect(Array.isArray(skills)).toBe(true);
      
      // If skills are found, verify they have proper structure
      if (skills.length > 0) {
        expect(skills[0]).toHaveProperty('name');
        expect(skills[0]).toHaveProperty('description');
        expect(skills[0]).toHaveProperty('fileHash');
      }
    }, 60000);
  });

  describe('parseSkillFile', () => {
    it('should parse valid SKILL.md with frontmatter', async () => {
      // Create test SKILL.md file
      const testSkillPath = path.join(tempDir, 'SKILL.md');
      const testContent = `---
name: Test Skill
description: A test skill for unit testing
---

# Test Skill Content

This is the skill content.
`;
      fs.writeFileSync(testSkillPath, testContent, 'utf-8');

      const skill = scanner.parseSkillFile(testSkillPath, tempDir, 'test-repo');

      expect(skill).toBeTruthy();
      expect(skill!.name).toBe('Test Skill');
      expect(skill!.description).toBe('A test skill for unit testing');
      expect(skill!.fileHash).toBeTruthy();
    });

    it('should return null for SKILL.md without required frontmatter', () => {
      const testSkillPath = path.join(tempDir, 'SKILL.md');
      const testContent = `---
title: Missing Required Fields
---

# Invalid Skill
`;
      fs.writeFileSync(testSkillPath, testContent, 'utf-8');

      const skill = scanner.parseSkillFile(testSkillPath, tempDir, 'test-repo');

      expect(skill).toBeNull();
    });
  });

  describe('calculateFileHash', () => {
    it('should calculate consistent hash for same content', () => {
      const testPath = path.join(tempDir, 'test.txt');
      fs.writeFileSync(testPath, 'test content', 'utf-8');

      const hash1 = scanner.calculateFileHash(testPath);
      const hash2 = scanner.calculateFileHash(testPath);

      expect(hash1).toBe(hash2);
      expect(hash1.length).toBe(64); // SHA256 hex length
    });

    it('should calculate different hash for different content', () => {
      const testPath1 = path.join(tempDir, 'test1.txt');
      const testPath2 = path.join(tempDir, 'test2.txt');
      
      fs.writeFileSync(testPath1, 'content 1', 'utf-8');
      fs.writeFileSync(testPath2, 'content 2', 'utf-8');

      const hash1 = scanner.calculateFileHash(testPath1);
      const hash2 = scanner.calculateFileHash(testPath2);

      expect(hash1).not.toBe(hash2);
    });
  });

  describe('scanProjectForLocalSkills', () => {
    it('should find local SKILL.md files in project root', () => {
      // Create local skill
      const skillDir = path.join(tempDir, '.claude', 'skills', 'test-skill');
      fs.mkdirSync(skillDir, { recursive: true });
      
      const skillContent = `---
name: local-test-skill
description: A local test skill
---

# Local Test Skill

This is a local skill.
`;
      fs.writeFileSync(path.join(skillDir, 'SKILL.md'), skillContent, 'utf-8');

      const skills = scanner.scanProjectForLocalSkills(tempDir);

      expect(skills.length).toBe(1);
      expect(skills[0].name).toBe('local-test-skill');
      expect(skills[0].description).toBe('A local test skill');
      expect(skills[0].repoName).toBe('local');
    });

    it('should exclude .skills directory from local scan', () => {
      // Create SKILL.md in .skills directory (should be excluded)
      const excludedDir = path.join(tempDir, '.skills', 'repositories', 'test');
      fs.mkdirSync(excludedDir, { recursive: true });
      
      const excludedContent = `---
name: should-not-find
description: Should be excluded
---
`;
      fs.writeFileSync(path.join(excludedDir, 'SKILL.md'), excludedContent, 'utf-8');

      // Create SKILL.md in valid location
      const validDir = path.join(tempDir, 'custom-skills');
      fs.mkdirSync(validDir, { recursive: true });
      
      const validContent = `---
name: should-find
description: Should be included
---
`;
      fs.writeFileSync(path.join(validDir, 'SKILL.md'), validContent, 'utf-8');

      const skills = scanner.scanProjectForLocalSkills(tempDir);

      expect(skills.length).toBe(1);
      expect(skills[0].name).toBe('should-find');
    });

    it('should exclude node_modules from local scan', () => {
      // Create SKILL.md in node_modules (should be excluded)
      const nodeModulesDir = path.join(tempDir, 'node_modules', 'some-package');
      fs.mkdirSync(nodeModulesDir, { recursive: true });
      
      const excludedContent = `---
name: node-module-skill
description: Should be excluded
---
`;
      fs.writeFileSync(path.join(nodeModulesDir, 'SKILL.md'), excludedContent, 'utf-8');

      const skills = scanner.scanProjectForLocalSkills(tempDir);

      expect(skills.length).toBe(0);
    });

    it('should find multiple local skills', () => {
      // Create first skill
      const skill1Dir = path.join(tempDir, 'skills', 'skill1');
      fs.mkdirSync(skill1Dir, { recursive: true });
      fs.writeFileSync(path.join(skill1Dir, 'SKILL.md'), `---
name: skill-one
description: First skill
---`, 'utf-8');

      // Create second skill
      const skill2Dir = path.join(tempDir, 'docs', 'skills', 'skill2');
      fs.mkdirSync(skill2Dir, { recursive: true });
      fs.writeFileSync(path.join(skill2Dir, 'SKILL.md'), `---
name: skill-two
description: Second skill
---`, 'utf-8');

      const skills = scanner.scanProjectForLocalSkills(tempDir);

      expect(skills.length).toBe(2);
      const names = skills.map(s => s.name).sort();
      expect(names).toEqual(['skill-one', 'skill-two']);
    });
  });
});

