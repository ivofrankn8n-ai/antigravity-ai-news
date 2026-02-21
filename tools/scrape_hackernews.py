#!/usr/bin/env python3
"""
Hacker News AI Articles Scraper
Fetches AI-related articles from Hacker News
"""

import json
import requests
from datetime import datetime, timezone
from pathlib import Path

HN_API_URL = "https://hacker-news.firebaseio.com/v0"
AI_KEYWORDS = ["ai", "llm", "gpt", "chatgpt", "openai", "anthropic", "claude", "machine learning", "ml", "deep learning"]
DATA_FILE = Path(".tmp/hackernews_articles.json")


def fetch_top_stories(limit=50):
    """Fetch top story IDs from HN"""
    response = requests.get(f"{HN_API_URL}/topstories.json", timeout=30)
    response.raise_for_status()
    return response.json()[:limit]


def fetch_story(story_id):
    """Fetch individual story details"""
    response = requests.get(f"{HN_API_URL}/item/{story_id}.json", timeout=10)
    if response.status_code == 200:
        return response.json()
    return None


def is_ai_related(title, tags=None):
    """Check if article is AI-related"""
    if not title:
        return False
    title_lower = title.lower()
    return any(kw in title_lower for kw in AI_KEYWORDS)


def transform_story(story):
    """Transform HN story to our schema"""
    if not story or story.get("type") != "story":
        return None
    
    if not is_ai_related(story.get("title", "")):
        return None
    
    return {
        "id": f"hn_{story.get('id')}",
        "title": story.get("title", ""),
        "subtitle": story.get("text", "")[:200] if story.get("text") else "",
        "url": story.get("url") or f"https://news.ycombinator.com/item?id={story.get('id')}",
        "source": "Hacker News",
        "published_at": datetime.fromtimestamp(story.get("time", 0), tz=timezone.utc).isoformat() if story.get("time") else None,
        "saved": False,
        "tags": [story.get("type")],
        "score": story.get("score", 0),
        "comments": story.get("descendants", 0)
    }


def save_articles(articles):
    """Save articles to local JSON file"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    existing = []
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            existing = json.load(f)
    
    existing_ids = {a["id"] for a in existing}
    new_articles = [a for a in articles if a and a["id"] not in existing_ids]
    
    all_articles = new_articles + existing
    
    with open(DATA_FILE, "w") as f:
        json.dump(all_articles, f, indent=2)
    
    return len(new_articles)


def main():
    """Main execution"""
    print("Fetching Hacker News top stories...")
    story_ids = fetch_top_stories(100)
    print(f"Found {len(story_ids)} top stories")
    
    articles = []
    for i, story_id in enumerate(story_ids):
        if i % 20 == 0:
            print(f"  Processing {i}/{len(story_ids)}...")
        story = fetch_story(story_id)
        if story:
            article = transform_story(story)
            if article:
                articles.append(article)
    
    print(f"Found {len(articles)} AI-related articles")
    
    if articles:
        saved_count = save_articles(articles)
        print(f"Saved {saved_count} new articles to {DATA_FILE}")
    else:
        print("No new AI articles found")


if __name__ == "__main__":
    main()
