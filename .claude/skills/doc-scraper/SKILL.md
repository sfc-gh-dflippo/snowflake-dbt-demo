---
name: doc-scraper
description: Generic web scraper for extracting and organizing Snowflake documentation with intelligent caching and configurable spider depth. Install globally with uv for easy access, or use uvx for development. Scrapes any section of docs.snowflake.com controlled by --base-path.
---

# Snowflake Documentation Scraper

Generic scraper for any section of docs.snowflake.com. Converts to Markdown with metadata and generates indexed SKILL.md.

**Features:** SQLite caching (7-day expiration) • Multi-threaded (4 workers) • Configurable spider depth • Base path filtering

**Install:** `uv tool install --editable .` • **Run:** `doc-scraper --output-dir=/path/to/output`

## Quick Start

**One-time setup (installs globally):**
```bash
cd .claude/skills/doc-scraper
uv tool install --editable .
```

**Then run from anywhere:**
```bash
doc-scraper --output-dir=/path/to/output
```

**For development** (picks up code/config changes without reinstall):
```bash
cd .claude/skills/doc-scraper
uvx --from . doc-scraper --output-dir=../../snowflake-docs
```

## Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output-dir DIR` | **Required** | Output directory for scraped docs (relative to CWD) |
| `--base-path PATH` | `/en/migrations/` | URL filter - controls what section to scrape |
| `--spider/--no-spider` | `--spider` | Follow internal links |
| `--spider-depth N` | `1` | Depth: 0=seeds only, 1=+direct links, 2=+2nd degree |
| `--limit N` | None | Cap URLs (for testing) |
| `--dry-run` | - | Preview without writing files |
| `-v, --verbose` | - | Debug logging |

## Common Tasks

**Using globally installed tool** (recommended - run from anywhere):

```bash
# Initial scrape - migrations section (clear cache first)
rm -rf /path/to/project/snowflake-docs/.cache
doc-scraper --output-dir=/path/to/project/snowflake-docs

# Update existing (skips cached pages automatically)
doc-scraper --output-dir=/path/to/project/snowflake-docs

# Scrape SQL reference instead of migrations
doc-scraper --output-dir=/path/to/project/snowflake-docs \
  --base-path="/en/sql-reference/"

# Scrape user guide section
doc-scraper --output-dir=/path/to/project/snowflake-docs \
  --base-path="/en/user-guide/"

# Deep spider (2 levels of link following)
doc-scraper --output-dir=/path/to/project/snowflake-docs \
  --spider-depth=2

# Test run (10 URLs max, preview only)
doc-scraper --output-dir=/path/to/project/snowflake-docs \
  --limit 10 --dry-run
```

**For development** (from `.claude/skills/doc-scraper/` directory):

```bash
# Use uvx to pick up code/config changes immediately
uvx --from . doc-scraper --output-dir=../../snowflake-docs
uvx --from . doc-scraper --output-dir=../../snowflake-docs --base-path="/en/sql-reference/"
```

## Configuration

**Auto-created on first run**: `{output-dir}/scraper_config.yaml`

The config file is automatically created in your output directory on first run with these defaults:

```yaml
rate_limiting:
  requests_per_second: 2        # Rate limit
  max_concurrent_threads: 4     # Parallel workers

spider:
  max_pages: 1000              # Stop after N pages
  max_queue_size: 500          # Queue limit
  allowed_paths: ["/en/"]      # URL filters

scraped_pages:
  expiration_days: 7           # Cache expiration
```

**To customize**: Edit `{output-dir}/scraper_config.yaml` directly. Changes take effect on next run.

## Output Structure

```
snowflake-docs/
├── SKILL.md                    # Auto-generated index
└── en/migrations/              # Organized by URL path
    ├── page1.md               # With YAML frontmatter
    └── page2.md
```

Each markdown file includes:
```yaml
---
title: "Page Title"
source_url: "https://docs.snowflake.com/..."
last_scraped: "2025-11-19T12:30:00+00:00"
---
```

## Cache Management

**Cache location**: `{output-dir}/.cache/`
- `scraper.db` - SQLite database with page metadata
- `sitemap_cache.json` - Cached sitemap URLs

```bash
# Clear cache for a specific output directory
rm -rf /path/to/output/.cache

# Clear cache (when using relative path from project)
rm -rf ../../snowflake-docs/.cache
```

**Cache behavior**: 7-day expiration, automatic pre-load, survives crashes, ~50KB per 1,000 pages.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Too many pages scraped | Lower `--spider-depth` or add blocked patterns in config |
| Missing pages | Increase `--spider-depth` or adjust `allowed_paths` |
| Slow performance | Check `max_queue_size` and `max_pages` in config |
| Cache not working | Delete `scripts/.cache/scraper.db` and re-run |
| ImportError (uv) | Use `uvx --refresh` or clear cache: `rm -rf ~/.cache/uv/archive-v0/<hash>` |

## Installation

**Recommended: Global install with uv**
```bash
cd .claude/skills/doc-scraper
uv tool install --editable .
```

Benefits:
- ✅ Run from anywhere: `doc-scraper --output-dir=/path/to/output`
- ✅ Simple command: no `uvx` or directory navigation
- ✅ Editable mode: updates when you pull new code

**For development: Use uvx**
```bash
cd .claude/skills/doc-scraper
uvx --from . doc-scraper --output-dir=../../snowflake-docs
```

Benefits:
- ✅ No installation needed
- ✅ Picks up code changes immediately
- ✅ Picks up config changes (`scraper_config.yaml`) immediately
- ✅ Perfect for testing changes

**Legacy: venv method**
```bash
cd .claude/skills/doc-scraper/scripts
python -m venv ../venv
source ../venv/bin/activate
pip install -r ../requirements.txt
python doc_scraper.py --output-dir=../../snowflake-docs
```

**⚠️ Path Tips:**
- Global install: Use absolute paths for `--output-dir`
- uvx/venv: Can use relative paths from project directory

## Technical Stack

Python 3.11+ • SQLite • BeautifulSoup • markdownify • requests • ratelimit • click

---

**Version**: 1.1.0 • **Status**: Production Ready ✅
