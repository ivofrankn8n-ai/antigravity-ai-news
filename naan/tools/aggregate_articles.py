#!/usr/bin/env python3
"""
Aggregate all articles from different sources
"""

import json
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path(".tmp")
COMBINED_FILE = Path(".tmp/articles.json")
SAVED_FILE = Path(".tmp/saved_articles.json")


def load_articles(filename):
    """Load articles from a JSON file"""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r") as f:
            return json.load(f)
    return []


def save_combined(articles):
    """Save combined articles"""
    COMBINED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COMBINED_FILE, "w") as f:
        json.dump(articles, f, indent=2)


def main():
    """Aggregate all articles"""
    bensbites = load_articles("bensbites_articles.json")
    reddit = load_articles("reddit_articles.json")
    hackernews = load_articles("hackernews_articles.json")
    rundown = load_articles("rundown_articles.json")

    all_articles = bensbites + reddit + hackernews + rundown

    all_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)

    save_combined(all_articles)
    print(f"Combined {len(all_articles)} articles:")
    print(f"  - Ben's Bites: {len(bensbites)}")
    print(f"  - Reddit: {len(reddit)}")
    print(f"  - Hacker News: {len(hackernews)}")
    print(f"  - The Rundown: {len(rundown)}")
    print(f"  - Total: {len(all_articles)}")


if __name__ == "__main__":
    main()
