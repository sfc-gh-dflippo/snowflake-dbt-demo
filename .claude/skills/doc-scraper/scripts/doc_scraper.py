#!/usr/bin/env python3
"""
Snowflake Documentation Scraper v1.1

Single-file scraper for extracting Snowflake documentation and generating AI skills.
Scrapes any section of docs.snowflake.com, converts to Markdown, and auto-generates
a comprehensive SKILL.md file.

Usage:
    python doc_scraper.py --output-dir=./snowflake-docs
    doc-scraper --output-dir=./snowflake-docs  (after install)
"""

import platform
import shutil
import subprocess
import sys
from pathlib import Path

# ============================================================================
# AUTO-INSTALL BOOTSTRAP (runs before other imports)
# ============================================================================


def get_platform() -> str:
    """Detect current platform."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "linux"


def is_running_as_script() -> bool:
    """Check if running as a direct Python script vs installed uv tool."""
    return sys.argv[0].endswith(".py")


def install_uv() -> bool:
    """Attempt to install uv. Returns True if successful."""
    plat = get_platform()
    print("Installing uv...")

    try:
        if plat == "windows":
            subprocess.run(
                [
                    "powershell",
                    "-ExecutionPolicy",
                    "ByPass",
                    "-c",
                    "irm https://astral.sh/uv/install.ps1 | iex",
                ],
                check=True,
                timeout=120,
            )
        else:  # macOS and Linux
            subprocess.run(
                ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"],
                check=True,
                timeout=120,
            )
        print("  ✓ uv installed successfully")
        return True
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
    ) as e:
        print(f"  ✗ Failed to install uv: {e}")
        return False


def check_and_install_uv() -> None:
    """Check if uv is installed, attempt to install if not."""
    if shutil.which("uv"):
        return

    if not install_uv():
        plat = get_platform()
        print("\nManual installation required. Run:")
        if plat == "windows":
            print(
                '  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
            )
        else:
            print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("\nThen restart your terminal and run this script again.")
        sys.exit(1)

    # Refresh PATH to find newly installed uv
    if not shutil.which("uv"):
        print("\nuv was installed but not found in PATH.")
        print("Please restart your terminal and run this script again.")
        sys.exit(1)


def install_self_as_uv_tool() -> None:
    """Install this package as a uv tool and exit."""
    # Find the package directory (parent of scripts/)
    script_path = Path(__file__).resolve()
    package_dir = script_path.parent.parent  # scripts/ -> doc-scraper/

    print(f"Installing doc-scraper as uv tool from {package_dir}...")
    try:
        subprocess.run(
            ["uv", "tool", "install", "--force", str(package_dir)],
            check=True,
            timeout=300,
        )
        print("\n✓ doc-scraper installed successfully!")
        print("\nRun 'doc-scraper --help' to see available options.")
        print("Example: doc-scraper --output-dir=./snowflake-docs")
        sys.exit(0)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n✗ Failed to install doc-scraper: {e}")
        print("\nTry installing manually:")
        print(f"  uv tool install {package_dir}")
        sys.exit(1)


# Bootstrap: if running as script, install uv and self as tool
if is_running_as_script():
    check_and_install_uv()
    install_self_as_uv_tool()


# ============================================================================
# MAIN IMPORTS (only reached when running as installed tool)
# ============================================================================

import json
import logging
import os
import re
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Any, Dict, List, Optional, Tuple, cast
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import click
import frontmatter
import requests
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

# ============================================================================
# CONFIGURATION & LOGGING
# ============================================================================

SCRAPER_VERSION = "1.1.0"
_rate_limiter_lock = threading.Lock()


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Configure logging for the scraper."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    handlers: List[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)


logger = get_logger(__name__)


def load_config(
    config_path: Optional[Path] = None, output_dir: Optional[str] = None
) -> dict:
    """Load scraper configuration from YAML.

    Priority:
    1. Explicit config_path if provided
    2. Config in output_dir/scraper_config.yaml
    3. Embedded config in scripts/scraper_config.yaml

    On first run, copies embedded config to output_dir for customization.
    """
    embedded_config = Path(__file__).parent / "scraper_config.yaml"

    if config_path is None:
        # Check output directory first
        if output_dir:
            output_config = Path(output_dir) / "scraper_config.yaml"

            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Copy embedded config to output dir on first run (visible, not hidden)
            if not output_config.exists():
                import shutil

                shutil.copy2(embedded_config, output_config)
                logger.info(f"Created config file: {output_config}")

            config_path = output_config

        # Fall back to embedded config
        if config_path is None or not config_path.exists():
            config_path = embedded_config

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        if not isinstance(config, dict):
            return {}
        return config


# ============================================================================
# DATABASE MANAGER
# ============================================================================


class ScraperDatabase:
    """
    SQLite database manager for tracking scraping progress and caching.
    Much more memory-efficient than keeping everything in memory.
    """

    def __init__(self, db_path: str = ".cache/scraper.db"):
        """Initialize database connection and create tables."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = Lock()
        self._init_db()

    def _init_db(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scraped_pages (
                    url TEXT PRIMARY KEY,
                    scraped_at TEXT NOT NULL,
                    status TEXT DEFAULT 'success',
                    file_path TEXT,
                    title TEXT,
                    content_hash TEXT
                )
            """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_scraped_at
                ON scraped_pages(scraped_at)
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scraping_session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    base_path TEXT,
                    pages_scraped INTEGER DEFAULT 0,
                    pages_failed INTEGER DEFAULT 0
                )
            """
            )
            conn.commit()

    def should_scrape_url(self, url: str, expiration_days: int = 7) -> bool:
        """Check if URL needs to be scraped (not in cache or expired)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT scraped_at FROM scraped_pages WHERE url = ?", (url,)
                )
                row = cursor.fetchone()

                if not row:
                    return True

                # Check if cache entry is expired
                try:
                    scraped_time = datetime.fromisoformat(row[0])
                    expiration = scraped_time + timedelta(days=expiration_days)

                    if datetime.now(timezone.utc) > expiration:
                        return True

                    return False
                except Exception:
                    return True

    def mark_url_scraped(
        self,
        url: str,
        file_path: Optional[str] = None,
        title: Optional[str] = None,
        status: str = "success",
    ):
        """Mark URL as scraped with current timestamp."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO scraped_pages
                    (url, scraped_at, status, file_path, title)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        url,
                        datetime.now(timezone.utc).isoformat(),
                        status,
                        file_path,
                        title,
                    ),
                )
                conn.commit()

    def mark_url_failed(self, url: str, error: Optional[str] = None):
        """Mark URL as failed."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO scraped_pages
                    (url, scraped_at, status)
                    VALUES (?, ?, ?)
                """,
                    (
                        url,
                        datetime.now(timezone.utc).isoformat(),
                        f"failed: {error}" if error else "failed",
                    ),
                )
                conn.commit()

    def is_url_visited(self, url: str) -> bool:
        """Check if URL has been visited in current session."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT 1 FROM scraped_pages WHERE url = ? LIMIT 1", (url,)
                )
                return cursor.fetchone() is not None

    def get_stats(self) -> Dict[str, int]:
        """Get scraping statistics."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT
                        COUNT(*) as total,
                        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                        SUM(CASE WHEN status LIKE 'failed%' THEN 1 ELSE 0 END) as failed
                    FROM scraped_pages
                """
                )
                row = cursor.fetchone()
                return {
                    "total": row[0] or 0,
                    "success": row[1] or 0,
                    "failed": row[2] or 0,
                }

    def get_all_scraped_urls(self) -> List[str]:
        """Get all successfully scraped URLs (for SKILL.md generation)."""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    SELECT url, title, file_path
                    FROM scraped_pages
                    WHERE status = 'success' AND file_path IS NOT NULL
                    ORDER BY url
                """
                )
                return cursor.fetchall()

    def preload_from_existing_files(self, output_dir: Path, logger=None):
        """
        Pre-populate database from existing markdown files in output directory.
        Reads front-matter to extract URL, title, and timestamps.
        """
        if not output_dir.exists():
            return

        if logger:
            logger.info(f"Pre-loading database from existing files in {output_dir}...")

        md_files = [f for f in output_dir.rglob("*.md") if f.name != "SKILL.md"]
        loaded_count = 0
        skipped_count = 0

        for md_file in md_files:
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    import frontmatter

                    post = frontmatter.load(f)

                # Extract metadata from front-matter
                url = post.metadata.get("source_url")
                title = post.metadata.get("title")
                scraped_at = post.metadata.get("last_scraped")

                if not url or not isinstance(url, str):
                    skipped_count += 1
                    continue

                # Check if already in database
                if self.is_url_visited(url):
                    skipped_count += 1
                    continue

                # Add to database with original timestamp if available
                with self.lock:
                    with sqlite3.connect(self.db_path) as conn:
                        conn.execute(
                            """
                            INSERT OR REPLACE INTO scraped_pages
                            (url, scraped_at, status, file_path, title)
                            VALUES (?, ?, ?, ?, ?)
                        """,
                            (
                                url,
                                scraped_at or datetime.now(timezone.utc).isoformat(),
                                "success",
                                str(md_file),
                                title,
                            ),
                        )
                        conn.commit()

                loaded_count += 1

            except Exception as e:
                if logger:
                    logger.debug(f"Could not load {md_file}: {e}")
                skipped_count += 1
                continue

        if logger:
            logger.info(
                f"Pre-loaded {loaded_count} existing files into database ({skipped_count} skipped)"
            )

    def close(self):
        """Close database connection (cleanup)."""
        # SQLite connections are per-thread, so nothing to close explicitly
        pass


