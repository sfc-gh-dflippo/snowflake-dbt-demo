---
name: doc-scraper
description:
  Generic web scraper for extracting and organizing Snowflake documentation with intelligent caching
  and configurable spider depth. Scrapes any section of docs.snowflake.com controlled by
  --base-path.
---

# Snowflake Documentation Scraper

Scrapes docs.snowflake.com sections to Markdown with SQLite caching (7-day expiration).

## Usage

**First time setup** (auto-installs uv and doc-scraper):

```bash
python3 .claude/skills/doc-scraper/scripts/doc_scraper.py
```

**Subsequent runs:**

```bash
doc-scraper --output-dir=./snowflake-docs
doc-scraper --output-dir=./snowflake-docs --base-path="/en/sql-reference/"
doc-scraper --output-dir=./snowflake-docs --spider-depth=2
```

## Command Options

| Option           | Default           | Description                           |
| ---------------- | ----------------- | ------------------------------------- |
| `--output-dir`   | **Required**      | Output directory for scraped docs     |
| `--base-path`    | `/en/migrations/` | URL section to scrape                 |
| `--spider-depth` | `1`               | Link depth: 0=seeds, 1=+links, 2=+2nd |
| `--limit`        | None              | Cap URLs (for testing)                |
| `--dry-run`      | -                 | Preview without writing               |

## Output

```sql
output-dir/
├── SKILL.md              # Auto-generated index
├── scraper_config.yaml   # Editable config (auto-created)
├── .cache/               # SQLite cache (auto-managed)
└── en/migrations/*.md    # Scraped pages with frontmatter
```

## Configuration

Auto-created at `{output-dir}/scraper_config.yaml`:

```yaml
rate_limiting:
  max_concurrent_threads: 4
spider:
  max_pages: 1000
  allowed_paths: ["/en/"]
scraped_pages:
  expiration_days: 7
```

## Troubleshooting

| Issue            | Solution                              |
| ---------------- | ------------------------------------- |
| Too many pages   | Lower `--spider-depth` or edit config |
| Missing pages    | Increase `--spider-depth`             |
| Cache corruption | Delete `{output-dir}/.cache/` (rare)  |
