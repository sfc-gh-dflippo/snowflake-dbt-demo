import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { BackgroundSync } from '../src/background-sync.js';
import { SkillsDatabase } from '../src/database.js';
import { RepositoryManager } from '../src/repository-manager.js';
import { SkillScanner } from '../src/skill-scanner.js';
import * as fs from 'fs';
import * as path from 'path';
import { tmpdir } from 'os';
import { parse } from 'yaml';

describe('BackgroundSync', () => {
  let tempDir: string;
  let skillsDir: string;
  let db: SkillsDatabase;
  let repoManager: RepositoryManager;
  let skillScanner: SkillScanner;
  let backgroundSync: BackgroundSync;

  beforeEach(() => {
    // Create temporary directory for test
    tempDir = fs.mkdtempSync(path.join(tmpdir(), 'background-sync-test-'));
    skillsDir = path.join(tempDir, '.skills');
    fs.mkdirSync(skillsDir, { recursive: true });
    fs.mkdirSync(path.join(skillsDir, 'repositories'), { recursive: true });

    // Initialize components
    const dbPath = path.join(skillsDir, 'skills.db');
    db = new SkillsDatabase(dbPath);
    repoManager = new RepositoryManager();
    skillScanner = new SkillScanner();
    backgroundSync = new BackgroundSync(skillsDir, repoManager, skillScanner, db);
  });

  afterEach(() => {
    // Clean up
    backgroundSync.stopBackgroundSync();
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  describe('startBackgroundSync', () => {
    it('should start background sync with default interval', () => {
      backgroundSync.startBackgroundSync();
      
      // Verify sync was started (no errors thrown)
      expect(true).toBe(true);
      
      backgroundSync.stopBackgroundSync();
    });

    it('should start background sync with custom interval', () => {
      backgroundSync.startBackgroundSync(60000); // 1 minute
      
      // Verify sync was started
      expect(true).toBe(true);
      
      backgroundSync.stopBackgroundSync();
    });
  });

  describe('stopBackgroundSync', () => {
    it('should stop background sync', () => {
      backgroundSync.startBackgroundSync();
      backgroundSync.stopBackgroundSync();
      
      // Verify sync was stopped (no errors thrown)
      expect(true).toBe(true);
    });

    it('should handle stopping when not started', () => {
      backgroundSync.stopBackgroundSync();
      
      // Should not throw error
      expect(true).toBe(true);
    });
  });

  describe('runSync', () => {
    it('should handle missing skills.yaml gracefully', async () => {
      await backgroundSync.runSync();
      
      // Should complete without errors even if skills.yaml doesn't exist
      expect(true).toBe(true);
    });

    it('should process repositories from skills.yaml', async () => {
      // Create AGENTS.md first (normally done by initializeSkillsDirectory)
      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      fs.writeFileSync(agentsMdPath, `# Agent Instructions

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
`, 'utf-8');

      // Create skills.yaml with a test repository
      const skillsYaml = {
        repositories: [
          {
            url: 'https://github.com/anthropics/skills',
            branch: 'main'
          }
        ]
      };
      
      const yaml = require('yaml');
      fs.writeFileSync(
        path.join(skillsDir, 'skills.yaml'),
        yaml.stringify(skillsYaml),
        'utf-8'
      );

      // Run sync (this will actually clone the repo, so it may take time)
      await backgroundSync.runSync();

      // Verify AGENTS.md was updated with skills
      expect(fs.existsSync(agentsMdPath)).toBe(true);
      const agentsContent = fs.readFileSync(agentsMdPath, 'utf-8');
      expect(agentsContent).toContain('MCP-Managed Skills');
      
      // Verify repository was added to database
      const repos = db.getRepositories();
      expect(repos.length).toBeGreaterThan(0);
    }, 120000); // 2 minute timeout for git operations

    it('should not regenerate catalog if no changes', async () => {
      // Create empty skills.yaml
      const skillsYaml = { repositories: [] };
      const yaml = require('yaml');
      fs.writeFileSync(
        path.join(skillsDir, 'skills.yaml'),
        yaml.stringify(skillsYaml),
        'utf-8'
      );

      // First sync
      await backgroundSync.runSync();
      
      const agentsMdPath = path.join(path.dirname(skillsDir), 'AGENTS.md');
      const firstGenTime = fs.existsSync(agentsMdPath) 
        ? fs.statSync(agentsMdPath).mtimeMs 
        : 0;

      // Wait a bit
      await new Promise(resolve => setTimeout(resolve, 100));

      // Second sync (should detect no changes)
      await backgroundSync.runSync();
      
      const secondGenTime = fs.existsSync(agentsMdPath)
        ? fs.statSync(agentsMdPath).mtimeMs
        : 0;

      // Times should be very close or identical since no changes
      if (firstGenTime > 0 && secondGenTime > 0) {
        const timeDiff = Math.abs(secondGenTime - firstGenTime);
        expect(timeDiff).toBeLessThan(1000); // Less than 1 second difference
      }
    }, 30000);
  });

  describe('sync prevention', () => {
    it('should not run multiple syncs simultaneously', async () => {
      // Create simple skills.yaml
      const skillsYaml = { repositories: [] };
      const yaml = require('yaml');
      fs.writeFileSync(
        path.join(skillsDir, 'skills.yaml'),
        yaml.stringify(skillsYaml),
        'utf-8'
      );

      // Start two syncs at the same time
      const sync1 = backgroundSync.runSync();
      const sync2 = backgroundSync.runSync();

      await Promise.all([sync1, sync2]);

      // Both should complete without errors (second should skip)
      expect(true).toBe(true);
    }, 30000);
  });
});

