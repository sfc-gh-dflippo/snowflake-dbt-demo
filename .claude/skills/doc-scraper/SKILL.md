# Snowflake Documentation Scraper

AI-powered web scraper for extracting and organizing Snowflake documentation with intelligent caching and configurable spider depth.

## Quick Start

```bash
cd .claude/skills/doc-scraper/scripts
source ../venv/bin/activate
python doc-scraper.py --full-update --spider --spider-depth=1
```

## Core Features

- **Intelligent Spidering**: Configurable depth control (0=seeds only, 1=+direct links, 2=+second degree)
- **SQLite Caching**: Automatic database tracking with 7-day expiration
- **Pre-loading**: Scans existing files on startup to avoid re-scraping
- **Multi-threaded**: Concurrent fetching (4 workers default)
- **Rate Limited**: Respectful 2 req/sec to Snowflake servers
- **Auto-generates**: Single SKILL.md with all document links

## Command Reference

### Basic Usage

```bash
# Scrape migrations + direct links (depth=1)
python doc-scraper.py --full-update --spider --spider-depth=1

# Scrape only migration pages (no spidering)
python doc-scraper.py --full-update --no-spider

# Scrape with 2 degrees of spidering
python doc-scraper.py --full-update --spider --spider-depth=2

# Test with limited URLs
python doc-scraper.py --full-update --spider --limit 10
```

### Key Options

- `--full-update`: Scrape all discovered URLs
- `--spider/--no-spider`: Enable/disable link following (default: on)
- `--spider-depth N`: How deep to spider (default: 1)
  - `0`: Seeds only (no following)
  - `1`: Seeds + direct links
  - `2`: Seeds + links + links from those
- `--base-path PATH`: URL filter (default: `/en/migrations/`)
- `--output-dir DIR`: Where to save (default: `../../snowflake-docs`)
- `--limit N`: Cap URLs per database (testing)
- `--dry-run`: Preview without writing

### Output Structure

```
snowflake-docs/
├── SKILL.md              # Auto-generated index of all docs
└── en/
    └── migrations/       # Organized by URL path
        ├── guides/
        ├── sma-docs/
        └── snowconvert-docs/
```

## Database Management

### Cache Location
```
scripts/.cache/scraper.db
```

### Reset Cache
```bash
rm -f scripts/.cache/scraper.db
```

### Cache Behavior
- **7-day expiration**: Pages older than 7 days are re-scraped
- **Automatic pre-load**: Existing files loaded into DB on startup
- **Skip cached**: Already-scraped pages skipped automatically
- **Persistent**: Survives crashes, continues from where it left off

## Configuration

Edit `scripts/scraper_config.yaml`:

```yaml
# Rate limiting
rate_limiting:
  requests_per_second: 2
  max_concurrent_threads: 4

# Spider limits
spider:
  max_pages: 1000
  max_queue_size: 500
  allowed_paths:
    - "/en/"

# Cache expiration
scraped_pages:
  expiration_days: 7
```

## Common Workflows

### 1. Initial Scrape
```bash
# Clear everything and start fresh
rm -rf ../../snowflake-docs
rm -f .cache/scraper.db

# Scrape migrations + direct references
python doc-scraper.py --full-update --spider --spider-depth=1
```

### 2. Update Existing
```bash
# Just run again - automatically skips cached pages
python doc-scraper.py --full-update --spider --spider-depth=1
```

### 3. Expand Coverage
```bash
# Increase spider depth to get more pages
python doc-scraper.py --full-update --spider --spider-depth=2
```

### 4. Change Target
```bash
# Scrape different documentation section
python doc-scraper.py --full-update --base-path="/en/sql-reference/"
```

## Output Files

Each scraped page creates:

**Markdown file** with YAML front-matter:
```yaml
---
title: "Page Title"
description: "Page description"
source_url: "https://docs.snowflake.com/..."
last_scraped: "2025-11-19T12:30:00+00:00"
scraper_version: "1.1.0"
auto_generated: true
---

# Content here...
```

**SKILL.md** index:
```markdown
- [Page Title](path/to/file.md) - Description
```

## Memory & Performance

- **Memory usage**: ~10-50 KB (only active queue in RAM)
- **Speed**: 2 requests/second, 4 concurrent workers
- **Cache efficiency**: 95%+ on subsequent runs
- **Database size**: ~50 KB per 1,000 pages

## Troubleshooting

### Issue: Too many pages scraped
**Solution**: Lower `--spider-depth` or add blocked patterns to config

### Issue: Missing pages
**Solution**: Increase `--spider-depth` or adjust `allowed_paths` in config

### Issue: Slow performance
**Solution**: Check `max_queue_size` and `max_pages` limits in config

### Issue: Cache not working
**Solution**: Delete `.cache/scraper.db` and re-run to rebuild

## Technical Details

- **Language**: Python 3.11+
- **Database**: SQLite with thread-safe operations
- **HTML Parser**: BeautifulSoup with lxml
- **Markdown**: markdownify with ATX headers
- **Rate Limiting**: ratelimit with thread safety
- **Front-matter**: python-frontmatter for metadata

## Dependencies

Install via:
```bash
source ../venv/bin/activate
pip install -r requirements.txt
```

See `requirements.txt` for full list.

---

**Version**: 1.1.0
**Last Updated**: 2025-11-19
**Status**: Production Ready ✅
