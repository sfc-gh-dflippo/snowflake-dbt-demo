"""Skills MCP Server main module."""

import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

# Add src directory to path for imports when run as script
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, Prompt

# Handle both module and script imports
try:
    from .git_sync import sync_all_repositories, GitSyncError
    from .skill_manager import SkillManager
except ImportError:
    from git_sync import sync_all_repositories, GitSyncError
    from skill_manager import SkillManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SkillsServer:
    """MCP server for serving skills from Git repositories."""
    
    def __init__(self):
        self.skill_manager = SkillManager()
        self.repositories = {}
        self.cache_dir = Path('./cache')
        
    def parse_config(self) -> dict:
        """Parse configuration from environment variables."""
        repos_str = os.getenv('SKILLS_REPOS', '')
        if not repos_str:
            raise ValueError("SKILLS_REPOS environment variable is required")
        
        repos = [r.strip() for r in repos_str.split(',') if r.strip()]
        
        return {
            'repositories': [
                {
                    'url': url,
                    'branches': ['main', 'master'],  # Try main first, then master
                    'path': '.'  # Search entire repo
                }
                for url in repos
            ]
        }
    
    async def initialize(self, cache_dir: Path):
        """Initialize server by syncing repositories and discovering skills."""
        try:
            config = self.parse_config()
            self.cache_dir = cache_dir
            
            logger.info("Skills MCP Server initializing...")
            logger.info(f"Cache directory: {self.cache_dir}")
            logger.info(f"Repositories: {len(config['repositories'])}")
            
            # Sync repositories
            logger.info("Syncing repositories...")
            self.repositories = sync_all_repositories(
                config['repositories'],
                self.cache_dir
            )
            logger.info(f"Synced {len(self.repositories)} repositories")
            
            # Discover skills
            logger.info("Discovering skills...")
            skills = self.skill_manager.discover_skills(self.repositories)
            logger.info(f"Discovered {len(skills)} skills")
            
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise


