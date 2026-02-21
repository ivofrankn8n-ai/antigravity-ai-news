# The Rundown AI Scraping

## Source Details
- URL: https://www.therundown.ai/
- Platform: Beehiiv
- Type: Daily AI Newsletter
- Subscribers: 2M+

## API Endpoint
- Posts JSON: https://www.therundown.ai/posts
- Similar structure to Ben's Bites

## Article URL Pattern
- Archive: https://www.therundown.ai/archive
- Individual: https://www.therundown.ai/p/{slug}

## Scraping Approach
1. Fetch posts from /posts endpoint
2. Filter articles from last 24 hours
3. Parse JSON for title, subtitle, URL, date
4. Store in article schema format
