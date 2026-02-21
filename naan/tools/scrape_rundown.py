#!/usr/bin/env python3
"""
The Rundown AI Scraper
Fetches articles from therundown.ai
"""

import json
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path

RUNDOWN_API_URL = "https://www.therundown.ai/posts"
DATA_FILE = Path(".tmp/rundown_articles.json")


def fetch_rundown_articles():
    """Fetch all articles from The Rundown AI API"""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; AI-Dashboard/1.0)"}

    response = requests.get(RUNDOWN_API_URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data.get("posts", [])


def filter_articles_by_date(articles, hours=24):
    """Filter articles published in the last N hours"""
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    filtered = []

    for article in articles:
        pub_date_str = article.get("override_scheduled_at") or article.get("created_at")
        if not pub_date_str:
            continue

        try:
            pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)

            if pub_date >= cutoff_time:
                filtered.append(transform_article(article))
        except (ValueError, TypeError):
            continue

    return filtered


def transform_article(article):
    """Transform article to our schema"""
    return {
        "id": article.get("id"),
        "title": article.get("web_title", ""),
        "subtitle": article.get("web_subtitle", ""),
        "url": f"https://www.therundown.ai/p/{article.get('slug')}",
        "source": "The Rundown AI",
        "published_at": article.get("override_scheduled_at")
        or article.get("created_at"),
        "saved": False,
        "tags": [tag.get("display", "") for tag in article.get("content_tags", [])],
        "reading_time": article.get("estimated_reading_time_display", ""),
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
    print("Fetching The Rundown AI articles...")
    articles = fetch_rundown_articles()
    print(f"Found {len(articles)} total articles")

    recent_articles = filter_articles_by_date(articles, hours=24)
    print(f"Found {len(recent_articles)} articles from last 24 hours")

    if recent_articles:
        saved_count = save_articles(recent_articles)
        print(f"Saved {saved_count} new articles to {DATA_FILE}")
    else:
        print("No new articles in the last 24 hours")
        print("Saving all articles for demonstration...")
        all_transformed = [transform_article(a) for a in articles]
        save_articles(all_transformed)
        print(f"Saved {len(all_transformed)} articles to {DATA_FILE}")


if __name__ == "__main__":
    main()
