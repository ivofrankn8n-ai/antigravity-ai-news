#!/usr/bin/env python3
"""
Daily scraper - Run to fetch latest articles and sync to Supabase
Can be scheduled with cron or Task Scheduler
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.scrape_bensbites import (
    fetch_bensbites_articles,
    save_articles as save_bensbites_articles,
)
from tools.scrape_reddit import (
    fetch_reddit_posts,
    transform_post,
    save_articles as save_reddit_articles,
)
from tools.scrape_hackernews import (
    fetch_top_stories,
    fetch_story,
    transform_story,
    save_articles as save_hn_articles,
)
from tools.scrape_rundown import (
    fetch_rundown_articles,
    save_articles as save_rundown_articles,
)
from tools.aggregate_articles import main as aggregate_articles
from tools.supabase_client import SupabaseClient
from datetime import datetime


def run_scrapers():
    """Run all scrapers and aggregate results"""
    print(f"\n{'=' * 50}")
    print(f"Starting daily scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}\n")

    # Run individual scrapers
    print("Scraping Ben's Bites...")
    articles = fetch_bensbites_articles()
    save_bensbites_articles(articles)

    print("Scraping The Rundown AI...")
    articles = fetch_rundown_articles()
    save_rundown_articles(articles)

    print("Scraping Reddit...")
    all_reddit = []
    for subreddit in ["artificial", "OpenAI"]:
        posts = fetch_reddit_posts(subreddit)
        transformed = [transform_post(p, subreddit) for p in posts]
        all_reddit.extend(transformed)
    save_reddit_articles(all_reddit)

    print("Scraping Hacker News...")
    story_ids = fetch_top_stories(100)
    articles = []
    for story_id in story_ids:
        story = fetch_story(story_id)
        if story:
            transformed = transform_story(story)
            if transformed:
                articles.append(transformed)
    save_hn_articles(articles)

    # Aggregate all articles
    print("\nAggregating articles...")
    aggregate_articles()

    print("\nScraping complete!")


def sync_to_supabase():
    """Sync aggregated articles to Supabase"""
    print("\nSyncing to Supabase...")

    client = SupabaseClient()

    # Read aggregated articles
    import json
    from pathlib import Path

    articles_file = Path(".tmp/articles.json")
    if not articles_file.exists():
        print("No articles found to sync")
        return False

    with open(articles_file) as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles to sync")

    # Insert articles
    success = client.insert_articles(articles)

    # Get total count from Supabase
    total = client.get_articles(limit=200)
    print(f"Total articles in database: {len(total)}")

    if success or len(total) > 0:
        print(f"Supabase sync successful!")
        return True
    else:
        print("Failed to sync articles")
        return False


def main():
    """Main entry point"""
    # Run scrapers
    run_scrapers()

    # Sync to Supabase (optional - only if configured)
    try:
        sync_to_supabase()
    except Exception as e:
        print(f"Supabase sync skipped: {e}")

    print(f"\n{'=' * 50}")
    print("Daily scrape complete!")
    print(f"{'=' * 50}\n")


if __name__ == "__main__":
    main()
