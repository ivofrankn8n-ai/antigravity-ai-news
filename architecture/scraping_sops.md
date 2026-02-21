# Scraping SOPs

## Overview
Automated daily scraping of AI news from multiple sources.

## Data Sources

| Source | Script | API/URL | Frequency |
|--------|--------|---------|-----------|
| Ben's Bites | `scrape_bensbites.py` | bensbites.beehiiv.com/posts | Daily |
| The Rundown AI | `scrape_rundown.py` | therundown.ai/posts | Daily |
| Reddit | `scrape_reddit.py` | reddit.com/r/artificial, r/OpenAI | Daily |
| Hacker News | `scrape_hackernews.py` | hacker-news.firebaseio.com | Daily |

## Workflow

### 1. Run Individual Scrapers
```bash
cd tools

# Scrape Ben's Bites
python scrape_bensbites.py

# Scrape The Rundown AI  
python scrape_rundown.py

# Scrape Reddit
python scrape_reddit.py

# Scrape Hacker News
python scrape_hackernews.py
```

### 2. Aggregate Articles
```bash
python aggregate_articles.py
```
- Combines all source JSON files
- Removes duplicates
- Sorts by published_at
- Saves to `.tmp/articles.json`

### 3. Sync to Supabase
```bash
python -c "from supabase_client import SupabaseClient; client = SupabaseClient(); client.sync_from_local()"
```

## Scheduling

### Option A: Cron (macOS/Linux)
```bash
# Edit crontab
crontab -e

# Add daily at 6 AM
0 6 * * * /path/to/tools/run_all_scrapers.py
```

### Option B: Task Scheduler (Windows)
```batch
# Create task_scrape.bat
@echo off
cd C:\path\to\project\tools
python run_all_scrapers.py
```
Then use Task Scheduler to run daily at 6 AM.

## Manual Run
```bash
cd tools
python run_all_scrapers.py
```

## Output Files
- `.tmp/bensbites_articles.json`
- `.tmp/rundown_articles.json`
- `.tmp/reddit_articles.json`
- `.tmp/hackernews_articles.json`
- `.tmp/articles.json` (aggregated)
