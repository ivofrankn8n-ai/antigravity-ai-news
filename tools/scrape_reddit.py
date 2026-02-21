#!/usr/bin/env python3
"""
Reddit Scraper
Fetches posts from specified subreddits
"""

import json
import requests
from datetime import datetime, timezone
from pathlib import Path

REDDIT_SUBREDDITS = ["artificial", "OpenAI"]
DATA_FILE = Path(".tmp/reddit_articles.json")


def fetch_reddit_posts(subreddit, limit=25):
    """Fetch posts from a subreddit"""
    url = f"https://www.reddit.com/r/{subreddit}/new.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AI-Dashboard/1.0)"
    }
    
    response = requests.get(url, headers=headers, params={"limit": limit}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    return data.get("data", {}).get("children", [])


def transform_post(post, subreddit):
    """Transform Reddit post to our schema"""
    data = post.get("data", {})
    created_utc = data.get("created_utc", 0)
    
    return {
        "id": data.get("id"),
        "title": data.get("title", ""),
        "subtitle": data.get("selftext", "")[:200] if data.get("selftext") else "",
        "url": f"https://reddit.com{data.get('permalink')}",
        "source": f"r/{subreddit}",
        "published_at": datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat(),
        "saved": False,
        "tags": [data.get("link_flair_text", "")] if data.get("link_flair_text") else [],
        "score": data.get("score", 0),
        "comments": data.get("num_comments", 0)
    }


def save_articles(articles):
    """Save articles to local JSON file"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    existing = []
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    
    existing_ids = {a["id"] for a in existing}
    new_articles = [a for a in articles if a["id"] not in existing_ids]
    
    all_articles = new_articles + existing
    
    with open(DATA_FILE, "w") as f:
        json.dump(all_articles, f, indent=2)
    
    return len(new_articles)


def main():
    """Main execution"""
    all_posts = []
    
    for subreddit in REDDIT_SUBREDDITS:
        print(f"Fetching r/{subreddit}...")
        posts = fetch_reddit_posts(subreddit)
        transformed = [transform_post(p, subreddit) for p in posts]
        all_posts.extend(transformed)
        print(f"  Found {len(transformed)} posts")
    
    saved_count = save_articles(all_posts)
    print(f"Saved {saved_count} new articles to {DATA_FILE}")


if __name__ == "__main__":
    main()
