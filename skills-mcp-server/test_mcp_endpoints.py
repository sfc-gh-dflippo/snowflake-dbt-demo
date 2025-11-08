#!/usr/bin/env python3
"""Test MCP server endpoints directly."""

import asyncio
import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing
os.environ['SKILLS_REPOS'] = "https://github.com/sfc-gh-dflippo/snowflake-dbt-demo,https://github.com/anthropics/skills"
os.environ['SKILLS_BRANCHES'] = "main,main"
os.environ['SKILLS_PATHS'] = ".claude/skills,."
os.environ['CACHE_DIR'] = "./.mcp_cache/skills"
os.environ['REFRESH_ON_STARTUP'] = "true"  # Sync repos

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from server import SkillsServer


async def test_server():
    """Test MCP server endpoints."""
    print("=" * 60)
    print("Testing Skills MCP Server Endpoints")
    print("=" * 60)
    
    # Initialize server
    print("\n1. Initializing server...")
    skills_server = SkillsServer()
    await skills_server.initialize()
    print(f"✓ Server initialized with {len(skills_server.skill_manager.skills)} skills")
    
    # Test prompts/list
    print("\n2. Testing prompts/list...")
    prompts = []
    for full_name, skill in skills_server.skill_manager.skills.items():
        prompt_name = f"skill_{full_name.replace('/', '_').replace('-', '_')}"
        prompts.append({
            "name": prompt_name,
            "description": f"{skill.name}: {skill.description[:80]}..."
        })
    
    print(f"✓ Found {len(prompts)} skill prompts")
    print(f"  Sample: {prompts[0]['name']}")
    
    # Test prompts/get
    print("\n3. Testing prompts/get...")
    first_skill_name = list(skills_server.skill_manager.skills.keys())[0]
    prompt_name = f"skill_{first_skill_name.replace('/', '_').replace('-', '_')}"
    
    content = skills_server.skill_manager.get_skill_content(first_skill_name)
    print(f"✓ Retrieved prompt: {prompt_name}")
    print(f"  Content length: {len(content)} characters")
    print(f"  First 100 chars: {content[:100]}...")
    
    # Test resources/list
    print("\n4. Testing resources/list...")
    resources = []
    for full_name, skill in skills_server.skill_manager.skills.items():
        for resource in skill.resources:
            resources.append({
                "uri": f"skill://{full_name}/resource/{resource.relative_path}",
                "name": f"{skill.name}/{resource.name}",
                "mime_type": resource.mime_type,
                "size": resource.size
            })
    
    print(f"✓ Found {len(resources)} resources (scripts, references, configs)")
    if resources:
        print(f"  Sample: {resources[0]['name']}")
        print(f"  URI: {resources[0]['uri']}")
    
    # Test resources/read
    print("\n5. Testing resources/read...")
    if resources:
        test_uri = resources[0]['uri']
        # Parse URI
        path = test_uri[8:]  # Remove "skill://"
        parts = path.split('/')
        full_skill_name = f"{parts[0]}/{parts[1]}"
        resource_path = '/'.join(parts[3:])
        
        content = skills_server.skill_manager.get_skill_resource(
            full_skill_name,
            resource_path
        )
        
        if content:
            try:
                text_content = content.decode('utf-8')
                print(f"✓ Retrieved resource: {test_uri}")
                print(f"  Content length: {len(text_content)} characters")
                print(f"  First 100 chars: {text_content[:100]}...")
            except UnicodeDecodeError:
                print(f"✓ Retrieved binary resource: {test_uri}")
                print(f"  Size: {len(content)} bytes")
        else:
            print(f"✗ Failed to retrieve resource: {test_uri}")
    else:
        print("  (No resources available to test)")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  • Skills (as prompts): {len(prompts)}")
    print(f"  • Resources (scripts/refs): {len(resources)}")
    print(f"  • Total files: {len(prompts) + len(resources)}")
    print("=" * 60)
    
    # Test specific skill examples
    print("\n6. Example Skills Available as Prompts:")
    for i, prompt in enumerate(prompts[:5], 1):
        print(f"  {i}. {prompt['name']}")
        print(f"     {prompt['description']}")
    
    if len(prompts) > 5:
        print(f"  ... and {len(prompts) - 5} more")
    
    # Test specific resources
    if resources:
        print("\n7. Example Resources Available to Fetch:")
        for i, resource in enumerate(resources[:5], 1):
            print(f"  {i}. {resource['name']} ({resource['type']})")
            print(f"     URI: {resource['uri']}")
        
        if len(resources) > 5:
            print(f"  ... and {len(resources) - 5} more")


if __name__ == "__main__":
    asyncio.run(test_server())

