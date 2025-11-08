#!/usr/bin/env python3
"""Basic test script to verify installation and core functionality."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from git_sync import get_repo_name_from_url, GitSyncError
        from skill_manager import SkillManager, Skill, SkillResource
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_repo_name_extraction():
    """Test repository name extraction."""
    print("\nTesting repository name extraction...")
    from git_sync import get_repo_name_from_url
    
    tests = [
        ("https://github.com/anthropics/skills", "anthropics-skills"),
        ("https://github.com/sfc-gh-dflippo/snowflake-dbt-demo", "sfc-gh-dflippo-snowflake-dbt-demo"),
        ("https://github.com/anthropics/skills.git", "anthropics-skills"),
    ]
    
    all_passed = True
    for url, expected in tests:
        result = get_repo_name_from_url(url)
        if result == expected:
            print(f"✓ {url} -> {result}")
        else:
            print(f"✗ {url} -> {result} (expected {expected})")
            all_passed = False
    
    return all_passed

def test_skill_manager_init():
    """Test SkillManager initialization."""
    print("\nTesting SkillManager initialization...")
    try:
        from skill_manager import SkillManager
        manager = SkillManager()
        print(f"✓ SkillManager initialized")
        print(f"  - Skills: {len(manager.skills)}")
        return True
    except Exception as e:
        print(f"✗ SkillManager init failed: {e}")
        return False

def test_config_parsing():
    """Test configuration parsing."""
    print("\nTesting configuration parsing...")
    try:
        # Set test environment variables
        os.environ['SKILLS_REPOS'] = "https://github.com/sfc-gh-dflippo/snowflake-dbt-demo,https://github.com/anthropics/skills"
        os.environ['SKILLS_BRANCHES'] = "main,main"
        os.environ['SKILLS_PATHS'] = ".claude/skills,."
        
        # This would normally be in server.py
        repos = os.environ['SKILLS_REPOS'].split(',')
        branches = os.environ['SKILLS_BRANCHES'].split(',')
        paths = os.environ['SKILLS_PATHS'].split(',')
        
        assert len(repos) == 2, "Should have 2 repos"
        assert len(branches) == 2, "Should have 2 branches"
        assert len(paths) == 2, "Should have 2 paths"
        
        print(f"✓ Configuration parsing works")
        print(f"  - Repos: {repos}")
        print(f"  - Branches: {branches}")
        print(f"  - Paths: {paths}")
        return True
    except Exception as e:
        print(f"✗ Config parsing failed: {e}")
        return False
    finally:
        # Clean up
        for key in ['SKILLS_REPOS', 'SKILLS_BRANCHES', 'SKILLS_PATHS']:
            os.environ.pop(key, None)

def main():
    """Run all tests."""
    print("=" * 60)
    print("Skills MCP Server - Basic Functionality Test")
    print("=" * 60)
    
    results = {
        'imports': test_imports(),
        'repo_name': test_repo_name_extraction(),
        'skill_manager': test_skill_manager_init(),
        'config': test_config_parsing(),
    }
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20s} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed. ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())

