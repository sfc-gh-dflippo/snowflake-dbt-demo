"""Git repository synchronization module."""

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Dict
from urllib.request import urlretrieve
from urllib.error import URLError

logger = logging.getLogger(__name__)


class GitSyncError(Exception):
    """Exception raised for git sync errors."""
    pass


def get_repo_name_from_url(url: str) -> str:
    """
    Extract repository name from GitHub URL.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Repository name (e.g., "anthropic-skills")
        
    Example:
        >>> get_repo_name_from_url("https://github.com/anthropics/skills")
        'anthropic-skills'
    """
    # Remove .git suffix if present
    url = url.rstrip('/').replace('.git', '')
    # Extract owner/repo
    parts = url.split('/')
    if len(parts) >= 2:
        owner = parts[-2]
        repo = parts[-1]
        return f"{owner}-{repo}"
    return parts[-1]


def download_repo_zip(url: str, branches: list, cache_path: Path) -> tuple[Path, str]:
    """
    Download repository as ZIP file from GitHub, trying multiple branches.
    
    Args:
        url: GitHub repository URL
        branches: List of branch names to try (in order)
        cache_path: Path to cache directory for this repository
        
    Returns:
        Tuple of (Path to extracted repository directory, branch name that worked)
        
    Raises:
        GitSyncError: If download or extraction fails for all branches
    """
    repo_name = get_repo_name_from_url(url)
    
    last_error = None
    for branch in branches:
        # Construct ZIP download URL
        # Format: https://github.com/owner/repo/archive/refs/heads/branch.zip
        if 'github.com' in url:
            zip_url = f"{url.rstrip('/')}/archive/refs/heads/{branch}.zip"
        else:
            raise GitSyncError(f"Unsupported repository URL: {url}")
        
        logger.info(f"Trying to download {repo_name} from branch '{branch}'")
        
        try:
            # Download to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                tmp_path = Path(tmp_file.name)
                
            urlretrieve(zip_url, tmp_path)
            logger.info(f"Downloaded {repo_name} from branch '{branch}'")
            
            # Extract to temporary directory first to avoid conflicts
            with tempfile.TemporaryDirectory() as temp_extract_dir:
                temp_extract_path = Path(temp_extract_dir)
                
                with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                    # Extract all files to temp directory
                    zip_ref.extractall(temp_extract_path)
                    
                # GitHub ZIPs create a subdirectory like "repo-branch"
                # Find the extracted directory
                extracted_dirs = [d for d in temp_extract_path.iterdir() if d.is_dir()]
                if not extracted_dirs:
                    raise GitSyncError(f"No directory found after extracting {repo_name}")
                    
                extracted_dir = extracted_dirs[0]
                
                # Move to final location
                cache_path.mkdir(parents=True, exist_ok=True)
                final_path = cache_path / repo_name
                if final_path.exists():
                    shutil.rmtree(final_path)
                    
                shutil.move(str(extracted_dir), str(final_path))
            
            # Clean up temp file
            tmp_path.unlink()
            
            logger.info(f"Successfully extracted {repo_name} from branch '{branch}' to {final_path}")
            return final_path, branch
            
        except (URLError, zipfile.BadZipFile, Exception) as e:
            last_error = e
            logger.warning(f"Failed to download {repo_name} from branch '{branch}': {e}")
            continue
    
    # If we get here, all branches failed
    raise GitSyncError(f"Failed to download {repo_name} from any branch ({', '.join(branches)}). Last error: {last_error}")


def sync_repository(url: str, branches: list, skills_path: str, cache_dir: Path) -> Dict[str, Path]:
    """
    Sync a single repository.
    
    Args:
        url: Repository URL
        branches: List of branch names to try
        skills_path: Path to skills within repository
        cache_dir: Base cache directory
        
    Returns:
        Dictionary with repository metadata and paths
        
    Raises:
        GitSyncError: If sync fails
    """
    repo_name = get_repo_name_from_url(url)
    repo_cache_path = cache_dir / repo_name
    
    try:
        # Download and extract (tries multiple branches)
        extracted_path, successful_branch = download_repo_zip(url, branches, cache_dir)
        
        # Resolve skills path
        full_skills_path = extracted_path / skills_path if skills_path != '.' else extracted_path
        
        if not full_skills_path.exists():
            logger.warning(f"Skills path {skills_path} not found in {repo_name}")
            full_skills_path = extracted_path
        
        return {
            'name': repo_name,
            'url': url,
            'branch': successful_branch,
            'repo_path': extracted_path,
            'skills_path': full_skills_path
        }
        
    except GitSyncError:
        raise
    except Exception as e:
        raise GitSyncError(f"Failed to sync {repo_name}: {e}")


def sync_all_repositories(repositories: list, cache_dir: Path) -> Dict[str, Dict]:
    """
    Sync all configured repositories.
    
    Args:
        repositories: List of repository configurations
        cache_dir: Base cache directory
        
    Returns:
        Dictionary mapping repository names to their metadata and paths
        
    Raises:
        GitSyncError: If any repository fails to sync
    """
    results = {}
    errors = []
    
    for repo_config in repositories:
        url = repo_config['url']
        branches = repo_config.get('branches', ['main', 'master'])
        skills_path = repo_config.get('path', '.')
        
        try:
            result = sync_repository(url, branches, skills_path, cache_dir)
            results[result['name']] = result
            logger.info(f"Successfully synced {result['name']}")
        except GitSyncError as e:
            logger.error(f"Failed to sync {url}: {e}")
            errors.append(str(e))
    
    if errors and not results:
        raise GitSyncError(f"All repositories failed to sync: {', '.join(errors)}")
    
    return results

