# Findings - AI Dashboard Project

## Ben's Bites Analysis
- Main URL: https://bensbites.beehiiv.com/
- Posts API endpoint discovered: https://bensbites.beehiiv.com/posts
- API returns JSON with article metadata including titles, subtitles, URLs, and timestamps
- Articles have consistent structure with estimated reading times and tags
- Scraping tool: tools/scrape_bensbites.py

## Reddit Sources
- Selected subreddits: r/artificial, r/OpenAI
- Uses public Reddit API (no credentials needed)
- Scraping tool: tools/scrape_reddit.py
- Hacker News also supported: tools/scrape_hackernews.py

## The Rundown AI Analysis
- Main URL: https://www.therundown.ai/
- Posts API endpoint: https://www.therundown.ai/posts
- Runs on Beehiiv platform (same as Ben's Bites)
- Archive page: https://www.therundown.ai/archive
- Article URLs follow pattern: /p/{slug}
- 2M+ subscribers, daily AI newsletter
- Scraping tool: tools/scrape_rundown.py

## Dashboard Implementation

### Topic Classification System
Four main categories:
1. Agentic AI - keywords: agent, agents, automation, autonomous, swarm, cli, codex
2. Market Updates - keywords: funding, valuation, investor, acquisition, billion, startup, vc
3. Demanded AI Skills - keywords: skill, learn, tutorial, course, coding, programming, api
4. New Model Releases - keywords: gpt, claude, gemini, llama, mistral, release, launch

### AI Chatbot
- Supports multiple API providers: OpenAI, Anthropic (Claude), Google (Gemini), Groq, OpenRouter, NVIDIA
- Requires API key and model name configuration
- Provides clickable article links in responses
- Uses conversation context window for better responses

### Data Flow
1. Scrapers fetch articles from sources → .tmp/ folder
2. Aggregate_articles.py combines all sources → .tmp/articles.json
3. dashboard.html loads from .tmp/articles.json via local server
4. Articles classified by topic using keyword matching

### Files Structure
- dashboard.html - Main application
- tools/ - Scraping scripts
- .tmp/ - Cached article data
- supabase_schema.sql - Database schema (for future use)
