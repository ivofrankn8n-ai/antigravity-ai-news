# Project Constitution - QWEN AI Dashboard

## Data Schemas

### Article Schema
```json
{
  "id": "string",
  "title": "string",
  "subtitle": "string",
  "url": "string",
  "source": "string",
  "published_at": "datetime",
  "saved": "boolean",
  "tags": ["string"]
}
```

### Source Schema
```json
{
  "name": "string",
  "type": "string",
  "url": "string",
  "last_scraped": "datetime"
}
```

## Behavioral Rules

1. Only scrape articles from the last 24 hours
2. Preserve saved articles across sessions
3. Run scraping job every 24 hours
4. Store data locally until Supabase integration
5. Design dashboard to be responsive and interactive

## Architectural Invariants

1. 3-layer architecture (Architecture/SOPs, Navigation, Tools)
2. Data-first approach - define schemas before implementation
3. Self-healing automation with error recovery
4. Separate concerns between data collection, processing, and presentation
