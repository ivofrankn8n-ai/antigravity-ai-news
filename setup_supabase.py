#!/usr/bin/env python3
"""
Setup script - Run this once to set up Supabase
Creates the articles table and syncs local data
"""

import json
import requests
from pathlib import Path

SUPABASE_URL = "https://dwnldnuvnwolvlfqgmobg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3bmxkbnV2bndvdmxmcWdtb2JnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1MjY2MDcsImV4cCI6MjA4NzEwMjYwN30.OpLDFT8PeBvp-sS_K0IlviVOUDhoF6lBquVmNn0bkpQ"


def create_table():
    """Create articles table"""
    print("Creating articles table...")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    # Create table using SQL
    sql = """
    CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        subtitle TEXT,
        url TEXT NOT NULL,
        source TEXT NOT NULL,
        published_at TIMESTAMPTZ,
        saved BOOLEAN DEFAULT FALSE,
        tags JSONB DEFAULT '[]',
        reading_time TEXT,
        score INTEGER DEFAULT 0,
        comments INTEGER DEFAULT 0,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """

    # Try to create table using REST API
    url = f"{SUPABASE_URL}/rest/v1/"

    # Insert a test record to create table if not exists
    test_article = {
        "id": "test_001",
        "title": "Test Article",
        "url": "https://example.com",
        "source": "Test",
    }

    resp = requests.post(url + "articles", headers=headers, json=test_article)

    if resp.status_code in [200, 201]:
        print("✓ Table created/verified!")
        # Delete test record
        requests.delete(url + "articles?id=eq.test_001", headers=headers)
        return True
    elif "relation" in resp.text.lower() and "does not exist" in resp.text.lower():
        print("✗ Table doesn't exist. Please create it manually in Supabase dashboard:")
        print("  1. Go to https://supabase.com/dashboard")
        print("  2. Select your project")
        print("  3. Click SQL Editor")
        print("  4. Run the SQL from supabase_schema.sql")
        return False
    else:
        print(f"Response: {resp.status_code} - {resp.text[:200]}")
        return False


def sync_articles():
    """Sync local articles to Supabase"""
    print("\nSyncing articles to Supabase...")

    articles_file = Path(".tmp/articles.json")
    if not articles_file.exists():
        print("✗ No articles.json found")
        return

    with open(articles_file) as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    url = f"{SUPABASE_URL}/rest/v1/articles"

    # Send in batches of 100
    batch_size = 100
    for i in range(0, len(articles), batch_size):
        batch = articles[i : i + batch_size]

        # Clean up article data
        clean_batch = []
        for a in batch:
            clean_batch.append(
                {
                    "id": a.get("id", ""),
                    "title": a.get("title", ""),
                    "subtitle": a.get("subtitle", ""),
                    "url": a.get("url", ""),
                    "source": a.get("source", ""),
                    "published_at": a.get("published_at", None),
                    "saved": a.get("saved", False),
                    "tags": json.dumps(a.get("tags", [])),
                    "reading_time": a.get("reading_time", ""),
                    "score": a.get("score", 0),
                    "comments": a.get("comments", 0),
                }
            )

        resp = requests.post(url, headers=headers, json=clean_batch)

        if resp.status_code in [200, 201]:
            print(f"✓ Synced {len(batch)} articles")
        else:
            print(f"✗ Error: {resp.status_code} - {resp.text[:100]}")

    print("\n✓ Sync complete!")


def main():
    print("=" * 50)
    print("Supabase Setup Script")
    print("=" * 50)

    # Create table
    create_table()

    # Sync articles
    sync_articles()

    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
