/**
 * SKILL.md discovery and parsing
 */

import * as fs from 'fs';
import * as path from 'path';
import matter from 'gray-matter';
import { createHash } from 'crypto';
import { SkillMetadata } from './types.js';

export class SkillScanner {
  /**
   * Scan repository for all SKILL.md files
   * 
   * IMPORTANT: This should ONLY be called on repositories within .skills/repositories/
   * It will scan the given repository path and find all SKILL.md files, skipping:
   * - All hidden directories (starting with .)
   * - node_modules, venv, __pycache__
   * 
   * @param repoPath Absolute path to repository (MUST be within .skills/repositories/)
   * @param repoName Name of the repository
   * @returns Array of discovered skill metadata
   */
  scanRepositoryForSkills(repoPath: string, repoName: string): SkillMetadata[] {
    // Validate that we're scanning within .skills/repositories/ only
    if (!repoPath.includes('.skills/repositories/') && !repoPath.includes('.skills\\repositories\\')) {
      console.warn(`[SkillScanner] WARNING: Attempting to scan outside .skills/repositories/: ${repoPath}`);
      return [];
    }

    const skills: SkillMetadata[] = [];
    this.findSkillFiles(repoPath, repoPath, repoName, skills);
    return skills;
  }

  /**
   * Scan project root for local SKILL.md files
   * 
   * This scans the project root directory for SKILL.md files, excluding:
   * - .skills directory (managed repositories)
   * - node_modules, venv, __pycache__
   * - .git, .github
   * - skills-mcp-server directory
   * 
   * @param projectRoot Absolute path to project root
   * @returns Array of discovered skill metadata
   */
  scanProjectForLocalSkills(projectRoot: string): SkillMetadata[] {
    const skills: SkillMetadata[] = [];
    this.findLocalSkillFiles(projectRoot, projectRoot, 'local', skills);
    return skills;
  }

  /**
   * Recursively find SKILL.md files in project root (for local skills)
   */
  private findLocalSkillFiles(
    currentPath: string,
    projectRoot: string,
    repoName: string,
    skills: SkillMetadata[]
  ): void {
    try {
      const entries = fs.readdirSync(currentPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);

        // Skip directories that should be excluded
        if (entry.name === '.skills' ||
            entry.name === '.git' ||
            entry.name === '.github' ||
            entry.name === 'node_modules' || 
            entry.name === 'venv' ||
            entry.name === '__pycache__' ||
            entry.name === 'skills-mcp-server') {
          continue;
        }

        if (entry.isDirectory()) {
          this.findLocalSkillFiles(fullPath, projectRoot, repoName, skills);
        } else if (entry.name === 'SKILL.md') {
          const skillData = this.parseSkillFile(fullPath, projectRoot, repoName);
          if (skillData) {
            skills.push(skillData);
          }
        }
      }
    } catch (error: any) {
      console.warn(`[SkillScanner] Error scanning ${currentPath}: ${error.message}`);
    }
  }

  /**
   * Recursively find SKILL.md files
   */
  private findSkillFiles(
    currentPath: string,
    repoRoot: string,
    repoName: string,
    skills: SkillMetadata[]
  ): void {
    try {
      const entries = fs.readdirSync(currentPath, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry.name);

        // Skip only technical directories, but allow .claude, .skills, and other hidden dirs
        if (entry.name === '.git' ||
            entry.name === '.github' ||
            entry.name === 'node_modules' || 
            entry.name === 'venv' ||
            entry.name === '__pycache__') {
          continue;
        }

        if (entry.isDirectory()) {
          this.findSkillFiles(fullPath, repoRoot, repoName, skills);
        } else if (entry.name === 'SKILL.md') {
          const skillData = this.parseSkillFile(fullPath, repoRoot, repoName);
          if (skillData) {
            skills.push(skillData);
          }
        }
      }
    } catch (error: any) {
      console.warn(`[SkillScanner] Error scanning ${currentPath}: ${error.message}`);
    }
  }

  /**
   * Parse a SKILL.md file and extract metadata
   */
  parseSkillFile(skillPath: string, repoRoot: string, repoName: string): SkillMetadata | null {
    try {
      const content = fs.readFileSync(skillPath, 'utf-8');
      const parsed = matter(content);

      // Extract required frontmatter fields
      const name = parsed.data.name as string;
      const description = parsed.data.description as string;

      if (!name || !description) {
        console.warn(`[SkillScanner] Skill at ${skillPath} missing required frontmatter (name/description)`);
        return null;
      }

      // Calculate file hash
      const fileHash = this.calculateFileHash(skillPath);

      // Calculate relative path from repository root
      const relativePath = path.relative(repoRoot, skillPath);

      return {
        name,
        description,
        path: skillPath,
        relativePath,
        repoName,
        fileHash,
      };
    } catch (error: any) {
      console.warn(`[SkillScanner] Error parsing ${skillPath}: ${error.message}`);
      return null;
    }
  }

  /**
   * Calculate SHA256 hash of file content
   */
  calculateFileHash(filePath: string): string {
    try {
      const content = fs.readFileSync(filePath);
      return createHash('sha256').update(content).digest('hex');
    } catch (error: any) {
      console.warn(`[SkillScanner] Error hashing ${filePath}: ${error.message}`);
      return '';
    }
  }

  /**
   * Get skill directory (parent of SKILL.md)
   */
  getSkillDirectory(skillPath: string): string {
    return path.dirname(skillPath);
  }
}

