/**
 * AGENTS.md file generation and management
 */

import * as fs from 'fs';
import * as path from 'path';
import { SkillRecord, RepositoryRecord } from './types.js';

export class AgentsMdGenerator {
  private readonly SKILLS_SECTION_MARKER = '<!-- BEGIN MCP SKILLS - DO NOT EDIT MANUALLY -->';
  private readonly SKILLS_SECTION_END = '<!-- END MCP SKILLS - DO NOT EDIT MANUALLY -->';

  /**
   * Check if AGENTS.md exists and create/update it with skills reference
   */
  ensureAgentsMd(projectRoot: string): void {
    const agentsMdPath = path.join(projectRoot, 'AGENTS.md');

    if (!fs.existsSync(agentsMdPath)) {
      // Create new AGENTS.md with default content
      this.createAgentsMd(agentsMdPath);
      console.log('[AgentsMdGenerator] Created AGENTS.md with skills reference');
    } else {
      // Check if skills reference exists, add if not
      this.ensureSkillsReference(agentsMdPath);
    }
  }

  /**
   * Update AGENTS.md with full skills list
   */
  updateAgentsMdWithSkills(projectRoot: string, skills: SkillRecord[], repositories: RepositoryRecord[], localSkills: SkillRecord[]): void {
    const agentsMdPath = path.join(projectRoot, 'AGENTS.md');

    if (!fs.existsSync(agentsMdPath)) {
      console.warn('[AgentsMdGenerator] AGENTS.md does not exist, cannot update skills');
      return;
    }

    const content = fs.readFileSync(agentsMdPath, 'utf-8');
    const updatedContent = this.replaceSkillsSection(content, skills, repositories, localSkills);
    fs.writeFileSync(agentsMdPath, updatedContent, 'utf-8');
    console.log('[AgentsMdGenerator] Updated AGENTS.md with skills list');
  }

  /**
   * Create a new AGENTS.md file
   */
  private createAgentsMd(agentsMdPath: string): void {
    const content = `# Agent Instructions

This document provides context and guidelines for AI coding agents working on this project.

## Project Overview

[Add your project description here]

## Technology Stack

[Add your technology stack here]

## Guidelines for Agents

### Code Standards
- Follow established patterns across the project
- Write testable, well-documented code
- Maintain consistency with existing code style

### Safety and Permissions

#### Allowed without prompt:
- Read files, list files
- Run tests
- Format code

#### Ask first:
- Installing new dependencies
- Modifying configuration files
- Deleting files
- Making git commits

${this.getSkillsSection()}
`;

    fs.writeFileSync(agentsMdPath, content, 'utf-8');
  }

  /**
   * Ensure AGENTS.md has the skills reference section
   */
  private ensureSkillsReference(agentsMdPath: string): void {
    const content = fs.readFileSync(agentsMdPath, 'utf-8');

    // Check if MCP skills section already exists
    if (content.includes(this.SKILLS_SECTION_MARKER)) {
      console.log('[AgentsMdGenerator] AGENTS.md already has MCP skills reference');
      return;
    }

    // Add skills section at the end
    const updatedContent = content.trimEnd() + '\n\n' + this.getSkillsSection();
    fs.writeFileSync(agentsMdPath, updatedContent, 'utf-8');
    console.log('[AgentsMdGenerator] Added skills reference to AGENTS.md');
  }

  /**
   * Get the skills section content
   */
  private getSkillsSection(): string {
    return `${this.SKILLS_SECTION_MARKER}

## MCP-Managed Skills

This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.

# Skills

**What are Skills?**

Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:
- **SKILL.md** - Core instructions and guidelines
- **references/** - Detailed documentation and examples
- **scripts/** - Helper scripts and templates
- **config/** - Configuration files

Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized "expert personas" for areas like dbt development, Snowflake operations, or testing frameworks.

**Key Features:**
- Skills can be enabled \`[x]\` or disabled \`[ ]\` individually

**Available Skills:**

No skills are currently available. Use the MCP tools to add skill repositories.

${this.SKILLS_SECTION_END}
`;
  }

