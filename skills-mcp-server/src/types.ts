/**
 * Type definitions for Skills MCP Server
 */

/**
 * Repository configuration from skills.yaml
 */
export interface SkillRepository {
  url: string;
  branch?: string; // Defaults to 'main'
}

/**
 * Parsed SKILL.md metadata
 */
export interface SkillMetadata {
  name: string;
  description: string;
  path: string; // Absolute path to SKILL.md file
  relativePath: string; // Path relative to repository root
  repoName: string;
  fileHash: string; // SHA256 hash of file content
}

/**
 * Database row for repositories table
 */
export interface RepositoryRecord {
  id: number;
  url: string;
  name: string;
  git_commit_hash: string;
  last_synced: number; // Unix timestamp
}

/**
 * Database row for skills table
 */
export interface SkillRecord {
  id: number;
  repo_id: number;
  name: string;
  description: string;
  skill_path: string;
  file_hash: string;
  last_checked: number; // Unix timestamp
  enabled: number; // 1 = enabled, 0 = disabled
}

/**
 * Database row for catalog_state table
 */
export interface CatalogStateRecord {
  id: number;
  last_generated_at: number; // Unix timestamp
}

/**
 * Result from git sync operations
 */
export interface SyncResult {
  repoName: string;
  commitHash: string;
  skillsFound: number;
  skillsUpdated: number;
  errors: string[];
}

/**
 * Configuration loaded from skills.yaml
 */
export interface SkillsConfig {
  repositories: SkillRepository[];
}

/**
 * Status of a repository
 */
export interface RepositoryStatus {
  url: string;
  branch: string;
  name: string;
  syncStatus: 'synced' | 'syncing' | 'error' | 'pending';
  lastSynced?: Date;
  skillCount: number;
  error?: string;
}

/**
 * Result from refresh operation
 */
export interface RefreshResult {
  repositoriesProcessed: number;
  skillsDiscovered: number;
  catalogRegenerated: boolean;
  errors: string[];
  timestamp: Date;
}