async def main():
    """Main entry point for the MCP server."""
    
    # Create temporary directory for cache (auto-cleanup on exit)
    with tempfile.TemporaryDirectory(prefix="skills-mcp-") as temp_dir:
        cache_dir = Path(temp_dir)
        logger.info(f"Using temporary cache directory: {cache_dir}")
        
        # Create server instance
        skills_server = SkillsServer()
        
        # Initialize first to discover skills
        await skills_server.initialize(cache_dir)
        
        # Build server description with skills list
        skills_list = []
        for full_name, skill in skills_server.skill_manager.skills.items():
            skills_list.append(f"- **{skill.name}**: {skill.description}")
        
        server_description = (
            "Skills MCP Server - Provides specialized domain knowledge through structured instruction sets.\n\n"
            f"Available skills ({len(skills_list)}):\n\n" + 
            "\n".join(skills_list)
        )
        
        # Log the skills description for the client
        logger.info("\n" + "="*80)
        logger.info(server_description)
        logger.info("="*80 + "\n")
        
        # Create server
        server = Server("skills-mcp-server")
        
        # Register prompts - individual skills only
        @server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available skill prompts."""
            prompts = []
            
            # First pass: detect name collisions
            skill_names = {}
            for full_name, skill in skills_server.skill_manager.skills.items():
                skill_name = skill.name
                if skill_name not in skill_names:
                    skill_names[skill_name] = []
                skill_names[skill_name].append(full_name)
            
            # Second pass: build prompts with minimal names
            for full_name, skill in skills_server.skill_manager.skills.items():
                skill_name = skill.name
                
                # Use simple name if no collision, otherwise include repo
                if len(skill_names[skill_name]) == 1:
                    base_name = skill_name.replace('-', '_').replace(' ', '_').lower()
                else:
                    base_name = full_name.replace('/', '_').replace('-', '_')
                
                # Add _skill suffix if not already present
                if base_name.endswith('_skill'):
                    prompt_name = base_name
                else:
                    prompt_name = f"{base_name}_skill"
                
                # Build comprehensive description
                skill_description = (
                    f"{skill.name}\n\n"
                    f"{skill.description}"
                )
                
                prompts.append(Prompt(
                    name=prompt_name,
                    description=skill_description,
                    arguments=[]
                ))
            
            return prompts
        
        @server.get_prompt()
        async def get_prompt(name: str, arguments: dict) -> str:
            """Get prompt content for individual skills."""
            if not name.endswith("_skill"):
                raise ValueError(f"Unknown prompt: {name}")
            
            # Remove "_skill" suffix
            skill_id = name[:-6]  # Remove "_skill" suffix
            
            # Try to find matching skill by name or full_name
            for full_name, skill in skills_server.skill_manager.skills.items():
                # Check if it matches simple skill name
                simple_name = skill.name.replace('-', '_').replace(' ', '_').lower()
                if skill_id == simple_name:
                    return skills_server.skill_manager.get_skill_content(full_name)
                
                # Check if it matches full name with repo
                normalized_full_name = full_name.replace('/', '_').replace('-', '_')
                if skill_id == normalized_full_name:
                    return skills_server.skill_manager.get_skill_content(full_name)
            
            raise ValueError(f"Unknown prompt: {name}")
        
        # Register resources - skill-specific resources only (scripts, references, config files)
        @server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available skill resources (scripts, references, config files)."""
            resources = []
            
            # Add individual skill resources (only if they're in subdirectories)
            for full_name, skill in skills_server.skill_manager.skills.items():
                for resource in skill.resources:
                    # Only include resources in subdirectories (references/, scripts/, config/, etc.)
                    # Skip files in the skill root directory
                    if '/' in resource.relative_path or '\\' in resource.relative_path:
                        # Use frontmatter name/description if available
                        if resource.frontmatter_name and resource.frontmatter_description:
                            resource_name = f"{skill.name}/{resource.frontmatter_name}"
                            description = f"{resource.frontmatter_description} ({resource.relative_path})"
                        else:
                            # Fall back to generated description
                            path_parts = resource.relative_path.replace('\\', '/').split('/')
                            folder = path_parts[0] if len(path_parts) > 1 else 'resource'
                            
                            # Determine resource type from folder
                            if 'reference' in folder.lower():
                                resource_type = "Reference documentation"
                            elif 'script' in folder.lower():
                                resource_type = "Helper script"
                            elif 'config' in folder.lower():
                                resource_type = "Configuration file"
                            elif 'example' in folder.lower():
                                resource_type = "Example"
                            elif 'template' in folder.lower():
                                resource_type = "Template"
                            else:
                                resource_type = "Resource"
                            
                            resource_name = f"{skill.name}/{resource.name}"
                            description = f"{resource_type} for {skill.name}: {resource.relative_path}"
                        
                        resources.append(Resource(
                            uri=f"skill://{full_name}/resource/{resource.relative_path}",
                            name=resource_name,
                            description=description,
                            mimeType=resource.mime_type
                        ))
            
            return resources
        
        @server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read resource content for skill-specific resources."""
            # Convert AnyUrl to string if needed
            uri_str = str(uri)
            if not uri_str.startswith("skill://"):
                raise ValueError(f"Invalid URI: {uri_str}")
            
            # Parse URI: skill://repo/skill/resource/path
            path = uri_str[8:]  # Remove "skill://"
            parts = path.split('/')
            
            if len(parts) < 4 or parts[2] != 'resource':
                raise ValueError(f"Invalid resource URI (must include /resource/): {uri_str}")
            
            repo_name = parts[0]
            skill_name = parts[1]
            full_skill_name = f"{repo_name}/{skill_name}"
            resource_path = '/'.join(parts[3:])
            
            content = skills_server.skill_manager.get_skill_resource(
                full_skill_name,
                resource_path
            )
            if content is None:
                raise ValueError(f"Resource not found: {uri_str}")
            
            # Return as text if possible, otherwise base64
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                import base64
                return base64.b64encode(content).decode('ascii')
        
        # Register tools
        @server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="get_skill_resources",
                    description="List additional resources (scripts, references, configs) for a specific skill. The skill itself is automatically available as a prompt - this tool lists supplementary files you can fetch on-demand.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skill_name": {
                                "type": "string",
                                "description": "Name of skill (format: repo/skill or just skill)"
                            }
                        },
                        "required": ["skill_name"]
                    }
                )
            ]
        
        @server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            if name == "get_skill_resources":
                skill_name = arguments.get("skill_name")
                if not skill_name:
                    raise ValueError("skill_name is required")
                
                resources = skills_server.skill_manager.get_skill_resources_list(skill_name)
                if resources is None:
                    raise ValueError(f"Skill not found: {skill_name}")
                
                return [TextContent(
                    type="text",
                    text=str(resources)
                )]
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        # Run server with initialization options
        async with stdio_server() as (read_stream, write_stream):
            init_options = server.create_initialization_options()
            
            # Add server information to initialization
            # The MCP protocol communicates server info through prompts and tools
            # Clients discover available skills by calling list_prompts()
            
            await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

