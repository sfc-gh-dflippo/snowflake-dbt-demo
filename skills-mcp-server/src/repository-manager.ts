/**
 * Git repository management using simple-git
 * Requires git CLI to be installed
 */

import { simpleGit, SimpleGit, SimpleGitOptions } from 'simple-git';
import * as fs from 'fs';
import * as path from 'path';
import { SkillRepository } from './types.js';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class RepositoryManager {
  constructor() {
    this.verifyGitInstalled();
  }

  /**
   * Verify git CLI is installed
   */
  private async verifyGitInstalled(): Promise<void> {
    try {
      await execAsync('git --version');
      console.log('[RepositoryManager] Git CLI detected');
    } catch (error) {
      throw new Error('Git CLI is required but not found. Please install git.');
    }
  }

  /**
   * Extract repository name from URL
   */
  getRepoNameFromUrl(url: string): string {
    // Remove .git suffix if present
    let cleanUrl = url.replace(/\.git$/, '');
    
    // Extract path after last slash
    const parts = cleanUrl.split('/');
    const repoName = parts[parts.length - 1];
    const owner = parts[parts.length - 2];
    
    // Extract hostname for server-unique subdirectory
    const urlObj = new URL(url);
    const hostname = urlObj.hostname.replace(/\./g, '-');
    
    return `${hostname}/${owner}-${repoName}`;
  }

  /**
   * Clone repository using git CLI
   */
  async cloneRepository(url: string, branch: string, targetPath: string): Promise<void> {
    // Ensure parent directory exists
    const parentDir = path.dirname(targetPath);
    if (!fs.existsSync(parentDir)) {
      fs.mkdirSync(parentDir, { recursive: true });
    }

    const options: Partial<SimpleGitOptions> = {
      baseDir: path.dirname(targetPath),
      binary: 'git',
      maxConcurrentProcesses: 6,
    };

    const git: SimpleGit = simpleGit(options);
    
    try {
      await git.clone(url, targetPath, [
        '--depth', '1',
        '--single-branch',
        '--branch', branch
      ]);
    } catch (error: any) {
      // Try with 'main' if specified branch fails
      if (branch !== 'main') {
        console.log(`[RepositoryManager] Branch ${branch} failed, trying 'main'...`);
        await git.clone(url, targetPath, [
          '--depth', '1',
          '--single-branch',
          '--branch', 'main'
        ]);
      } else {
        throw error;
      }
    }
  }

  /**
   * Pull repository updates
   */
  async pullRepository(repoPath: string): Promise<string> {
    const git: SimpleGit = simpleGit(repoPath);
    await git.pull(['--depth', '1']);
    return await this.getCurrentCommitHash(repoPath);
  }

  /**
   * Get current commit hash
   */
  async getCurrentCommitHash(repoPath: string): Promise<string> {
    const git: SimpleGit = simpleGit(repoPath);
    const log = await git.log({ maxCount: 1 });
    return log.latest?.hash || '';
  }

  /**
   * Ensure repository exists (clone if missing, pull if exists)
   */
  async ensureRepositoryExists(config: SkillRepository, repositoriesDir: string): Promise<{ path: string; commitHash: string; name: string }> {
    const branch = config.branch || 'main';
    const repoName = this.getRepoNameFromUrl(config.url);
    const repoPath = path.join(repositoriesDir, repoName);

    if (!fs.existsSync(repoPath)) {
      console.log(`[RepositoryManager] Cloning ${config.url} (${branch})...`);
      await this.cloneRepository(config.url, branch, repoPath);
    } else {
      console.log(`[RepositoryManager] Pulling updates for ${repoName}...`);
      try {
        await this.pullRepository(repoPath);
      } catch (error: any) {
        console.warn(`[RepositoryManager] Pull failed for ${repoName}: ${error.message}`);
        // Continue with existing repo if pull fails
      }
    }

    const commitHash = await this.getCurrentCommitHash(repoPath);
    return { path: repoPath, commitHash, name: repoName };
  }

  /**
   * Check if a path is a git repository
   */
  isGitRepository(dir: string): boolean {
    return fs.existsSync(path.join(dir, '.git'));
  }
}

