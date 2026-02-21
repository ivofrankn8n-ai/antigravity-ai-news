-- Supabase Database Schema for AI News Dashboard

-- Create articles table
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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_saved ON articles(saved);

-- Enable Row Level Security (optional)
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- Create policy for anonymous access (read/write)
DROP POLICY IF EXISTS "Allow anonymous access" ON articles;
CREATE POLICY "Allow anonymous access" ON articles FOR ALL USING (true) WITH CHECK (true);

-- Create a function to upsert articles
CREATE OR REPLACE FUNCTION upsert_article(
    p_id TEXT,
    p_title TEXT,
    p_subtitle TEXT,
    p_url TEXT,
    p_source TEXT,
    p_published_at TIMESTAMPTZ,
    p_saved BOOLEAN DEFAULT FALSE,
    p_tags JSONB DEFAULT '[]'::JSONB,
    p_reading_time TEXT DEFAULT '',
    p_score INTEGER DEFAULT 0,
    p_comments INTEGER DEFAULT 0
)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO articles (id, title, subtitle, url, source, published_at, saved, tags, reading_time, score, comments)
    VALUES (p_id, p_title, p_subtitle, p_url, p_source, p_published_at, p_saved, p_tags, p_reading_time, p_score, p_comments)
    ON CONFLICT (id) DO UPDATE SET
        title = EXCLUDED.title,
        subtitle = EXCLUDED.subtitle,
        url = EXCLUDED.url,
        source = EXCLUDED.source,
        published_at = EXCLUDED.published_at,
        tags = EXCLUDED.tags,
        reading_time = EXCLUDED.reading_time,
        score = EXCLUDED.score,
        comments = EXCLUDED.comments;
END;
$$;

-- Function to get articles from last 24 hours
CREATE OR REPLACE FUNCTION get_recent_articles(hours INTEGER DEFAULT 24)
RETURNS SETOF articles
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM articles
    WHERE published_at >= NOW() - INTERVAL '1 hour' * hours
    ORDER BY published_at DESC;
END;
$$;
