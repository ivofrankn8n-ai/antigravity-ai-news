#!/usr/bin/env python3
"""
Run all scrapers and aggregate articles
"""

import subprocess
import sys
from pathlib import Path

SCRAPERS = [
    ("Ben's Bites", "tools/scrape_bensbites.py"),
    ("The Rundown AI", "tools/scrape_rundown.py"),
    ("Reddit", "tools/scrape_reddit.py"),
    ("Hacker News", "tools/scrape_hackernews.py"),
]


def run_scraper(name, script):
    """Run a scraper script"""
    print(f"\n{'=' * 50}")
    print(f"Running {name} scraper...")
    print("=" * 50)

    result = subprocess.run([sys.executable, script], capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


def main():
    """Run all scrapers"""
    Path(".tmp").mkdir(exist_ok=True)

    success = True
    for name, script in SCRAPERS:
        if not run_scraper(name, script):
            print(f"Warning: {name} scraper failed")
            success = False

    print(f"\n{'=' * 50}")
    print("Aggregating articles...")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, "tools/aggregate_articles.py"], capture_output=True, text=True
    )
    print(result.stdout)

    if success:
        print("\nAll scrapers completed successfully!")
    else:
        print("\nSome scrapers failed. Check logs above.")


if __name__ == "__main__":
    main()
