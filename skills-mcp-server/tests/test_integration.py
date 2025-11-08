#!/usr/bin/env python3
"""Integration test script that downloads real repositories and discovers skills."""

import os
import sys
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_sync import sync_all_repositories, GitSyncError
from skill_manager import SkillManager


def test_real_repository_sync():
    """Test syncing real repositories."""
    print("=" * 60)
    print("Integration Test: Real Repository Sync")
    print("=" * 60)
    
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
    
    cache_dir = Path('./test_cache')
    
    try:
        # Clean up any existing test cache
        if cache_dir.exists():
            print(f"Cleaning up existing test cache: {cache_dir}")
            shutil.rmtree(cache_dir)
        
        print(f"\nSyncing {len(repositories)} repositories...")
        print("This may take a moment to download...")
        
        # Sync repositories
        repo_paths = sync_all_repositories(repositories, cache_dir)
        
        print(f"\n✓ Successfully synced {len(repo_paths)} repositories:")
        for repo_name, repo_data in repo_paths.items():
            print(f"  - {repo_name}")
            print(f"    Path: {repo_data['skills_path']}")
        
        # Discover skills
        print(f"\nDiscovering skills...")
        skill_manager = SkillManager()
        skills = skill_manager.discover_skills(repo_paths)
        
        print(f"\n✓ Discovered {len(skills)} skills:")
        
        # Group by repository
        repos = {}
        for full_name, skill in skills.items():
            if skill.repo_name not in repos:
                repos[skill.repo_name] = []
            repos[skill.repo_name].append(skill)
        
        for repo_name in sorted(repos.keys()):
            print(f"\n  {repo_name}:")
            for skill in sorted(repos[repo_name], key=lambda s: s.name):
                print(f"    - {skill.name}")
                print(f"      Description: {skill.description[:80]}...")
                print(f"      Resources: {len(skill.resources)} files")
        
        # Test catalog generation
        print(f"\nGenerating skills catalog...")
        catalog = skill_manager.format_skills_catalog()
        print(f"✓ Catalog generated ({len(catalog)} characters)")
        
        # Show a snippet of the catalog
        print(f"\nCatalog preview (first 500 chars):")
        print("-" * 60)
        print(catalog[:500])
        print("-" * 60)
        
        # Test loading a specific skill
        if skills:
            first_skill_name = list(skills.keys())[0]
            print(f"\nTesting skill content loading: {first_skill_name}")
            content = skill_manager.get_skill_content(first_skill_name)
            if content:
                print(f"✓ Loaded skill content ({len(content)} characters)")
                print(f"  First 200 chars: {content[:200]}...")
            else:
                print(f"✗ Failed to load skill content")
                return False
        
        print("\n" + "=" * 60)
        print("✓ Integration test PASSED")
        print("=" * 60)
        
        return True
        
    except GitSyncError as e:
        print(f"\n✗ Repository sync failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test cache
        if cache_dir.exists():
            print(f"\nCleaning up test cache: {cache_dir}")
            shutil.rmtree(cache_dir)


def main():
    """Run integration test."""
    print("\n" + "=" * 60)
    print("Skills MCP Server - Integration Test")
    print("=" * 60)
    print("\nThis test will:")
    print("1. Download real repositories from GitHub")
    print("2. Discover skills in those repositories")
    print("3. Test skill content loading")
    print("\nNote: Requires internet connection")
    print("=" * 60)
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    success = test_real_repository_sync()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

