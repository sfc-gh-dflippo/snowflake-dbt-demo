/**
 * Skills MCP Server
 * 
 * Provides Python and TypeScript sync scripts as downloadable MCP resources.
 * Built with FastMCP - a trusted TypeScript framework for MCP servers.
 * 
 * Resources:
 * - script://sync-skills.py - Python sync script
 * - script://sync-skills.ts - TypeScript sync script
 * - doc://manage-repositories - Documentation for managing repositories
 */

import { FastMCP } from 'fastmcp';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Constants for instructions
const WHAT_IT_DOES_INSTRUCTIONS = `**What it does:**
- Reads repositories from \`.skills/repos.txt\`
- Clones/pulls GitHub repos efficiently
- Scans for local and remote SKILL.md files
- Applies local skill precedence
- Updates AGENTS.md with organized skills list`;

const PYTHON_SCRIPT_INSTRUCTIONS = `Python script to sync skills from GitHub repositories to AGENTS.md.

**To use:**
1. Write this script to: \`sync-skills.py\` in project root
2. Execute: \`python3 sync-skills.py\`

${WHAT_IT_DOES_INSTRUCTIONS}`;

const TYPESCRIPT_SCRIPT_INSTRUCTIONS = `TypeScript script to sync skills from GitHub repositories to AGENTS.md.

**To use:**
1. Write this script to: \`sync-skills.ts\` in project root
2. Execute: \`npx tsx sync-skills.ts\`

${WHAT_IT_DOES_INSTRUCTIONS}`;

const MANAGE_REPOS_DESCRIPTION = `Instructions for adding and removing GitHub repositories from the skills configuration.`;

const SERVER_INSTRUCTIONS = `This server manages AI agent skills by providing sync scripts as MCP resources.

**To sync skills:**
## Step 1: Check all available MCP resources
## Step 2: Download the \`script://sync-skills.ts\` or \`script://sync-skills.py\` sync script to a file in the project root directory
## Step 3: Execute the script in your local environment using npx or python3

\`\`\`bash
npx tsx sync-skills.ts
\`\`\`
or
\`\`\`bash
python3 sync-skills.py
\`\`\`

${WHAT_IT_DOES_INSTRUCTIONS}

## Configuration

Configure repositories in \`.skills/repos.txt\`:
\`\`\`
https://github.com/anthropics/skills
https://github.com/your-org/custom-skills
\`\`\`
`;

// Initialize FastMCP server
const server = new FastMCP({
  name: 'skills-mcp-server',
  version: '2.0.0',
  instructions: SERVER_INSTRUCTIONS,
});

// Add Python sync script resource
server.addResource({
  uri: 'script://sync-skills.py',
  name: 'Skills Sync Script (Python)',
  description: PYTHON_SCRIPT_INSTRUCTIONS,
  mimeType: 'text/x-python',
  load: async () => {
    const text = fs.readFileSync(
      path.join(__dirname, 'resources', 'sync-skills.py'),
      'utf-8'
    );
    return {
      text,
      mimeType: 'text/x-python',
      uri: 'script://sync-skills.py',
    };
  },
});

// Add TypeScript sync script resource
server.addResource({
  uri: 'script://sync-skills.ts',
  name: 'Skills Sync Script (TypeScript)',
  description: TYPESCRIPT_SCRIPT_INSTRUCTIONS,
  mimeType: 'application/typescript',
  load: async () => {
    const text = fs.readFileSync(
      path.join(__dirname, 'resources', 'sync-skills.ts'),
      'utf-8'
    );
    return {
      text,
      mimeType: 'application/typescript',
      uri: 'script://sync-skills.ts',
    };
  },
});

// Add repository management documentation
server.addResource({
  uri: 'doc://manage-repositories',
  name: 'Managing Skills Repositories',
  description: MANAGE_REPOS_DESCRIPTION,
  mimeType: 'text/markdown',
  load: async () => {
    const text = fs.readFileSync(
      path.join(__dirname, 'resources', 'manage-repositories.md'),
      'utf-8'
    );
    return {
      text,
      mimeType: 'text/markdown',
      uri: 'doc://manage-repositories',
    };
  },
});

// Add prompts to guide agents on using the resources
server.addPrompt({
  name: 'sync-skills',
  description: 'Step-by-step instructions for syncing skills, including how to fetch and execute the sync script',
  load: async () => SERVER_INSTRUCTIONS,
});

server.addPrompt({
  name: 'manage-repositories',
  description: 'Learn how to add and remove GitHub repositories from skills configuration',
  load: async () => {
    const content = fs.readFileSync(
      path.join(__dirname, 'resources', 'manage-repositories.md'),
      'utf-8'
    );
    return content;
  },
});

// Add tools that agents can call (Cursor needs these!)
server.addTool({
  name: 'get_sync_instructions',
  description: 'Step-by-step instructions for syncing skills, including how to fetch and execute the sync script',
  execute: async () => SERVER_INSTRUCTIONS,
});

// Start the server
server.start({
  transportType: 'stdio',
});

console.error('[SkillsMCPServer] Started - serving sync scripts as downloadable resources');
console.error('[SkillsMCPServer] Resources: 3, Prompts: 2, Tools: 1');
console.error('[SkillsMCPServer] Built with FastMCP framework');
