# AI News Dashboard - Deployment Guide

## Quick Deploy to Netlify

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "AI News Dashboard"
   ```

2. **Connect to Netlify**
   - Go to https://netlify.com
   - Sign up with GitHub
   - "Add new site" → "Import an existing project"
   - Select your GitHub repo

3. **Configure**
   - Build command: (leave empty)
   - Publish directory: .

4. **Deploy!**

## Alternative: Drag & Drop

1. Go to https://app.netlify.com/drop
2. Drag the project folder onto the page
3. Your site is live!

## Running Daily Scraping

### Option 1: GitHub Actions (Free)

Create `.github/workflows/daily-scrape.yml`:

```yaml
name: Daily Scrape
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Run scrapers
        run: python run_daily_scrape.py
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
```

### Option 2: Local Cron (Mac/Linux)

```bash
# Add to crontab
crontab -e

# Add this line to run daily at 6am:
0 6 * * * /usr/bin/python3 /path/to/run_daily_scrape.py
```

### Option 3: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily
4. Set action: Start a program
5. Program: `python`
6. Arguments: `run_daily_scrape.py`

## Supabase Setup

1. Create project at https://supabase.com
2. Get URL and anon key from Settings → API
3. Create table with schema from `supabase_schema.sql`
4. Add credentials to dashboard via API Config button

## Files Structure

```
├── dashboard.html      # Main app
├── .tmp/             # Local article cache
├── tools/            # Scraper scripts
├── run_daily_scrape.py  # Daily scraper
├── netlify.toml      # Netlify config
└── supabase_schema.sql   # DB schema
```
