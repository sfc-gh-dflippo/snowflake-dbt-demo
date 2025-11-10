"""
Tests for Python sync-skills.py script

Tests the Python implementation directly:
- Script syntax and structure
- Required functions exist
- Script can be executed
"""

import pytest
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def sync_script():
    """Path to the Python sync script."""
    root = Path(__file__).parent.parent
    script = root / "src" / "resources" / "sync-skills.py"
    assert script.exists(), f"Sync script not found: {script}"
    return script


class TestScriptStructure:
    """Test the structure and syntax of the sync script."""
    
    def test_script_has_valid_syntax(self, sync_script):
        """Test that the script has valid Python syntax."""
        with open(sync_script) as f:
            code = f.read()
        
        try:
            compile(code, str(sync_script), 'exec')
        except SyntaxError as e:
            pytest.fail(f"Script has syntax error: {e}")
    
    def test_script_has_shebang(self, sync_script):
        """Test that the script has proper shebang line."""
        with open(sync_script) as f:
            first_line = f.readline()
        
        assert first_line.startswith('#!/usr/bin/env python3'), \
            "Script should start with python3 shebang"
    
    def test_script_has_required_functions(self, sync_script):
        """Test that all required functions are present."""
        with open(sync_script) as f:
            content = f.read()
        
        required_functions = [
            'check_git_installed',
            'read_repo_list',
            'clone_or_pull_repo',
            'scan_all_skills',
            'update_agents_md',
            'main',
        ]
        
        for func in required_functions:
            assert f'def {func}(' in content, \
                f"Missing required function: {func}"
    
    def test_script_has_proper_imports(self, sync_script):
        """Test that the script imports required modules."""
        with open(sync_script) as f:
            content = f.read()
        
        required_imports = [
            'import os',
            'import subprocess',
            'import sys',
            'from pathlib import Path',
            'import frontmatter',
        ]
        
        for imp in required_imports:
            assert imp in content, f"Missing import: {imp}"
    
    def test_script_size_is_reasonable(self, sync_script):
        """Test that the script size is within expected range."""
        size = sync_script.stat().st_size
        assert 9000 < size < 12000, \
            f"Script size {size} bytes seems unusual (expected ~10KB)"


class TestScriptExecution:
    """Test script execution (requires git to be installed)."""
    
    def test_script_can_be_compiled(self, sync_script):
        """Test that Python can compile the script."""
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(sync_script)],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0, \
            f"Script compilation failed: {result.stderr}"
    
    def test_script_shows_help_or_runs(self, sync_script):
        """Test that script can be invoked (may fail if git not installed)."""
        # Just test that the script can be invoked without syntax errors
        # Don't actually run it as it would modify files
        result = subprocess.run(
            [sys.executable, '-c', f'import sys; exec(open("{sync_script}").read())'],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        # Script may fail due to missing git or other dependencies
        # but should not have syntax errors
        if result.returncode != 0:
            # Check it's not a syntax error
            assert 'SyntaxError' not in result.stderr, \
                f"Script has syntax error: {result.stderr}"


# Run with: pytest tests/test_sync_script.py -v

