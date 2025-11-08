/**
 * Background synchronization for skill repositories
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import { RepositoryManager } from './repository-manager.js';
import { SkillScanner } from './skill-scanner.js';
import { SkillsDatabase } from './database.js';
import { AgentsMdGenerator } from './agents-md-generator.js';
import { SkillsConfig, SkillRepository, RefreshResult, SkillRecord } from './types.js';

export class BackgroundSync {
  private intervalHandle?: NodeJS.Timeout;
  private syncInProgress: boolean = false;

  constructor(
    private skillsDir: string,
    private repoManager: RepositoryManager,
    private scanner: SkillScanner,
    private db: SkillsDatabase
  ) {}

  /**
   * Parse AGENTS.md to extract skill enabled/disabled state
   */
  private parseSkillStates(agentsMdPath: string): Map<string, boolean> {
    const stateMap = new Map<string, boolean>();
    if (!fs.existsSync(agentsMdPath)) return stateMap;

    try {
      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      for (const line of content.split('\n')) {
        const enabledMatch = line.match(/^-\s+\[x\]\s+\*\*\[([^\]]+)\]/);
        const disabledMatch = line.match(/^-\s+\[\s\]\s+\*\*\[([^\]]+)\]/);
        if (enabledMatch) stateMap.set(enabledMatch[1], true);
        else if (disabledMatch) stateMap.set(disabledMatch[1], false);
      }
      return stateMap;
    } catch (error) {
      console.error('[BackgroundSync] Error parsing AGENTS.md:', error);
      return stateMap;
    }
  }

  /**
   * Start background sync with specified interval
   */
  startBackgroundSync(intervalMs: number = 300000): void {
    console.log(`[BackgroundSync] Starting background sync (interval: ${intervalMs / 1000}s)`);
    
    this.intervalHandle = setInterval(() => {
      this.runSync().catch(error => {
        console.error('[BackgroundSync] Sync error:', error);
      });
    }, intervalMs);

    // Also run immediately on startup (after delay to allow server to start)
    setTimeout(() => {
      this.runSync().catch(error => {
        console.error('[BackgroundSync] Initial sync error:', error);
      });
    }, 5000);
  }

  /**
   * Stop background sync
   */
  stopBackgroundSync(): void {
    if (this.intervalHandle) {
      clearInterval(this.intervalHandle);
      this.intervalHandle = undefined;
      console.log('[BackgroundSync] Stopped background sync');
    }
  }

  /**
   * Run a full sync cycle
   */
  async runSync(): Promise<RefreshResult> {
    if (this.syncInProgress) {
      console.log('[BackgroundSync] Sync already in progress, skipping...');
      return {
        repositoriesProcessed: 0,
        skillsDiscovered: 0,
        catalogRegenerated: false,
        errors: ['Sync already in progress'],
        timestamp: new Date(),
      };
    }

    this.syncInProgress = true;
    console.log('[BackgroundSync] Starting sync cycle...');

    const errors: string[] = [];
    let repositoriesProcessed = 0;
    let totalSkills = 0;

    try {
      // 1. Read skills.yaml configuration
      const config = this.readConfig();
      const configRepoUrls = new Set(config.repositories.map(r => r.url));

      // 2. Get current repositories from database
      const dbRepos = this.db.getRepositories();
      const dbRepoUrls = new Set(dbRepos.map(r => r.url));

      // 3. Remove repositories no longer in config
      for (const dbRepo of dbRepos) {
        if (!configRepoUrls.has(dbRepo.url)) {
          console.log(`[BackgroundSync] Removing repository: ${dbRepo.name}`);
          this.removeRepository(dbRepo.name);
          this.db.deleteRepository(dbRepo.url);
        }
      }

      // 4. Process each repository in config
      for (const repoConfig of config.repositories) {
        try {
          const result = await this.syncRepository(repoConfig);
          repositoriesProcessed++;
          totalSkills += result.skillsFound;
        } catch (error: any) {
          console.error(`[BackgroundSync] Error syncing ${repoConfig.url}:`, error.message);
          errors.push(`${repoConfig.url}: ${error.message}`);
        }
      }

      // 5. Check if AGENTS.md needs update
      let agentsMdUpdated = false;
      if (this.db.hasChanges()) {
        console.log('[BackgroundSync] Changes detected, updating AGENTS.md...');
        await this.updateAgentsMd();
        this.db.markCatalogGenerated();
        agentsMdUpdated = true;
      } else {
        console.log('[BackgroundSync] No changes detected, AGENTS.md up to date');
      }

      console.log(`[BackgroundSync] Sync complete: ${repositoriesProcessed} repos, ${totalSkills} skills`);

      return {
        repositoriesProcessed,
        skillsDiscovered: totalSkills,
        catalogRegenerated: agentsMdUpdated,
        errors,
        timestamp: new Date(),
      };
    } finally {
      this.syncInProgress = false;
    }
  }

  /**
   * Sync a single repository
   * 
   * CRITICAL: Only scans repositories within .skills/repositories/
   * Skips all hidden directories (including .claude, .git, .github, etc.)
   */
  private async syncRepository(config: SkillRepository): Promise<{ skillsFound: number }> {
    const repositoriesDir = path.join(this.skillsDir, 'repositories');

    // Ensure repository exists and is up to date
    const { path: repoPath, commitHash, name } = await this.repoManager.ensureRepositoryExists(
      config,
      repositoriesDir
    );

    // Update repository in database
    const repoId = this.db.updateRepositoryHash(config.url, name, commitHash);

    // Scan for skills
    const skills = this.scanner.scanRepositoryForSkills(repoPath, name);

    // Parse existing AGENTS.md to preserve enabled/disabled state
    const agentsMdPath = path.join(path.dirname(this.skillsDir), 'AGENTS.md');
    const skillStates = this.parseSkillStates(agentsMdPath);

    // Update skills in database, preserving enabled state
    const skillPaths: string[] = [];
    for (const skill of skills) {
      const enabled = skillStates.has(skill.name) ? (skillStates.get(skill.name) ? 1 : 0) : 1;
      this.db.updateSkillHash(repoId, skill, enabled);
      skillPaths.push(skill.relativePath);
    }

    // Remove stale skills from database
    this.db.deleteStaleSkills(repoId, skillPaths);

    return { skillsFound: skills.length };
  }

  /**
   * Read configuration from skills.yaml
   */
  private readConfig(): SkillsConfig {
    const configPath = path.join(this.skillsDir, 'skills.yaml');
    
    if (!fs.existsSync(configPath)) {
      return { repositories: [] };
    }

    try {
      const content = fs.readFileSync(configPath, 'utf-8');
      const parsed = yaml.parse(content);
      return parsed as SkillsConfig;
    } catch (error: any) {
      console.error(`[BackgroundSync] Error reading config: ${error.message}`);
      return { repositories: [] };
    }
  }

  /**
   * Remove repository from filesystem
   */
  private removeRepository(repoName: string): void {
    const repoPath = path.join(this.skillsDir, 'repositories', repoName);
    if (fs.existsSync(repoPath)) {
      fs.rmSync(repoPath, { recursive: true, force: true });
      console.log(`[BackgroundSync] Deleted repository: ${repoPath}`);
    }
  }

  /**
   * Update AGENTS.md with current skills
   */
  private async updateAgentsMd(): Promise<void> {
    // Get all skills and repositories from database
    const allSkills = this.db.getAllSkills();
    const allRepositories = this.db.getAllRepositories();

    // Scan for local skills in project root
    const projectRoot = path.dirname(this.skillsDir);
    const localSkillsMetadata = this.scanner.scanProjectForLocalSkills(projectRoot);
    
    // Convert local skills metadata to SkillRecord format
    const localSkills: SkillRecord[] = localSkillsMetadata.map(skill => ({
      id: -1,  // Use -1 to indicate local skill
      repo_id: -1,
      name: skill.name,
      description: skill.description,
      skill_path: skill.relativePath,
      file_hash: skill.fileHash,
      enabled: 1,
      last_checked: Math.floor(Date.now() / 1000),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }));

    // Update AGENTS.md with full skills list
    const agentsMdGenerator = new AgentsMdGenerator();
    agentsMdGenerator.updateAgentsMdWithSkills(projectRoot, allSkills, allRepositories, localSkills);
  }
}

