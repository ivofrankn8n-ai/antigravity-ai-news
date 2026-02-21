#!/usr/bin/env python3
"""
Supabase client for storing and retrieving articles
"""

from dotenv import load_dotenv
load_dotenv()
import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class SupabaseClient:
    def __init__(self, url=None, key=None):
        self.url = url or SUPABASE_URL
        self.key = key or SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def create_table(self):
        """Create articles table if not exists"""
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
        
        CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
        CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at DESC);
        CREATE INDEX IF NOT EXISTS idx_articles_saved ON articles(saved);
        """

        response = requests.post(
            f"{self.url}/rest/v1/rpc/exec_sql",
            headers=self.headers,
            json={"query": sql},
        )
        return response.status_code in (200, 201, 204)

    def insert_article(self, article):
        """Insert or update an article"""
        data = {
            "id": article.get("id"),
            "title": article.get("title"),
            "subtitle": article.get("subtitle", ""),
            "url": article.get("url"),
            "source": article.get("source"),
            "published_at": article.get("published_at"),
            "saved": article.get("saved", False),
            "tags": json.dumps(article.get("tags", [])),
            "reading_time": article.get("reading_time", ""),
            "score": article.get("score", 0),
            "comments": article.get("comments", 0),
        }

        response = requests.post(
            f"{self.url}/rest/v1/articles", headers=self.headers, json=data
        )
        return response.status_code in (200, 201)

    def insert_articles(self, articles, batch_size=50):
        """Bulk insert articles in batches with duplicate handling"""
        total_inserted = 0

        # Get existing IDs to avoid duplicates
        existing = self.get_articles(limit=1000)
        existing_ids = {a.get("id") for a in existing}

        for i in range(0, len(articles), batch_size):
            batch = articles[i : i + batch_size]
            data = []
            for article in batch:
                # Skip if missing required fields or already exists
                if (
                    not article.get("id")
                    or not article.get("title")
                    or not article.get("url")
                ):
                    continue
                if article.get("id") in existing_ids:
                    continue

                data.append(
                    {
                        "id": article.get("id"),
                        "title": article.get("title"),
                        "subtitle": article.get("subtitle", ""),
                        "url": article.get("url"),
                        "source": article.get("source"),
                        "published_at": article.get("published_at"),
                        "saved": article.get("saved", False),
                        "tags": json.dumps(article.get("tags", [])),
                        "reading_time": article.get("reading_time", ""),
                        "score": article.get("score", 0),
                        "comments": article.get("comments", 0),
                    }
                )
                existing_ids.add(article.get("id"))

            if not data:
                continue

            response = requests.post(
                f"{self.url}/rest/v1/articles", headers=self.headers, json=data
            )
            if response.status_code in (200, 201):
                total_inserted += len(data)
            else:
                print(
                    f"Batch {i // batch_size + 1} failed: {response.status_code} - {response.text[:200]}"
                )

        return total_inserted > 0

    def get_articles(self, source=None, saved=None, limit=100):
        """Fetch articles from Supabase"""
        params = {"limit": limit, "order": "published_at.desc"}

        if source:
            params["source"] = f"eq.{source}"
        if saved is not None:
            params["saved"] = f"eq.{str(saved).lower()}"

        response = requests.get(
            f"{self.url}/rest/v1/articles", headers=self.headers, params=params
        )

        if response.status_code == 200:
            return response.json()
        return []

    def update_saved(self, article_id, saved):
        """Update saved status of an article"""
        response = requests.patch(
            f"{self.url}/rest/v1/articles?id=eq.{article_id}",
            headers=self.headers,
            json={"saved": saved},
        )
        return response.status_code in (200, 201)

    def sync_from_local(self):
        """Sync articles from local JSON files to Supabase"""
        articles_file = Path(".tmp/articles.json")
        if not articles_file.exists():
            print("No local articles found")
            return 0

        with open(articles_file) as f:
            articles = json.load(f)

        count = self.insert_articles(articles)
        print(f"Synced {count} articles to Supabase")
        return count


def main():
    """Test Supabase connection"""
    client = SupabaseClient()

    if not client.url or not client.key:
        print("Error: SUPABASE_URL and SUPABASE_KEY not set in .env")
        print("Please add your Supabase credentials to .env")
        return

    print(f"Connected to: {client.url}")

    # Test fetching articles
    articles = client.get_articles(limit=5)
    print(f"Found {len(articles)} existing articles")


if __name__ == "__main__":
    main()
