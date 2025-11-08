/**
 * Tests for AgentsMdGenerator
 */

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { AgentsMdGenerator } from '../src/agents-md-generator.js';
import { SkillRecord, RepositoryRecord } from '../src/types.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('AgentsMdGenerator', () => {
  let generator: AgentsMdGenerator;
  let tempDir: string;

  beforeEach(() => {
    generator = new AgentsMdGenerator();
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'agents-md-test-'));
  });

  afterEach(() => {
    if (fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
  });

  describe('ensureAgentsMd', () => {
    it('should create AGENTS.md if it does not exist', () => {
      generator.ensureAgentsMd(tempDir);

      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      expect(fs.existsSync(agentsMdPath)).toBe(true);

      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      expect(content).toContain('# Agent Instructions');
      expect(content).toContain('<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->');
      expect(content).toContain('<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->');
      expect(content).toContain('# Skills');
      expect(content).toContain('What are Skills?');
    });

    it('should add skills section to existing AGENTS.md', () => {
      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const existingContent = `# Agent Instructions

## Project Overview

This is my project.
`;
      fs.writeFileSync(agentsMdPath, existingContent, 'utf-8');

      generator.ensureAgentsMd(tempDir);

      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      expect(content).toContain('This is my project.');
      expect(content).toContain('<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->');
      expect(content).toContain('<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->');
    });

    it('should not duplicate skills section if it already exists', () => {
      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const existingContent = `# Agent Instructions

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
## MCP-Managed Skills
Already has MCP skills section
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
`;
      fs.writeFileSync(agentsMdPath, existingContent, 'utf-8');

      generator.ensureAgentsMd(tempDir);

      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      const matches = content.match(/<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->/g);
      expect(matches?.length).toBe(1);
    });
  });

  describe('updateAgentsMdWithSkills', () => {
    beforeEach(() => {
      // Create a basic AGENTS.md with markers
      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const content = `# Agent Instructions

## Project Overview

This is my project.

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->
`;
      fs.writeFileSync(agentsMdPath, content, 'utf-8');
    });

    it('should update AGENTS.md with repository skills', () => {
      const skills: SkillRecord[] = [
        {
          id: 1,
          repo_id: 1,
          name: 'test-skill',
          description: 'A test skill',
          skill_path: 'test-skill/SKILL.md',
          file_hash: 'hash1',
          enabled: 1,
          last_checked: Date.now(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      const repositories: RepositoryRecord[] = [
        {
          id: 1,
          url: 'https://github.com/test/repo',
          name: 'test-repo',
          git_commit_hash: 'abc123',
          last_synced: Date.now(),
        },
      ];

      generator.updateAgentsMdWithSkills(tempDir, skills, repositories, []);

      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      
      expect(content).toContain('This is my project');
      expect(content).toContain('## MCP-Managed Skills');
      expect(content).toContain('# Skills');
      expect(content).toContain('### test-repo');
      expect(content).toContain('test-skill');
      expect(content).toContain('A test skill');
    });

    it('should show local skills first', () => {
      const repoSkills: SkillRecord[] = [
        {
          id: 1,
          repo_id: 1,
          name: 'repo-skill',
          description: 'From repository',
          skill_path: 'repo-skill/SKILL.md',
          file_hash: 'hash1',
          enabled: 1,
          last_checked: Date.now(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      const localSkills: SkillRecord[] = [
        {
          id: -1,
          repo_id: -1,
          name: 'local-skill',
          description: 'From local project',
          skill_path: '.claude/skills/local/SKILL.md',
          file_hash: 'hash2',
          enabled: 1,
          last_checked: Date.now(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      const repositories: RepositoryRecord[] = [
        {
          id: 1,
          url: 'https://github.com/test/repo',
          name: 'test-repo',
          git_commit_hash: 'abc123',
          last_synced: Date.now(),
        },
      ];

      generator.updateAgentsMdWithSkills(tempDir, repoSkills, repositories, localSkills);

      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      
      const localIndex = content.indexOf('### Local Skills');
      const repoIndex = content.indexOf('### test-repo');
      
      expect(localIndex).toBeGreaterThan(-1);
      expect(repoIndex).toBeGreaterThan(-1);
      expect(localIndex).toBeLessThan(repoIndex); // Local should come first
    });

    it('should prefer local skills over remote skills with same name', () => {
      const repoSkills: SkillRecord[] = [
        {
          id: 1,
          repo_id: 1,
          name: 'duplicate-skill',
          description: 'Remote version',
          skill_path: 'duplicate-skill/SKILL.md',
          file_hash: 'hash1',
          enabled: 1,
          last_checked: Date.now(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      const localSkills: SkillRecord[] = [
        {
          id: -1,
          repo_id: -1,
          name: 'duplicate-skill',
          description: 'Local version',
          skill_path: '.claude/skills/duplicate/SKILL.md',
          file_hash: 'hash2',
          enabled: 1,
          last_checked: Date.now(),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        },
      ];

      const repositories: RepositoryRecord[] = [
        {
          id: 1,
          url: 'https://github.com/test/repo',
          name: 'test-repo',
          git_commit_hash: 'abc123',
          last_synced: Date.now(),
        },
      ];

      generator.updateAgentsMdWithSkills(tempDir, repoSkills, repositories, localSkills);

      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      
      // Should only contain local version
      expect(content).toContain('Local version');
      expect(content).not.toContain('Remote version');
      
      // Should appear in Local Skills section
      expect(content).toContain('### Local Skills');
      const localSectionStart = content.indexOf('### Local Skills');
      const localVersionIndex = content.indexOf('Local version');
      expect(localVersionIndex).toBeGreaterThan(localSectionStart);
    });

    it('should preserve content outside markers', () => {
      const agentsMdPath = path.join(tempDir, 'AGENTS.md');
      const beforeContent = `# My Custom Header

Important project info here.

<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->
<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->

## Footer Section

More content at the end.
`;
      fs.writeFileSync(agentsMdPath, beforeContent, 'utf-8');

      generator.updateAgentsMdWithSkills(tempDir, [], [], []);

      const content = fs.readFileSync(agentsMdPath, 'utf-8');
      expect(content).toContain('# My Custom Header');
      expect(content).toContain('Important project info here');
      expect(content).toContain('## Footer Section');
      expect(content).toContain('More content at the end');
    });
  });
});
