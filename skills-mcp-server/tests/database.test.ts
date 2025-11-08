/**
 * Tests for SkillsDatabase
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { SkillsDatabase } from '../src/database.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('SkillsDatabase', () => {
  let db: SkillsDatabase;
  let tempDir: string;
  let dbPath: string;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-test-'));
    dbPath = path.join(tempDir, 'test.db');
    db = new SkillsDatabase(dbPath);
  });

  afterEach(() => {
    db.close();
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  describe('updateRepositoryHash', () => {
    it('should insert new repository', () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      expect(repoId).toBeGreaterThan(0);

      const repos = db.getRepositories();
      expect(repos.length).toBe(1);
      expect(repos[0].url).toBe('https://github.com/test/repo');
      expect(repos[0].git_commit_hash).toBe('abc123');
    });

    it('should update existing repository', () => {
      const repoId1 = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      const repoId2 = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'def456'
      );

      expect(repoId1).toBe(repoId2);

      const repos = db.getRepositories();
      expect(repos.length).toBe(1);
      expect(repos[0].git_commit_hash).toBe('def456');
    });
  });

  describe('updateSkillHash', () => {
    it('should insert new skill', () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.updateSkillHash(repoId, {
        name: 'Test Skill',
        description: 'A test skill',
        relativePath: 'path/to/skill',
        skillPath: '/full/path/to/skill',
        repoName: 'test-repo',
        fileHash: 'hash123',
      });

      const skills = db.getSkillsByRepoId(repoId);
      expect(skills.length).toBe(1);
      expect(skills[0].skill_path).toBe('path/to/skill');
      expect(skills[0].file_hash).toBe('hash123');
      expect(skills[0].name).toBe('Test Skill');
      expect(skills[0].description).toBe('A test skill');
    });

    it('should update existing skill', () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.updateSkillHash(repoId, {
        name: 'Test Skill',
        description: 'A test skill',
        relativePath: 'path/to/skill',
        skillPath: '/full/path/to/skill',
        repoName: 'test-repo',
        fileHash: 'hash123',
      });
      
      db.updateSkillHash(repoId, {
        name: 'Test Skill Updated',
        description: 'Updated description',
        relativePath: 'path/to/skill',
        skillPath: '/full/path/to/skill',
        repoName: 'test-repo',
        fileHash: 'hash456',
      });

      const skills = db.getSkillsByRepoId(repoId);
      expect(skills.length).toBe(1);
      expect(skills[0].file_hash).toBe('hash456');
      expect(skills[0].name).toBe('Test Skill Updated');
    });
  });

  describe('hasChanges', () => {
    it('should return true when new repository added', () => {
      db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      expect(db.hasChanges()).toBe(true);
    });

    it('should return false after marking catalog generated', () => {
      db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.markCatalogGenerated();

      expect(db.hasChanges()).toBe(false);
    });

    it('should return true when repository updated after catalog generation', async () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.markCatalogGenerated();

      // Wait a bit to ensure timestamp difference
      await new Promise(resolve => setTimeout(resolve, 10));
      
      db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'def456'
      );

      expect(db.hasChanges()).toBe(true);
    });
  });

  describe('deleteRepository', () => {
    it('should delete repository and associated skills', () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.updateSkillHash(repoId, {
        name: 'Skill 1',
        description: 'First skill',
        relativePath: 'skill1',
        skillPath: '/path/skill1',
        repoName: 'test-repo',
        fileHash: 'hash1',
      });
      db.updateSkillHash(repoId, {
        name: 'Skill 2',
        description: 'Second skill',
        relativePath: 'skill2',
        skillPath: '/path/skill2',
        repoName: 'test-repo',
        fileHash: 'hash2',
      });

      db.deleteRepository('https://github.com/test/repo');

      expect(db.getRepositories().length).toBe(0);
      expect(db.getSkills().length).toBe(0);
    });
  });

  describe('deleteStaleSkills', () => {
    it('should remove skills not in current list', () => {
      const repoId = db.updateRepositoryHash(
        'https://github.com/test/repo',
        'test-repo',
        'abc123'
      );

      db.updateSkillHash(repoId, {
        name: 'Skill 1',
        description: 'First skill',
        relativePath: 'skill1',
        skillPath: '/path/skill1',
        repoName: 'test-repo',
        fileHash: 'hash1',
      });
      db.updateSkillHash(repoId, {
        name: 'Skill 2',
        description: 'Second skill',
        relativePath: 'skill2',
        skillPath: '/path/skill2',
        repoName: 'test-repo',
        fileHash: 'hash2',
      });
      db.updateSkillHash(repoId, {
        name: 'Skill 3',
        description: 'Third skill',
        relativePath: 'skill3',
        skillPath: '/path/skill3',
        repoName: 'test-repo',
        fileHash: 'hash3',
      });

      db.deleteStaleSkills(repoId, ['skill1', 'skill3']);

      const skills = db.getSkillsByRepoId(repoId);
      expect(skills.length).toBe(2);
      expect(skills.find(s => s.skill_path === 'skill2')).toBeUndefined();
    });
  });
});

