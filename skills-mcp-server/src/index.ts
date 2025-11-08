#!/usr/bin/env node
/**
 * Skills MCP Server - Main entry point
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import { RepositoryManager } from './repository-manager.js';
import { SkillScanner } from './skill-scanner.js';
import { SkillsDatabase } from './database.js';
import { BackgroundSync } from './background-sync.js';
import { AgentsMdGenerator } from './agents-md-generator.js';
import { SkillsConfig, SkillRepository, RepositoryStatus } from './types.js';

class SkillsMCPServer {
  private server: Server;
  private skillsDir: string;
  private repoManager: RepositoryManager;
  private scanner: SkillScanner;
  private db: SkillsDatabase;
  private backgroundSync: BackgroundSync;

  constructor() {
    this.server = new Server(
      {
        name: 'skills-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Detect workspace directory
    const workspaceDir = process.env.SKILLS_WORKSPACE_DIR || this.findProjectRoot();
    this.skillsDir = path.join(workspaceDir, '.skills');

    // Initialize components
    this.repoManager = new RepositoryManager();
    this.scanner = new SkillScanner();
    
    // Initialize skills directory structure
    this.initializeSkillsDirectory();

    // Initialize database
    const dbPath = path.join(this.skillsDir, 'skills.db');
    this.db = new SkillsDatabase(dbPath);

    // Initialize background sync
    this.backgroundSync = new BackgroundSync(
      this.skillsDir,
      this.repoManager,
      this.scanner,
      this.db
    );

    // Setup MCP handlers
    this.setupHandlers();

    // Log startup info
    console.error('[SkillsMCPServer] Initialized');
    console.error(`[SkillsMCPServer] Skills directory: ${this.skillsDir}`);
    console.error(`[SkillsMCPServer] Workspace: ${workspaceDir}`);
  }

  /**
   * Find project root by looking for .git directory or stopping at parent of skills-mcp-server
   */
  private findProjectRoot(): string {
    let currentDir = process.cwd();
    
    // Walk up the directory tree
    while (currentDir !== path.dirname(currentDir)) {
      // Check if we're in the skills-mcp-server directory
      if (path.basename(currentDir) === 'skills-mcp-server') {
        // Return parent directory (project root)
        return path.dirname(currentDir);
      }
      
      // Check for .git directory (indicates project root)
      if (fs.existsSync(path.join(currentDir, '.git'))) {
        return currentDir;
      }
      
      // Move up one directory
      currentDir = path.dirname(currentDir);
    }
    
    // Fallback to current working directory
    return process.cwd();
  }

  /**
   * Initialize .skills directory structure
   */
  private initializeSkillsDirectory(): void {
    // Create .skills directory
    if (!fs.existsSync(this.skillsDir)) {
      fs.mkdirSync(this.skillsDir, { recursive: true });
      console.error('[SkillsMCPServer] Created .skills directory');
    }

    // Create .gitignore to exclude from client repos
    const gitignorePath = path.join(this.skillsDir, '.gitignore');
    if (!fs.existsSync(gitignorePath)) {
      fs.writeFileSync(gitignorePath, '*\n!.gitignore\n', 'utf-8');
      console.error('[SkillsMCPServer] Created .skills/.gitignore');
    }

    // Create default skills.yaml if missing
    const configPath = path.join(this.skillsDir, 'skills.yaml');
    if (!fs.existsSync(configPath)) {
      const defaultConfig: SkillsConfig = {
        repositories: [
          {
            url: 'https://github.com/anthropics/skills',
            branch: 'main',
          },
        ],
      };
      fs.writeFileSync(configPath, yaml.stringify(defaultConfig), 'utf-8');
      console.error('[SkillsMCPServer] Created default skills.yaml');
    }

    // Create repositories directory
    const reposDir = path.join(this.skillsDir, 'repositories');
    if (!fs.existsSync(reposDir)) {
      fs.mkdirSync(reposDir, { recursive: true });
    }

    // Ensure AGENTS.md exists with skills section markers
    const agentsMdGenerator = new AgentsMdGenerator();
    agentsMdGenerator.ensureAgentsMd(path.dirname(this.skillsDir));
  }

  /**
   * Setup MCP request handlers
   */
  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'list_skill_repositories',
          description: 'List all configured skill repositories with their sync status',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'add_skill_repository',
          description: 'Add a new skill repository from a Git URL',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'Git repository URL (e.g., https://github.com/user/repo)',
              },
              branch: {
                type: 'string',
                description: 'Branch name (optional, defaults to "main")',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'remove_skill_repository',
          description: 'Remove a skill repository by URL',
          inputSchema: {
            type: 'object',
            properties: {
              url: {
                type: 'string',
                description: 'Git repository URL to remove',
              },
            },
            required: ['url'],
          },
        },
        {
          name: 'refresh_skill_repositories',
          description: 'Force immediate sync of all skill repositories (outside of the scheduled interval)',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'list_skill_repositories':
            return await this.handleListRepositories();
          case 'add_skill_repository':
            return await this.handleAddRepository(args?.url as string, args?.branch as string);
          case 'remove_skill_repository':
            return await this.handleRemoveRepository(args?.url as string);
          case 'refresh_skill_repositories':
            return await this.handleRefreshRepositories();
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error: any) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
        };
      }
    });
  }

  /**
   * Handle list_skill_repositories tool
   */
  private async handleListRepositories(): Promise<any> {
    const config = this.readConfig();
    const dbRepos = this.db.getRepositories();
    const skillCounts = this.db.getSkillCountByRepo();

    const statuses: RepositoryStatus[] = config.repositories.map(repo => {
      const dbRepo = dbRepos.find(r => r.url === repo.url);
      const skillCount = dbRepo ? (skillCounts.get(dbRepo.id) || 0) : 0;

      return {
        url: repo.url,
        branch: repo.branch || 'main',
        name: dbRepo?.name || this.repoManager.getRepoNameFromUrl(repo.url),
        syncStatus: dbRepo ? 'synced' : 'pending',
        lastSynced: dbRepo ? new Date(dbRepo.last_synced) : undefined,
        skillCount,
      };
    });

    const output = {
      repositories: statuses,
      totalRepositories: statuses.length,
      totalSkills: Array.from(skillCounts.values()).reduce((a, b) => a + b, 0),
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(output, null, 2),
        },
      ],
    };
  }

  /**
   * Handle add_skill_repository tool
   */
  private async handleAddRepository(url: string, branch?: string): Promise<any> {
    if (!url) {
      throw new Error('URL is required');
    }

    // Validate URL format
    try {
      new URL(url);
    } catch {
      throw new Error('Invalid URL format');
    }

    // Read current config
    const config = this.readConfig();

    // Check if already exists
    if (config.repositories.some(r => r.url === url)) {
      throw new Error('Repository already exists');
    }

    // Add to config
    config.repositories.push({
      url,
      branch: branch || 'main',
    });

    // Write config
    this.writeConfig(config);

    // Trigger background sync (non-blocking)
    setTimeout(() => {
      this.backgroundSync.runSync().catch(error => {
        console.error('[SkillsMCPServer] Error during background sync:', error);
      });
    }, 1000);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            message: `Repository added: ${url}`,
            note: 'Repository will be cloned in the background. Check AGENTS.md in a few moments.',
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Handle remove_skill_repository tool
   */
  private async handleRemoveRepository(url: string): Promise<any> {
    if (!url) {
      throw new Error('URL is required');
    }

    // Read current config
    const config = this.readConfig();

    // Find repository
    const index = config.repositories.findIndex(r => r.url === url);
    if (index === -1) {
      throw new Error('Repository not found');
    }

    // Get repo info for cleanup
    const dbRepo = this.db.getRepositoryByUrl(url);
    const skillCount = dbRepo ? (this.db.getSkillCountByRepo().get(dbRepo.id) || 0) : 0;

    // Remove from config
    config.repositories.splice(index, 1);
    this.writeConfig(config);

    // Clean up database
    if (dbRepo) {
      this.db.deleteRepository(url);
    }

    // Clean up filesystem
    if (dbRepo) {
      const repoPath = path.join(this.skillsDir, 'repositories', dbRepo.name);
      if (fs.existsSync(repoPath)) {
        fs.rmSync(repoPath, { recursive: true, force: true });
      }
    }

    // Update AGENTS.md
    await this.backgroundSync.runSync();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            message: `Repository removed: ${url}`,
            skillsRemoved: skillCount,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Handle refresh_skill_repositories tool
   */
  private async handleRefreshRepositories(): Promise<any> {
    console.error('[SkillsMCPServer] Manual refresh triggered');
    const result = await this.backgroundSync.runSync();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            repositoriesProcessed: result.repositoriesProcessed,
            skillsDiscovered: result.skillsDiscovered,
            catalogRegenerated: result.catalogRegenerated,
            errors: result.errors,
            timestamp: result.timestamp,
          }, null, 2),
        },
      ],
    };
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
      return yaml.parse(content) as SkillsConfig;
    } catch (error: any) {
      console.error(`[SkillsMCPServer] Error reading config: ${error.message}`);
      return { repositories: [] };
    }
  }

  /**
   * Write configuration to skills.yaml
   */
  private writeConfig(config: SkillsConfig): void {
    const configPath = path.join(this.skillsDir, 'skills.yaml');
    fs.writeFileSync(configPath, yaml.stringify(config), 'utf-8');
  }

  /**
   * Start the server
   */
  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);

    // Start background sync
    const syncIntervalMs = parseInt(process.env.SKILLS_SYNC_INTERVAL_MS || '300000', 10);
    this.backgroundSync.startBackgroundSync(syncIntervalMs);

    console.error('[SkillsMCPServer] Server started');
    console.error(`[SkillsMCPServer] Background sync interval: ${syncIntervalMs / 1000}s`);
  }

  /**
   * Stop the server
   */
  async stop(): Promise<void> {
    this.backgroundSync.stopBackgroundSync();
    this.db.close();
    await this.server.close();
    console.error('[SkillsMCPServer] Server stopped');
  }
}

// Suppress ALL console.error logging when running as MCP server
// (MCP protocol uses stderr for JSON protocol messages only, not plain text logs)
// To enable logs for debugging, set SKILLS_DEBUG=true environment variable
if (!process.env.SKILLS_DEBUG) {
  console.error = () => {};
  console.log = () => {};
  console.warn = () => {};
}

// Start server
const server = new SkillsMCPServer();
server.start().catch((error) => {
  console.error('[SkillsMCPServer] Fatal error:', error);
  process.exit(1);
});

// Handle shutdown
process.on('SIGINT', async () => {
  console.error('[SkillsMCPServer] Shutting down...');
  await server.stop();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.error('[SkillsMCPServer] Shutting down...');
  await server.stop();
  process.exit(0);
});

