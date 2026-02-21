#!/usr/bin/env python3
"""
Sync local articles to Supabase
"""

from dotenv import load_dotenv
load_dotenv()
import os
import json
import requests
import sys
from pathlib import Path

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


def main():
    articles_file = Path(".tmp/articles.json")
    if not articles_file.exists():
        print("Error: .tmp/articles.json not found")
        print("Run 'python tools/run_all_scrapers.py' first")
        sys.exit(1)

    with open(articles_file) as f:
        articles = json.load(f)

    for a in articles:
        if "tags" in a and isinstance(a["tags"], list):
            a["tags"] = json.dumps(a["tags"])

    batch_size = 50
    total = len(articles)

    for i in range(0, total, batch_size):
        batch = articles[i : i + batch_size]
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/articles", headers=headers, json=batch
        )
        print(f"Batch {i // batch_size + 1}: {resp.status_code}")

    print(f"\nSynced {total} articles to Supabase!")


if __name__ == "__main__":
    main()