# ============================================================================
# SNOWFLAKE DOCUMENTATION SCRAPER
# ============================================================================


class SnowflakeDocsScraper:
    """
    Generic scraper for Snowflake documentation.
    Handles URL discovery, fetching, conversion, and file organization.
    """

    def __init__(
        self,
        config_path: Optional[Path] = None,
        output_dir: str = ".claude/skills/snowflake-docs",
        base_path: str = "/en/",
    ):
        """Initialize the scraper."""
        self.output_dir = output_dir
        self.base_path = base_path

        # Load config (checks output_dir first, then falls back to embedded)
        self.config = load_config(config_path, output_dir)
        self.session = self._create_session()

        # Initialize database in output directory (memory-efficient!)
        output_path = Path(self.output_dir)
        cache_dir = output_path / ".cache"
        self.db = ScraperDatabase(db_path=str(cache_dir / "scraper.db"))

        # Pre-load database from existing files (if any)
        if output_path.exists():
            self.db.preload_from_existing_files(output_path, logger)

        # Spider-specific attributes
        self.url_queue = []  # Queue of URLs to scrape (kept small in memory)
        self.base_domain = "docs.snowflake.com"

        # Spider path restrictions from config
        spider_config = self.config.get("spider", {})
        self.allowed_paths = spider_config.get("allowed_paths", ["/en/"])
        self.blocked_patterns = spider_config.get("blocked_patterns", [])
        self.max_pages = spider_config.get("max_pages", 1000)
        self.max_queue_size = spider_config.get("max_queue_size", 500)

        # Scraped pages tracking
        self.expiration_days = self.config.get("scraped_pages", {}).get(
            "expiration_days", 7
        )
        self.max_concurrent_threads = self.config["rate_limiting"].get(
            "max_concurrent_threads", 4
        )

        # Thread safety
        self.file_write_lock = Lock()
        self.stats_lock = Lock()

        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_time": 0.0,
            "pages_scraped": 0,
            "links_discovered": 0,
        }

        # Rate limiting config
        self.rate_limit_calls = self.config["rate_limiting"]["requests_per_second"]
        self.rate_limit_period = self.config["rate_limiting"]["period"]
        self.max_retries = self.config["retry_logic"]["max_retries"]
        self.backoff_factor = self.config["retry_logic"]["backoff_factor"]
        self.timeout = self.config["retry_logic"]["timeout"]
        self.user_agent = self.config["user_agent"]

        # Log existing cached pages
        db_stats = self.db.get_stats()
        logger.info(
            f"Initialized SnowflakeDocsScraper v{SCRAPER_VERSION} (base_path: {base_path})"
        )
        total_cached = db_stats["total"]
        success_count = db_stats["success"]
        failed_count = db_stats["failed"]
        logger.info(
            f"Database: {total_cached} pages cached ({success_count} success, {failed_count} failed)"
        )

    def _create_session(self) -> requests.Session:
        """Create requests.Session with retry logic."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.config["retry_logic"]["max_retries"],
            backoff_factor=self.config["retry_logic"]["backoff_factor"],
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(
            max_retries=cast(Any, retry_strategy), pool_connections=10, pool_maxsize=20
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def discover_urls(self, use_cache: bool = True) -> Dict[str, Dict[str, List[str]]]:
        """Discover and categorize URLs from sitemap."""
        cache_dir = Path(self.output_dir) / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = cache_dir / "sitemap_cache.json"

        if use_cache and cache_file.exists():
            logger.info("Loading URLs from cache...")
            with open(cache_file, "r") as f:
                return json.load(f)

        logger.info("Fetching sitemap...")
        sitemap_url = self.config["sitemap_url"]
        response = self.session.get(sitemap_url, timeout=30)
        response.raise_for_status()

        xml_content = response.content
        all_urls = self._parse_sitemap_xml(xml_content)
        filtered_urls = self._filter_urls_by_base_path(all_urls)
        categorized = self._categorize_urls(filtered_urls)

        # Cache results
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(categorized, f, indent=2)

        logger.info(
            f"Discovered {len(filtered_urls)} URLs across {len(categorized)} categories"
        )
        return categorized

    def _parse_sitemap_xml(self, xml_content: bytes) -> List[str]:
        """Parse XML sitemap and extract URLs."""
        tree = ElementTree.fromstring(xml_content)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [
            loc.text.strip() for loc in tree.findall(".//ns:loc", namespace) if loc.text
        ]
        return urls

    def _filter_urls_by_base_path(self, urls: List[str]) -> List[str]:
        """Filter URLs by configured base path."""
        pattern = re.escape(self.base_path)
        filtered = [url for url in urls if re.search(pattern, url)]
        logger.info(
            f"Filtered {len(filtered)} URLs matching '{self.base_path}' from {len(urls)} total"
        )
        return filtered

    def _categorize_urls(self, urls: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Categorize URLs by database and topic."""
        categorized = {}

        for url in urls:
            parsed = urlparse(url)
            segments = [s for s in parsed.path.split("/") if s]

            # Extract database/category from URL
            matched_db = None
            if "translation-references" in segments:
                idx = segments.index("translation-references")
                if idx + 1 < len(segments):
                    matched_db = segments[idx + 1]
            elif len(segments) > 3:
                matched_db = (
                    segments[-2]
                    if segments[-1] not in ["README", "readme"]
                    else segments[-3]
                )

            if not matched_db:
                matched_db = "general"

            # Initialize database entry
            if matched_db not in categorized:
                categorized[matched_db] = {"urls": []}

            categorized[matched_db]["urls"].append(url)

        return categorized

    @sleep_and_retry
    @limits(calls=10, period=1)
    def _rate_limited_get(self, url: str) -> requests.Response:
        """Rate-limited HTTP GET with thread safety."""
        with _rate_limiter_lock:
            return self.session.get(
                url, headers={"User-Agent": self.user_agent}, timeout=self.timeout
            )

    def fetch_and_convert(
        self, url: str
    ) -> Optional[Tuple[str, Dict[str, Any], List[str]]]:
        """Fetch URL, convert to Markdown, and extract links."""
        start_time = time.time()

        try:
            response = self._rate_limited_get(url)
            assert response is not None  # Type guard: decorators preserve return type
            response.raise_for_status()

            elapsed = time.time() - start_time
            with self.stats_lock:
                self.stats["total_requests"] += 1
                self.stats["successful_requests"] += 1
                self.stats["total_time"] += elapsed

            logger.info(
                f"Fetched {url} ({len(response.content)} bytes, {elapsed:.2f}s)"
            )

            # Parse HTML
            soup = BeautifulSoup(response.content, "lxml")

            # Extract internal links for spidering
            internal_links = self._extract_internal_links(soup, url)
            self.stats["links_discovered"] += len(internal_links)

            # Convert to Markdown
            main_content = soup.find("main") or soup.find("article") or soup.body

            if main_content:
                markdown_content = md(str(main_content), heading_style="ATX")
            else:
                markdown_content = md(str(soup), heading_style="ATX")

            # Fix relative links in markdown content
            markdown_content = self._fix_markdown_links(markdown_content, url)

            # Extract metadata
            metadata = {
                "title": self._extract_title(soup),
                "description": self._extract_description(soup),
                "source_url": url,
                "last_scraped": datetime.now(timezone.utc).isoformat(),
                "scraper_version": SCRAPER_VERSION,
                "auto_generated": True,
            }

            return markdown_content, metadata, internal_links

        except Exception as e:
            with self.stats_lock:
                self.stats["total_requests"] += 1
                self.stats["failed_requests"] += 1
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from HTML."""
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        h1_tag = soup.find("h1")
        if h1_tag:
            return h1_tag.get_text().strip()

        return "Untitled"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract description from HTML."""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            content = meta_desc.get("content")
            if isinstance(content, str):
                return content.strip()

        p_tag = soup.find("p")
        if p_tag:
            return " ".join(p_tag.get_text().split())[:200]

        return "Reference documentation from Snowflake"

    def _is_url_allowed(self, url: str) -> bool:
        """Check if a URL is allowed based on path restrictions."""
        parsed = urlparse(url)
        path = parsed.path

        # Check if path starts with any allowed path
        if not any(path.startswith(allowed) for allowed in self.allowed_paths):
            return False

        # Check if path matches any blocked pattern
        if any(blocked in path for blocked in self.blocked_patterns):
            return False

        return True

    def _extract_internal_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all internal links from HTML that point to docs.snowflake.com and pass filters."""
        links = set()

        for a_tag in soup.find_all("a", href=True):
            href_attr = a_tag["href"]
            href = (
                href_attr.strip()
                if isinstance(href_attr, str)
                else str(href_attr[0]).strip() if href_attr else ""
            )

            # Skip anchors, external links, and non-http links
            if not href or href.startswith("#") or href.startswith("mailto:"):
                continue

            # Convert relative URLs to absolute
            if href.startswith("/"):
                full_url = f"https://{self.base_domain}{href}"
            elif href.startswith("http"):
                full_url = href
            else:
                # Relative path
                full_url = urljoin(base_url, href)

            # Only keep links to the same domain
            parsed = urlparse(full_url)
            if parsed.netloc == self.base_domain:
                # Normalize URL (remove fragments, trailing slashes for non-root)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url.endswith("/") and clean_url.count("/") > 3:
                    clean_url = clean_url.rstrip("/")

                # Check if URL is allowed based on path restrictions
                if self._is_url_allowed(clean_url):
                    links.add(clean_url)
                else:
                    logger.debug(f"Blocked URL (outside allowed paths): {clean_url}")

        return list(links)

    def _fix_markdown_links(self, content: str, source_url: str) -> str:
        """Fix relative links in markdown content to work locally."""
        # Pattern to match markdown links: [text](url)
        link_pattern = r"\[([^\]]+)\]\((/en/[^\)]+)\)"

        def replace_link(match):
            text = match.group(1)
            link_url = match.group(2).strip()

            # Remove any title attributes (e.g., "Overview")
            if '"' in link_url:
                link_url = link_url.split('"')[0].strip()

            # Convert to relative path since we're now spidering all linked pages
            try:
                full_url = f"https://docs.snowflake.com{link_url}"
                target_path = self._get_output_filepath(full_url)
                source_path = self._get_output_filepath(source_url)

                # Calculate relative path from source to target
                relative = os.path.relpath(target_path, source_path.parent)

                return f"[{text}]({relative})"
            except Exception:
                # If we can't resolve it, keep as absolute URL to Snowflake
                return f"[{text}](https://docs.snowflake.com{link_url})"

        return re.sub(link_pattern, replace_link, content)

    def save_file(self, content: str, metadata: Dict[str, Any], url: str) -> Path:
        """Save content with front-matter to file (thread-safe)."""
        output_path = self._get_output_filepath(url)

        with self.file_write_lock:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create front-matter file
            post = frontmatter.Post(content)
            post.metadata = metadata

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(frontmatter.dumps(post))

            logger.info(f"Saved file: {output_path}")

        # Mark as scraped in database after successful save
        self.db.mark_url_scraped(url, str(output_path), metadata.get("title"))

        return output_path

    def _get_output_filepath(self, url: str) -> Path:
        """Generate output filepath from URL, preserving full path from server root."""
        parsed = urlparse(url)
        # Remove leading slash and preserve full path
        path = parsed.path.lstrip("/")

        # Transform certain paths for better organization
        # Move guides-overview-* files into guides/ folder
        if path.startswith("en/guides-overview-"):
            filename = path.replace("en/guides-overview-", "")
            path = f"en/guides/overview-{filename}"
        elif path == "en/guides":
            path = "en/guides/README"

        # Move user-guide-* files into user-guide/ folder
        if (
            path.startswith("en/user-guide-") and "/" not in path[3:]
        ):  # Only root level files
            filename = path.replace("en/user-guide-", "")
            path = f"en/user-guide/{filename}"

        # Ensure .md extension
        if not path.endswith(".md"):
            if path.endswith("/"):
                path = path + "README.md"
            else:
                path = path + ".md"

        return Path(self.output_dir) / path

    def _process_single_url(self, url: str) -> Optional[Tuple[Path, List[str]]]:
        """Process a single URL (fetch, convert, save). Returns (output_path, new_links)."""
        # Check if we should skip this URL (already scraped recently)
        if not self.db.should_scrape_url(url, self.expiration_days):
            logger.info(f"Skipping (cached): {url}")
            return None

        result = self.fetch_and_convert(url)
        if result:
            content, metadata, internal_links = result
            output_path = self.save_file(content, metadata, url)

            with self.stats_lock:
                self.stats["pages_scraped"] += 1

            return (output_path, internal_links)
        return None

    def scrape_urls(
        self, urls: List[str], spider: bool = False, spider_depth: int = 1
    ) -> List[Path]:
        """
        Scrape URLs with multi-threading. If spider=True, follow internal links up to specified depth.

        Args:
            urls: List of seed URLs to start with
            spider: If True, follow internal links
            spider_depth: Maximum depth to spider (0=seeds only, 1=+direct links, 2=+links from those, etc.)
        """
        output_files = []
        pages_processed = 0

        if spider:
            # Multi-threaded spider mode with depth control
            # Track depth for each URL (seeds are depth 0)
            url_depths = {url: 0 for url in urls}
            self.url_queue = list(urls)

            logger.info(f"Starting spider with {len(self.url_queue)} seed URLs")
            logger.info(
                f"Spider depth: {spider_depth} (0=seeds only, 1=+links from seeds, etc.)"
            )

            with ThreadPoolExecutor(
                max_workers=self.max_concurrent_threads
            ) as executor:
                while self.url_queue:
                    # Get next batch of URLs to process
                    batch_size = min(self.max_concurrent_threads, len(self.url_queue))
                    batch = []

                    for _ in range(batch_size):
                        if not self.url_queue:
                            break
                        url = self.url_queue.pop(0)

                        # Skip if already visited (check database)
                        if self.db.is_url_visited(url):
                            continue

                        # Check max pages limit
                        if pages_processed >= self.max_pages:
                            logger.warning(
                                f"Reached max pages limit ({self.max_pages}). Stopping spider."
                            )
                            return output_files

                        batch.append(url)

                    if not batch:
                        break

                    # Process batch in parallel
                    futures = {
                        executor.submit(self._process_single_url, url): url
                        for url in batch
                    }

                    for future in as_completed(futures):
                        url = futures[future]
                        try:
                            result = future.result()
                            if result:
                                output_path, internal_links = result
                                output_files.append(output_path)
                                pages_processed += 1

                                # Get current depth and check if we should follow links
                                current_depth = url_depths.get(url, 0)
                                if current_depth < spider_depth:
                                    # Add new links to queue with depth = current + 1
                                    new_links = [
                                        link
                                        for link in internal_links
                                        if link not in url_depths  # Not seen before
                                        and link not in self.url_queue
                                    ]

                                    # Assign depth to new links
                                    for link in new_links:
                                        url_depths[link] = current_depth + 1

                                    # Limit queue growth
                                    available_slots = self.max_queue_size - len(
                                        self.url_queue
                                    )
                                    if available_slots > 0:
                                        links_to_add = new_links[:available_slots]
                                        self.url_queue.extend(links_to_add)

                                        if len(new_links) > available_slots:
                                            logger.warning(
                                                f"Dropped {len(new_links) - available_slots} links (queue full)"
                                            )
                                else:
                                    logger.debug(
                                        f"Max depth {spider_depth} reached for {url}, not following links"
                                    )
                        except Exception as e:
                            logger.error(f"Error processing {url}: {e}")
                            self.db.mark_url_failed(url, str(e))

                    # Progress update
                    if pages_processed % 10 == 0:
                        logger.info(
                            f"Progress: {pages_processed} pages processed, {len(self.url_queue)} in queue"
                        )

        else:
            # Simple mode: multi-threaded scraping of provided URLs
            # Filter through database cache
            urls_to_scrape = [
                u for u in urls if self.db.should_scrape_url(u, self.expiration_days)
            ]
            total = len(urls_to_scrape)
            logger.info(f"Starting scrape of {total} URLs (after cache check)")

            with ThreadPoolExecutor(
                max_workers=self.max_concurrent_threads
            ) as executor:
                futures = {
                    executor.submit(self._process_single_url, url): url
                    for url in urls_to_scrape
                }

                completed = 0
                for future in as_completed(futures):
                    url = futures[future]
                    completed += 1
                    try:
                        result = future.result()
                        if result:
                            output_path, _ = result
                            output_files.append(output_path)
                    except Exception as e:
                        logger.error(f"Error processing {url}: {e}")
                        self.db.mark_url_failed(url, str(e))

                    # Progress update
                    if completed % 10 == 0:
                        logger.info(
                            f"Progress: {completed}/{total} ({completed/total*100:.1f}%)"
                        )

        return output_files

    def scrape_all(
        self, databases: tuple = (), limit: Optional[int] = None
    ) -> Dict[str, List[Path]]:
        """Scrape all discovered URLs."""
        categorized = self.discover_urls()

        if databases:
            categorized = {
                db: data for db, data in categorized.items() if db in databases
            }

        results = {}

        for db, data in categorized.items():
            logger.info(f"Scraping {db}...")
            urls = data["urls"][:limit] if limit else data["urls"]

            db_files = []
            for url in tqdm(urls, desc=f"Scraping {db}", unit="url"):
                result = self.fetch_and_convert(url)
                if result:
                    content, metadata, _ = result  # Unpack 3 values now
                    filepath = self.save_file(content, metadata, url)
                    db_files.append(filepath)

            results[db] = db_files

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        total = self.stats["total_requests"]
        if total == 0:
            return {"total_requests": 0, "success_rate": 0, "average_time": 0}

        return {
            "total_requests": total,
            "success_rate": (self.stats["successful_requests"] / total) * 100,
            "average_time": self.stats["total_time"] / total,
        }

    def close(self):
        """Close HTTP session and database."""
        self.session.close()
        self.db.close()
        logger.info("Closed HTTP session and database")


# ============================================================================
# SKILL.MD GENERATOR
# ============================================================================


def create_comprehensive_skill_file(
    root_dir: Path, overwrite: bool = False, db: Optional[ScraperDatabase] = None
) -> Optional[Path]:
    """
    Create a single comprehensive SKILL.md at root with ALL documents listed.

    Args:
        root_dir: Root directory containing all scraped content
        overwrite: Whether to overwrite existing SKILL.md
        db: Database connection for metadata retrieval

    Returns:
        Path to created SKILL.md file
    """
    if not root_dir.exists() or not root_dir.is_dir():
        logger.warning(f"Directory does not exist: {root_dir}")
        return None

    skill_file = root_dir / "SKILL.md"

    if skill_file.exists() and not overwrite:
        logger.info(f"SKILL.md already exists: {skill_file}")
        return skill_file

    logger.info("Using database for metadata...")

    # Collect all markdown files with their metadata from database
    documents = []

    if db is None:
        logger.warning("No database provided, cannot generate SKILL.md")
        return None

    for _url, title, file_path in db.get_all_scraped_urls():
        if file_path:
            try:
                full_path = Path(file_path)
                if full_path.exists():
                    rel_path = full_path.relative_to(root_dir)

                    # Get description from file
                    with open(full_path, "r", encoding="utf-8") as f:
                        post = frontmatter.load(f)
                    description = post.metadata.get("description", "")

                    documents.append(
                        {
                            "title": title or full_path.stem.replace("-", " ").title(),
                            "description": description,
                            "path": str(rel_path),
                        }
                    )
            except Exception as e:
                logger.debug(f"Could not process {file_path}: {e}")
                continue

    if not documents:
        logger.warning(f"No documents found in {root_dir}")
        return None

    logger.info(f"Found {len(documents)} documents, generating SKILL.md...")

    # Sort documents by path
    documents.sort(key=lambda x: x["path"])

    # Derive skill name from directory name
    skill_name = root_dir.name

    # Generate the comprehensive SKILL.md content
    content = f"""---
