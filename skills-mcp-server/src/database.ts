/**
 * SQLite database operations for tracking git hashes and skill changes
 * Uses native Node.js SQLite module (node:sqlite)
 */

import { DatabaseSync } from 'node:sqlite';
import { RepositoryRecord, SkillRecord, CatalogStateRecord, SkillMetadata } from './types.js';

export class SkillsDatabase {
  private db: DatabaseSync;

  constructor(dbPath: string) {
    this.db = new DatabaseSync(dbPath);
    this.initialize();
  }

  /**
   * Initialize database schema
   */
  private initialize(): void {
    // Create repositories table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS repositories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        git_commit_hash TEXT NOT NULL,
        last_synced INTEGER NOT NULL
      )
    `);

    // Create skills table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        repo_id INTEGER NOT NULL,
        name TEXT NOT NULL DEFAULT '',
        description TEXT NOT NULL DEFAULT '',
        skill_path TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        last_checked INTEGER NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (repo_id) REFERENCES repositories(id) ON DELETE CASCADE,
        UNIQUE(repo_id, skill_path)
      )
    `);

    // Create catalog_state table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS catalog_state (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        last_generated_at INTEGER NOT NULL
      )
    `);

    // Initialize catalog_state if empty
    const stateExists = this.db.prepare('SELECT COUNT(*) as count FROM catalog_state').get() as { count: number };
    if (stateExists.count === 0) {
      this.db.prepare('INSERT INTO catalog_state (id, last_generated_at) VALUES (1, 0)').run();
    }
  }

  /**
   * Update repository commit hash
   */
  updateRepositoryHash(url: string, name: string, commitHash: string): number {
    const now = Date.now();
    const result = this.db.prepare(`
      INSERT INTO repositories (url, name, git_commit_hash, last_synced)
      VALUES (?, ?, ?, ?)
      ON CONFLICT(url) DO UPDATE SET
        git_commit_hash = excluded.git_commit_hash,
        last_synced = excluded.last_synced,
        name = excluded.name
    `).run(url, name, commitHash, now);

    // Return the repository ID
    const repo = this.db.prepare('SELECT id FROM repositories WHERE url = ?').get(url) as { id: number };
    return repo.id;
  }

  /**
   * Update skill file hash
   */
  updateSkillHash(repoId: number, skillMetadata: SkillMetadata, enabled: number = 1): void {
    const now = Date.now();
    this.db.prepare(`
      INSERT INTO skills (repo_id, name, description, skill_path, file_hash, last_checked, enabled)
      VALUES (?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(repo_id, skill_path) DO UPDATE SET
        name = excluded.name,
        description = excluded.description,
        file_hash = excluded.file_hash,
        last_checked = excluded.last_checked
    `).run(repoId, skillMetadata.name, skillMetadata.description, skillMetadata.relativePath, skillMetadata.fileHash, now, enabled);
  }

  /**
   * Check if there are changes since last AGENTS.md update
   */
  hasChanges(): boolean {
    const state = this.db.prepare('SELECT last_generated_at FROM catalog_state WHERE id = 1').get() as unknown as CatalogStateRecord;
    const lastGenerated = state.last_generated_at;

    // Check if any repository was synced after last update
    const repoChanges = this.db.prepare(`
      SELECT COUNT(*) as count FROM repositories WHERE last_synced > ?
    `).get(lastGenerated) as unknown as { count: number };

    if (repoChanges.count > 0) {
      return true;
    }

    // Check if any skill was checked after last update
    const skillChanges = this.db.prepare(`
      SELECT COUNT(*) as count FROM skills WHERE last_checked > ?
    `).get(lastGenerated) as unknown as { count: number };

    return skillChanges.count > 0;
  }

  /**
   * Mark AGENTS.md as updated with current timestamp
   */
  markCatalogGenerated(): void {
    const now = Date.now();
    this.db.prepare('UPDATE catalog_state SET last_generated_at = ? WHERE id = 1').run(now);
  }

  /**
   * Get all repositories
   */
  getRepositories(): RepositoryRecord[] {
    return this.db.prepare('SELECT * FROM repositories ORDER BY name').all() as unknown as RepositoryRecord[];
  }

  /**
   * Get repository by URL
   */
  getRepositoryByUrl(url: string): RepositoryRecord | undefined {
    return this.db.prepare('SELECT * FROM repositories WHERE url = ?').get(url) as RepositoryRecord | undefined;
  }

  /**
   * Get repository by name
   */
  getRepositoryByName(name: string): RepositoryRecord | undefined {
    return this.db.prepare('SELECT * FROM repositories WHERE name = ?').get(name) as RepositoryRecord | undefined;
  }

  /**
   * Get all skills
   */
  getSkills(): SkillRecord[] {
    return this.db.prepare('SELECT * FROM skills ORDER BY skill_path').all() as unknown as SkillRecord[];
  }

  /**
   * Get skills for a specific repository
   */
  getSkillsByRepoId(repoId: number): SkillRecord[] {
    return this.db.prepare('SELECT * FROM skills WHERE repo_id = ? ORDER BY skill_path').all(repoId) as unknown as SkillRecord[];
  }

  /**
   * Get all skills from all repositories (alias for consistency)
   */
  getAllSkills(): SkillRecord[] {
    return this.getSkills();
  }

  /**
   * Get all repositories (alias for consistency)
   */
  getAllRepositories(): RepositoryRecord[] {
    return this.getRepositories();
  }

  /**
   * Delete repository and all associated skills
   */
  deleteRepository(url: string): void {
    this.db.prepare('DELETE FROM repositories WHERE url = ?').run(url);
    // Skills are automatically deleted due to CASCADE
  }

  /**
   * Delete skills not in the provided list for a given repository
   */
  deleteStaleSkills(repoId: number, currentSkillPaths: string[]): void {
    if (currentSkillPaths.length === 0) {
      // Delete all skills for this repo
      this.db.prepare('DELETE FROM skills WHERE repo_id = ?').run(repoId);
      return;
    }

    const placeholders = currentSkillPaths.map(() => '?').join(',');
    this.db.prepare(`
      DELETE FROM skills WHERE repo_id = ? AND skill_path NOT IN (${placeholders})
    `).run(repoId, ...currentSkillPaths);
  }

  /**
   * Get count of skills per repository
   */
  getSkillCountByRepo(): Map<number, number> {
    const results = this.db.prepare(`
      SELECT repo_id, COUNT(*) as count FROM skills GROUP BY repo_id
    `).all() as { repo_id: number; count: number }[];

    const map = new Map<number, number>();
    for (const result of results) {
      map.set(result.repo_id, result.count);
    }
    return map;
  }

  /**
   * Close database connection
   */
  close(): void {
    this.db.close();
  }
}

