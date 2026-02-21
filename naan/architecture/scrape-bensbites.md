# SOP: Ben's Bites Scraper

## Goal
Fetch AI news articles from Ben's Bites newsletter published in the last 24 hours.

## Input
- API Endpoint: `https://bensbites.beehiiv.com/posts`
- No authentication required

## Tool Logic

### 1. Fetch Articles
```python
GET https://bensbites.beehiiv.com/posts
Headers: User-Agent: Mozilla/5.0
```

### 2. Filter by Date
- Parse `override_scheduled_at` or `created_at` field
- Compare against `datetime.utcnow() - 24 hours`
- Keep articles within the window

### 3. Transform Schema
Map to unified Article schema:
```json
{
  "id": "string",
  "title": "string",
  "subtitle": "string",
  "url": "string",
  "source": "Ben's Bites",
  "published_at": "datetime",
  "saved": false,
  "tags": [],
  "reading_time": "string"
}
```

### 4. Save to Storage
- Location: `.tmp/bensbites_articles.json`
- Merge with existing (avoid duplicates by ID)

## Edge Cases
- Empty response: Log warning, exit gracefully
- Network error: Raise exception, do not corrupt existing data
- No new articles: Log "No new articles" message
- Date parse error: Skip article, continue processing

## Verification
- Run: `python3 tools/scrape_bensbites.py`
- Check: `.tmp/bensbites_articles.json` contains articles
