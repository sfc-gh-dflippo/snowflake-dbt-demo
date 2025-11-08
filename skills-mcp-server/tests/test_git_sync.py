"""Tests for git_sync module."""

import pytest
from pathlib import Path
from src.git_sync import get_repo_name_from_url


class TestGetRepoNameFromUrl:
    """Tests for get_repo_name_from_url function."""
    
    def test_basic_github_url(self):
        """Test basic GitHub URL."""
        url = "https://github.com/anthropics/skills"
        assert get_repo_name_from_url(url) == "anthropics-skills"
    
    def test_github_url_with_git_suffix(self):
        """Test GitHub URL with .git suffix."""
        url = "https://github.com/anthropics/skills.git"
        assert get_repo_name_from_url(url) == "anthropics-skills"
    
    def test_github_url_with_trailing_slash(self):
        """Test GitHub URL with trailing slash."""
        url = "https://github.com/anthropics/skills/"
        assert get_repo_name_from_url(url) == "anthropics-skills"
    
    def test_different_owner(self):
        """Test with different owner."""
        url = "https://github.com/sfc-gh-dflippo/snowflake-dbt-demo"
        assert get_repo_name_from_url(url) == "sfc-gh-dflippo-snowflake-dbt-demo"


# Note: Integration tests for download_repo_zip and sync_repository
# would require network access and are better suited for integration testing


