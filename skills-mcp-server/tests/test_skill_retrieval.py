#!/usr/bin/env python3
"""Test skill retrieval functionality - simulates how MCP server returns skills to clients."""

import os
import sys
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_sync import sync_all_repositories, GitSyncError
from skill_manager import SkillManager


def test_skill_catalog_generation():
    """Test generating the skills catalog as it would be sent to agents."""
    print("=" * 70)
    print("TEST: Skills Catalog Generation")
    print("=" * 70)
    
    # Configuration for real repos
    repositories = [
        {
            'url': 'https://github.com/sfc-gh-dflippo/snowflake-dbt-demo',
            'branch': 'main',
            'path': '.claude/skills'
        },
        {
            'url': 'https://github.com/anthropics/skills',
            'branch': 'main',
            'path': '.'
        }
    ]
    
    cache_dir = Path('./test_cache_catalog')
    
    try:
        # Clean up any existing test cache
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        
        print("\n1. Syncing repositories...")
        repo_paths = sync_all_repositories(repositories, cache_dir)
        print(f"   ✓ Synced {len(repo_paths)} repositories")
        
        print("\n2. Discovering skills...")
        skill_manager = SkillManager()
        skills = skill_manager.discover_skills(repo_paths)
        print(f"   ✓ Discovered {len(skills)} skills")
        
        print("\n3. Generating skills catalog (as returned to agent)...")
        print("=" * 70)
        catalog = skill_manager.format_skills_catalog()
        print(catalog)
        print("=" * 70)
        
        print(f"\n✓ Catalog generated: {len(catalog)} characters")
        
        return True, catalog
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        # Clean up
        if cache_dir.exists():
            shutil.rmtree(cache_dir)


def test_list_skills_tool():
    """Test the list_skills tool output."""
    print("\n" + "=" * 70)
    print("TEST: list_skills Tool Output")
    print("=" * 70)
    
    repositories = [
        {
            'url': 'https://github.com/sfc-gh-dflippo/snowflake-dbt-demo',
            'branch': 'main',
            'path': '.claude/skills'
        },
        {
            'url': 'https://github.com/anthropics/skills',
            'branch': 'main',
            'path': '.'
        }
    ]
    
    cache_dir = Path('./test_cache_list')
    
    try:
        # Clean up any existing test cache
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        
        print("\nSyncing and discovering skills...")
        repo_paths = sync_all_repositories(repositories, cache_dir)
        skill_manager = SkillManager()
        skills = skill_manager.discover_skills(repo_paths)
        
        print("\nCalling list_skills() tool...")
        print("=" * 70)
        skills_list = skill_manager.list_skills()
        
        print(f"\nTotal skills: {len(skills_list)}")
        print("\nSkills returned by list_skills tool:\n")
        
        for skill in skills_list:
            print(f"Name: {skill['name']}")
            print(f"Full Name: {skill['full_name']}")
            print(f"Description: {skill['description']}")
            print(f"Repository: {skill['repo']}")
            print(f"URI: {skill['uri']}")
            print(f"Resources: {skill['resource_count']} files")
            print("-" * 70)
        
        return True, skills_list
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        # Clean up
        if cache_dir.exists():
            shutil.rmtree(cache_dir)


def test_skill_content_retrieval():
    """Test retrieving specific skill content."""
    print("\n" + "=" * 70)
    print("TEST: Skill Content Retrieval (On-Demand Loading)")
    print("=" * 70)
    
    repositories = [
        {
            'url': 'https://github.com/sfc-gh-dflippo/snowflake-dbt-demo',
            'branch': 'main',
            'path': '.claude/skills'
        },
        {
            'url': 'https://github.com/anthropics/skills',
            'branch': 'main',
            'path': '.'
        }
    ]
    
    cache_dir = Path('./test_cache_content')
    
    try:
        # Clean up any existing test cache
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        
        print("\nSyncing and discovering skills...")
        repo_paths = sync_all_repositories(repositories, cache_dir)
        skill_manager = SkillManager()
        skills = skill_manager.discover_skills(repo_paths)
        
        if not skills:
            print("✗ No skills discovered")
            return False, None
        
        # Test loading first skill
        first_skill_name = list(skills.keys())[0]
        print(f"\nTesting on-demand loading of skill: {first_skill_name}")
        print("=" * 70)
        
        # Get skill content (simulates agent requesting skill://repo/skill)
        content = skill_manager.get_skill_content(first_skill_name)
        
        if content:
            print(f"✓ Successfully loaded skill content")
            print(f"  Length: {len(content)} characters")
            print(f"\nFirst 500 characters of SKILL.md content:\n")
            print("-" * 70)
            print(content[:500])
            print("-" * 70)
            
            # Test resource listing
            print(f"\nGetting resources for {first_skill_name}...")
            resources = skill_manager.get_skill_resources_list(first_skill_name)
            if resources:
                print(f"✓ Found {len(resources)} resources:")
                for resource in resources[:5]:  # Show first 5
                    print(f"  - {resource['name']} ({resource['type']}, {resource['size']} bytes)")
                    print(f"    URI: {resource['uri']}")
            
            return True, content
        else:
            print(f"✗ Failed to load skill content")
            return False, None
            
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        # Clean up
        if cache_dir.exists():
            shutil.rmtree(cache_dir)


