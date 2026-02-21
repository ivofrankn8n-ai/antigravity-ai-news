# SOP: Reddit Scraper

## Goal
Fetch latest posts from AI-related subreddits (r/artificial, r/OpenAI).

## Input
- Subreddits: r/artificial, r/OpenAI
- Endpoint: `https://www.reddit.com/r/{subreddit}/new.json`
- No authentication required (read-only public access)

## Tool Logic

### 1. Fetch Posts
```python
GET https://www.reddit.com/r/{subreddit}/new.json?limit=25
Headers: User-Agent: Mozilla/5.0
```

### 2. Transform Schema
Map Reddit post to unified Article schema:
```json
{
  "id": "string (Reddit post ID)",
  "title": "string",
  "subtitle": "string (selftext truncated to 200 chars)",
  "url": "string (permalink)",
  "source": "r/{subreddit}",
  "published_at": "datetime (ISO format)",
  "saved": false,
  "tags": ["flair_text"],
  "score": "number",
  "comments": "number"
}
```

### 3. Save to Storage
- Location: `.tmp/reddit_articles.json`
- Merge with existing (avoid duplicates by ID)

## Edge Cases
- Rate limiting: Respect Reddit's 60 requests/minute
- Private subreddit: Skip with warning
- Deleted/removed posts: Skip silently
- No posts: Log message

## Verification
- Run: `python3 tools/scrape_reddit.py`
- Check: `.tmp/reddit_articles.json` contains posts from both subreddits