name: {skill_name}
description: Reference documentation scraped from Snowflake's official documentation
version: 1.1.0
author: Snowflake Inc.
auto_generated: true
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

# {skill_name.replace('-', ' ').title()}

Reference documentation scraped from Snowflake's official documentation.

## All Documents ({len(documents)} total)

"""

    # Add each document with description
    for doc in documents:
        if doc["description"]:
            content += f"- [{doc['title']}]({doc['path']}) - {doc['description']}\n"
        else:
            content += f"- [{doc['title']}]({doc['path']})\n"

    content += f"""
## About This Documentation

All content is automatically scraped from [Snowflake's Official Documentation](https://docs.snowflake.com/).

- **Total Documents**: {len(documents)}
- **Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
- **Auto-generated**: Yes

---

*This skill provides quick access to Snowflake documentation for AI assistants.*
"""

    # Write the file
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Created SKILL.md with {len(documents)} documents")
    return skill_file


# ============================================================================
# CLI
# ============================================================================


@click.command()
@click.option(
    "--output-dir", required=True, help="Output directory for scraped documentation"
)
@click.option(
    "--base-path",
    default="/en/migrations/",
    help="URL base path to filter (e.g., /en/, /en/sql-reference/)",
)
@click.option("--limit", type=int, help="Limit URLs (for testing)")
@click.option(
    "--spider/--no-spider", default=True, help="Follow internal links (spider mode)"
)
@click.option(
    "--spider-depth",
    default=1,
    type=int,
    help="Spider depth: 0=seeds only, 1=+direct links (default), 2=+2nd degree, etc.",
)
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--dry-run", is_flag=True, help="Preview without writing files")
def main(output_dir, base_path, limit, spider, spider_depth, verbose, dry_run):
    """Scrape Snowflake documentation with configurable base path (v1.1)."""

    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(level=log_level, log_file="scraper-v1.1.log")

    click.secho("\n" + "=" * 70, fg="cyan", bold=True)
    click.secho("  Snowflake Documentation Scraper v1.1", fg="cyan", bold=True)
    click.secho("=" * 70 + "\n", fg="cyan", bold=True)

    # Display configuration
    click.echo(f"Output directory: {output_dir}")
    click.echo(f"Base path filter: {base_path}")
    click.echo(f"Spider mode: {'Enabled (follow links)' if spider else 'Disabled'}")
    if limit:
        click.echo(f"Limit: {limit} URLs per database")
    if dry_run:
        click.secho("\n⚠ DRY RUN MODE - No files will be written", fg="yellow")

    try:
        # Initialize scraper
        scraper = SnowflakeDocsScraper(output_dir=output_dir, base_path=base_path)

        # Discover URLs
        click.echo("\n[1/3] Discovering URLs from sitemap...")
        categorized = scraper.discover_urls(use_cache=True)

        total_urls = sum(len(data["urls"]) for data in categorized.values())
        click.echo(f"Found {total_urls} URLs across {len(categorized)} categories")

        if dry_run:
            click.echo("\nWould scrape:")
            for db, data in categorized.items():
                click.echo(f"  - {db}: {len(data['urls'])} URLs")
            return

        # Scrape all URLs
        click.echo(
            f"\n[2/3] Scraping documentation... (spider={'on' if spider else 'off'})"
        )

        # Get all URLs from categorized data
        all_urls = []
        for _category, data in categorized.items():
            urls = data["urls"][:limit] if limit else data["urls"]
            all_urls.extend(urls)

        # Use spider mode
        output_files = scraper.scrape_urls(
            all_urls, spider=spider, spider_depth=spider_depth
        )

        # For compatibility with old structure
        results = {"all": output_files}

        # Display results
        click.echo("\n[3/3] Results:")
        total_files = 0
        for db, files in results.items():
            click.echo(f"  - {db}: {len(files)} files")
            total_files += len(files)

        # Display statistics
        stats = scraper.get_stats()
        click.echo(f"\n{click.style('✓', fg='green', bold=True)} Scraping complete:")
        click.echo(f"  Total files: {total_files}")
        click.echo(f"  Total requests: {stats['total_requests']}")
        click.echo(f"  Success rate: {stats['success_rate']:.1f}%")
        click.echo(f"  Average time: {stats['average_time']:.2f}s per request")

        # Cleanup
        scraper.close()

        # Generate comprehensive SKILL.md
        click.echo("\n[4/4] Generating SKILL.md...")
        skill_file = create_comprehensive_skill_file(
            Path(output_dir), overwrite=True, db=scraper.db
        )
        if skill_file:
            click.secho(f"✓ Created: {skill_file.name}", fg="green")
        else:
            click.secho("⚠ Failed to create SKILL.md", fg="yellow")

        click.secho(
            f"\nAll done! Output written to: {output_dir}", fg="green", bold=True
        )

    except Exception as e:
        click.secho(f"\n✗ Error: {e}", fg="red", bold=True)
        logger.exception("Scraping failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