def test_skill_resource_retrieval():
    """Test retrieving skill resources (scripts, references, etc.)."""
    print("\n" + "=" * 70)
    print("TEST: Skill Resource Retrieval")
    print("=" * 70)
    
    repositories = [
        {
            'url': 'https://github.com/anthropics/skills',
            'branch': 'main',
            'path': '.'
        }
    ]
    
    cache_dir = Path('./test_cache_resources')
    
    try:
        # Clean up any existing test cache
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        
        print("\nSyncing and discovering skills...")
        repo_paths = sync_all_repositories(repositories, cache_dir)
        skill_manager = SkillManager()
        skills = skill_manager.discover_skills(repo_paths)
        
        # Find a skill with resources
        skill_with_resources = None
        for full_name, skill in skills.items():
            if len(skill.resources) > 0:
                skill_with_resources = (full_name, skill)
                break
        
        if not skill_with_resources:
            print("✗ No skills with resources found")
            return False, None
        
        full_name, skill = skill_with_resources
        print(f"\nTesting resource retrieval for: {full_name}")
        print(f"Skill has {len(skill.resources)} resources")
        
        # Try to load first resource
        if skill.resources:
            resource = skill.resources[0]
            print(f"\nAttempting to load resource: {resource.relative_path}")
            print(f"  Type: {resource.mime_type}")
            print(f"  Size: {resource.size} bytes")
            
            # Get resource content
            resource_content = skill_manager.get_skill_resource(
                full_name,
                resource.relative_path
            )
            
            if resource_content:
                print(f"✓ Successfully loaded resource")
                print(f"  Actual size: {len(resource_content)} bytes")
                
                # Try to display as text if possible
                try:
                    text_content = resource_content.decode('utf-8')
                    print(f"\nFirst 300 characters of resource:\n")
                    print("-" * 70)
                    print(text_content[:300])
                    print("-" * 70)
                except UnicodeDecodeError:
                    print(f"  (Binary content, not displayable as text)")
                
                return True, resource_content
            else:
                print(f"✗ Failed to load resource")
                return False, None
                
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None
    finally:
        # Clean up
        if cache_dir.exists():
            shutil.rmtree(cache_dir)


def main():
    """Run all skill retrieval tests."""
    print("\n" + "=" * 70)
    print("SKILLS MCP SERVER - SKILL RETRIEVAL TESTS")
    print("=" * 70)
    print("\nThese tests demonstrate how the MCP server returns skills to clients.")
    print("Tests require internet connection to download repositories.")
    print("=" * 70)
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    results = {}
    
    # Test 1: Catalog generation
    print("\n\n")
    success, catalog = test_skill_catalog_generation()
    results['catalog'] = success
    
    # Test 2: List skills tool
    print("\n\n")
    success, skills_list = test_list_skills_tool()
    results['list_skills'] = success
    
    # Test 3: Skill content retrieval
    print("\n\n")
    success, content = test_skill_content_retrieval()
    results['content_retrieval'] = success
    
    # Test 4: Resource retrieval
    print("\n\n")
    success, resource = test_skill_resource_retrieval()
    results['resource_retrieval'] = success
    
    # Summary
    print("\n\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30s} {status}")
    
    all_passed = all(results.values())
    print("=" * 70)
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed. ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())


