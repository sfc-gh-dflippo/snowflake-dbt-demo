/**
 * Tests for RepositoryManager
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { RepositoryManager } from '../src/repository-manager.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('RepositoryManager', () => {
  let repoManager: RepositoryManager;
  let tempDir: string;

  beforeEach(() => {
    repoManager = new RepositoryManager();
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skills-test-'));
  });

  afterEach(() => {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  describe('getRepoNameFromUrl', () => {
    it('should extract repository name from GitHub URL', () => {
      const name = repoManager.getRepoNameFromUrl('https://github.com/anthropics/skills');
      expect(name).toContain('anthropics-skills');
    });

    it('should handle URLs with .git suffix', () => {
      const name = repoManager.getRepoNameFromUrl('https://github.com/user/repo.git');
      expect(name).toContain('user-repo');
    });

    it('should create unique subdirectories for different servers', () => {
      const github = repoManager.getRepoNameFromUrl('https://github.com/user/repo');
      const gitlab = repoManager.getRepoNameFromUrl('https://gitlab.com/user/repo');
      expect(github).not.toBe(gitlab);
    });
  });

  describe('cloneRepository', () => {
    it('should clone Anthropic skills repository', async () => {
      const repoPath = path.join(tempDir, 'anthropic-skills');
      
      await repoManager.cloneRepository(
        'https://github.com/anthropics/skills',
        'main',
        repoPath
      );

      expect(fs.existsSync(repoPath)).toBe(true);
      expect(fs.existsSync(path.join(repoPath, '.git'))).toBe(true);
    }, 60000);

    it('should clone snowflake-dbt-demo repository', async () => {
      const repoPath = path.join(tempDir, 'snowflake-dbt-demo');
      
      await repoManager.cloneRepository(
        'https://github.com/sfc-gh-dflippo/snowflake-dbt-demo',
        'main',
        repoPath
      );

      expect(fs.existsSync(repoPath)).toBe(true);
      expect(fs.existsSync(path.join(repoPath, '.claude'))).toBe(true);
    }, 60000);
  });

  describe('getCurrentCommitHash', () => {
    it('should get commit hash from cloned repository', async () => {
      const repoPath = path.join(tempDir, 'test-repo');
      
      await repoManager.cloneRepository(
        'https://github.com/anthropics/skills',
        'main',
        repoPath
      );

      const hash = await repoManager.getCurrentCommitHash(repoPath);
      expect(hash).toBeTruthy();
      expect(hash.length).toBeGreaterThan(0);
    }, 60000);
  });

  describe('ensureRepositoryExists', () => {
    it('should clone if repository does not exist', async () => {
      const result = await repoManager.ensureRepositoryExists(
        { url: 'https://github.com/anthropics/skills', branch: 'main' },
        tempDir
      );

      expect(result.path).toBeTruthy();
      expect(result.commitHash).toBeTruthy();
      expect(result.name).toContain('anthropics-skills');
      expect(fs.existsSync(result.path)).toBe(true);
    }, 60000);

    it('should pull if repository already exists', async () => {
      // First clone
      const result1 = await repoManager.ensureRepositoryExists(
        { url: 'https://github.com/anthropics/skills', branch: 'main' },
        tempDir
      );

      // Second call should pull
      const result2 = await repoManager.ensureRepositoryExists(
        { url: 'https://github.com/anthropics/skills', branch: 'main' },
        tempDir
      );

      expect(result2.path).toBe(result1.path);
      expect(result2.commitHash).toBeTruthy();
    }, 60000);
  });
});