  /**
   * Replace the skills section in AGENTS.md with updated content
   */
  private replaceSkillsSection(content: string, skills: SkillRecord[], repositories: RepositoryRecord[], localSkills: SkillRecord[]): string {
    const startIndex = content.indexOf(this.SKILLS_SECTION_MARKER);
    const endIndex = content.indexOf(this.SKILLS_SECTION_END);

    if (startIndex === -1 || endIndex === -1) {
      console.warn('[AgentsMdGenerator] Could not find skills section markers in AGENTS.md');
      return content;
    }

    const beforeSection = content.substring(0, startIndex);
    const afterSection = content.substring(endIndex + this.SKILLS_SECTION_END.length);
    const skillsSection = this.formatSkillsSection(skills, repositories, localSkills);

    return beforeSection + skillsSection + afterSection;
  }

  /**
   * Format the skills section content with full skills list
   */
  private formatSkillsSection(skills: SkillRecord[], repositories: RepositoryRecord[], localSkills: SkillRecord[]): string {
    const timestamp = new Date().toISOString();
    let content = `${this.SKILLS_SECTION_MARKER}\n`;
    content += `<!-- Generated: ${timestamp} -->\n\n`;
    content += `## MCP-Managed Skills\n\n`;
    content += `This project uses the **Skills MCP Server** to dynamically manage both local SKILL.md files and skills from remote Git repositories.\n\n`;
    content += `# Skills\n\n`;
    content += `**What are Skills?**\n\n`;
    content += `Skills are structured instruction sets that enhance AI assistant capabilities for specific domains or tasks. Each skill is a folder containing:\n`;
    content += `- **SKILL.md** - Core instructions and guidelines\n`;
    content += `- **references/** - Detailed documentation and examples\n`;
    content += `- **scripts/** - Helper scripts and templates\n`;
    content += `- **config/** - Configuration files\n\n`;
    content += `Skills provide domain-specific knowledge, best practices, code templates, and troubleshooting strategies. Think of them as specialized "expert personas" for areas like dbt development, Snowflake operations, or testing frameworks.\n\n`;
    content += `**Key Features:**\n`;
    content += `- Skills can be enabled \`[x]\` or disabled \`[ ]\` individually\n\n`;

    // Merge local skills with remote skills (local takes precedence)
    const localSkillNames = new Set(localSkills.map(s => s.name));
    const mergedSkills = [...localSkills, ...skills.filter(s => !localSkillNames.has(s.name))];

    if (mergedSkills.length === 0) {
      content += 'No skills are currently available. Use the MCP tools to add skill repositories.\n\n';
      content += this.SKILLS_SECTION_END;
      return content;
    }

    content += '**Available Skills:**\n\n';

    // Group and sort skills by source
    const localSkillsList = mergedSkills.filter(s => s.repo_id === -1).sort((a, b) => a.name.localeCompare(b.name));
    const repoMap = new Map(repositories.map(r => [r.id, r]));
    const repoSkillsMap = new Map<number, SkillRecord[]>();
    
    mergedSkills.filter(s => s.repo_id !== -1).forEach(skill => {
      if (!repoSkillsMap.has(skill.repo_id)) {
        repoSkillsMap.set(skill.repo_id, []);
      }
      repoSkillsMap.get(skill.repo_id)!.push(skill);
    });

    // Sort repository IDs by repository name
    const sortedRepoIds = Array.from(repoSkillsMap.keys()).sort((a, b) => 
      (repoMap.get(a)?.name || '').localeCompare(repoMap.get(b)?.name || '')
    );

    // Output local skills first
    if (localSkillsList.length > 0) {
      content += `### Local Skills\n\n`;
      for (const skill of localSkillsList) {
        const checkbox = skill.enabled ? '[x]' : '[ ]';
        content += `- ${checkbox} **[${skill.name}](${skill.skill_path})** - ${skill.description}\n`;
      }
      content += '\n';
    }

    // Output repository skills
    for (const repoId of sortedRepoIds) {
      const repo = repoMap.get(repoId);
      if (!repo) continue;
      
      content += `### ${repo.name}\n\n`;
      const sortedSkills = repoSkillsMap.get(repoId)!.sort((a, b) => a.name.localeCompare(b.name));
      
      for (const skill of sortedSkills) {
        const checkbox = skill.enabled ? '[x]' : '[ ]';
        const skillPath = `.skills/repositories/${repo.name}/${skill.skill_path}`;
        content += `- ${checkbox} **[${skill.name}](${skillPath})** - ${skill.description}\n`;
      }
      content += '\n';
    }

    content += this.SKILLS_SECTION_END;
    return content;
  }
}

