"""Skill discovery and management module."""

import logging
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import frontmatter

logger = logging.getLogger(__name__)


@dataclass
class SkillResource:
    """Represents a skill resource file."""
    name: str
    path: Path
    relative_path: str
    mime_type: str
    size: int
    frontmatter_name: Optional[str] = None
    frontmatter_description: Optional[str] = None


@dataclass
class Skill:
    """Represents a discovered skill."""
    name: str
    description: str
    repo_name: str
    skill_path: Path
    skill_file: Path
    resources: List[SkillResource]


class SkillManager:
    """Manages skill discovery and serving."""
    
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        mimetypes.init()
    
    def discover_skills(self, repo_paths: Dict[str, Dict]) -> Dict[str, Skill]:
        """
        Discover all skills from synced repositories.
        
        Args:
            repo_paths: Dictionary of repository metadata from git_sync
            
        Returns:
            Dictionary mapping skill names to Skill objects
        """
        skills = {}
        
        for repo_name, repo_data in repo_paths.items():
            skills_path = repo_data['skills_path']
            
            logger.info(f"Scanning {repo_name} for SKILL.md files in {skills_path}")
            
            # Recursively find all SKILL.md files
            for skill_file in skills_path.rglob('SKILL.md'):
                try:
                    skill = self._parse_skill_file(skill_file, repo_name)
                    if skill:
                        # Use repo-prefixed name to avoid conflicts
                        full_name = f"{repo_name}/{skill.name}"
                        skills[full_name] = skill
                        logger.info(f"Discovered skill: {full_name}")
                except Exception as e:
                    logger.warning(f"Failed to parse {skill_file}: {e}")
        
        self.skills = skills
        return skills
    
    def _parse_skill_file(self, skill_file: Path, repo_name: str) -> Optional[Skill]:
        """
        Parse a SKILL.md file and extract metadata.
        
        Args:
            skill_file: Path to SKILL.md file
            repo_name: Name of repository containing skill
            
        Returns:
            Skill object or None if invalid
        """
        try:
            # Parse frontmatter
            post = frontmatter.load(skill_file)
            
            # Extract required fields
            name = post.get('name')
            description = post.get('description')
            
            if not name or not description:
                logger.warning(f"Skill {skill_file} missing required frontmatter (name/description)")
                return None
            
            # Skill directory is parent of SKILL.md
            skill_path = skill_file.parent
            
            # Discover resources
            resources = self._discover_resources(skill_path)
            
            return Skill(
                name=name,
                description=description,
                repo_name=repo_name,
                skill_path=skill_path,
                skill_file=skill_file,
                resources=resources
            )
            
        except Exception as e:
            logger.error(f"Error parsing {skill_file}: {e}")
            return None
    
    def _discover_resources(self, skill_path: Path) -> List[SkillResource]:
        """
        Discover all resource files in a skill directory.
        
        Args:
            skill_path: Path to skill directory
            
        Returns:
            List of SkillResource objects
        """
        resources = []
        
        # Text-based mime types that might have frontmatter
        text_mimes = [
            'text/',                    # text/plain, text/markdown, text/x-python, etc.
            'application/json',         # JSON files
            'application/xml',          # XML files
            'application/x-yaml',       # YAML with x- prefix
            'application/yaml',         # YAML without x- prefix
            'application/x-sql',        # SQL files
            'application/x-sh',         # Shell scripts
        ]
        
        # Find all files except SKILL.md
        for file_path in skill_path.rglob('*'):
            if file_path.is_file() and file_path.name != 'SKILL.md':
                relative_path = str(file_path.relative_to(skill_path))
                mime_type, _ = mimetypes.guess_type(str(file_path))
                mime_type = mime_type or 'application/octet-stream'
                
                # Try to extract frontmatter if it's a text file
                fm_name = None
                fm_description = None
                if any(mime_type.startswith(prefix) or mime_type == prefix for prefix in text_mimes):
                    try:
                        # Read file content
                        content = file_path.read_text(encoding='utf-8')
                        
                        # Simple universal approach: search for "name:" and "description:" in any line
                        # This works with any comment style (#, //, /*, <!--, """, etc.)
                        lines = content.split('\n')
                        
                        # Only check the first 50 lines for metadata (performance)
                        for line in lines[:50]:
                            line_stripped = line.strip()
                            
                            # Look for name: (case insensitive, with flexible spacing)
                            if 'name:' in line_stripped.lower() and fm_name is None:
                                # Extract everything after "name:"
                                name_idx = line_stripped.lower().find('name:')
                                value = line_stripped[name_idx + 5:].strip()
                                # Remove common trailing characters from comments
                                value = value.rstrip('*/->')
                                # Remove quotes if present
                                value = value.strip('"\'')
                                if value:
                                    fm_name = value
                            
                            # Look for description: (case insensitive, with flexible spacing)
                            if 'description:' in line_stripped.lower() and fm_description is None:
                                # Extract everything after "description:"
                                desc_idx = line_stripped.lower().find('description:')
                                value = line_stripped[desc_idx + 12:].strip()
                                # Remove common trailing characters from comments
                                value = value.rstrip('*/->')
                                # Remove quotes if present
                                value = value.strip('"\'')
                                if value:
                                    fm_description = value
                            
                            # Stop early if we found both
                            if fm_name and fm_description:
                                break
                    except Exception:
                        # Not all text files have frontmatter, that's okay
                        pass
                
                resources.append(SkillResource(
                    name=file_path.name,
                    path=file_path,
                    relative_path=relative_path,
                    mime_type=mime_type,
                    size=file_path.stat().st_size,
                    frontmatter_name=fm_name,
                    frontmatter_description=fm_description
                ))
        
        return resources
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """
        Get a skill by name.
        
        Args:
            skill_name: Name of skill (can be "repo/skill" or just "skill")
            
        Returns:
            Skill object or None if not found
        """
        # Try exact match first
        if skill_name in self.skills:
            return self.skills[skill_name]
        
        # Try finding by skill name only (first match)
        for full_name, skill in self.skills.items():
            if skill.name == skill_name or full_name.endswith(f"/{skill_name}"):
                return skill
        
        return None
    
    def get_skill_content(self, skill_name: str) -> Optional[str]:
        """
        Get raw SKILL.md content.
        
        Args:
            skill_name: Name of skill
            
        Returns:
            Raw file content or None if not found
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return None
        
        try:
            return skill.skill_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to read skill content for {skill_name}: {e}")
            return None
    
    def get_skill_resource(self, skill_name: str, resource_path: str) -> Optional[bytes]:
        """
        Get raw resource file content.
        
        Args:
            skill_name: Name of skill
            resource_path: Relative path to resource within skill directory
            
        Returns:
            Raw file content or None if not found
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return None
        
        # Resolve resource path
        full_path = skill.skill_path / resource_path
        
        # Security check: ensure path is within skill directory
        try:
            full_path = full_path.resolve()
            skill.skill_path.resolve()
            if not str(full_path).startswith(str(skill.skill_path.resolve())):
                logger.warning(f"Attempted directory traversal: {resource_path}")
                return None
        except Exception:
            return None
        
        if not full_path.exists() or not full_path.is_file():
            return None
        
        try:
            return full_path.read_bytes()
        except Exception as e:
            logger.error(f"Failed to read resource {resource_path} for {skill_name}: {e}")
            return None
    
    def list_skills(self, filter_repo: Optional[str] = None) -> List[Dict]:
        """
        List all discovered skills.
        
        Args:
            filter_repo: Optional repository name to filter by
            
        Returns:
            List of skill dictionaries
        """
        results = []
        
        for full_name, skill in self.skills.items():
            if filter_repo and skill.repo_name != filter_repo:
                continue
            
            results.append({
                'name': skill.name,
                'full_name': full_name,
                'description': skill.description,
                'repo': skill.repo_name,
                'uri': f"skill://{full_name}",
                'resource_count': len(skill.resources)
            })
        
        return results
    
    def get_skill_resources_list(self, skill_name: str) -> Optional[List[Dict]]:
        """
        List all resources for a skill.
        
        Args:
            skill_name: Name of skill
            
        Returns:
            List of resource dictionaries or None if skill not found
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return None
        
        full_name = next((name for name, s in self.skills.items() if s == skill), skill.name)
        
        return [
            {
                'name': resource.name,
                'path': resource.relative_path,
                'type': self._classify_resource(resource),
                'uri': f"skill://{full_name}/resource/{resource.relative_path}",
                'mime_type': resource.mime_type,
                'size': resource.size
            }
            for resource in skill.resources
        ]
    
    def _classify_resource(self, resource: SkillResource) -> str:
        """
        Classify a resource by type.
        
        Args:
            resource: SkillResource object
            
        Returns:
            Resource type (script, reference, config, other)
        """
        path_parts = Path(resource.relative_path).parts
        
        if path_parts and path_parts[0] == 'scripts':
            return 'script'
        elif path_parts and path_parts[0] in ('reference', 'references', 'docs'):
            return 'reference'
        elif path_parts and path_parts[0] in ('config', 'configs'):
            return 'config'
        else:
            return 'other'
    
    def format_skills_catalog(self) -> str:
        """
        Generate formatted skills catalog markdown.
        
        Returns:
            Markdown formatted catalog
        """
        if not self.skills:
            return "# Available Skills\n\nNo skills currently available."
        
        lines = [
            "# Available Skills",
            "",
            "The following skills are available for use. To load a skill, reference its URI.",
            ""
        ]
        
        # Group by repository
        repos: Dict[str, List[Skill]] = {}
        for full_name, skill in self.skills.items():
            if skill.repo_name not in repos:
                repos[skill.repo_name] = []
            repos[skill.repo_name].append(skill)
        
        # Format each repository section
        for repo_name in sorted(repos.keys()):
            lines.append(f"## Skills from {repo_name}")
            lines.append("")
            
            for skill in sorted(repos[repo_name], key=lambda s: s.name):
                full_name = f"{repo_name}/{skill.name}"
                lines.append(f"### {skill.name}")
                lines.append(f"**URI:** `skill://{full_name}`  ")
                lines.append(f"**Description:** {skill.description}")
                if skill.resources:
                    lines.append(f"**Resources:** {len(skill.resources)} files available")
                lines.append("")
        
        return "\n".join(lines)


