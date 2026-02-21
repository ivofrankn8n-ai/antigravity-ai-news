// Supabase Edge Function for scraping AI news
// Run with: supabase functions invoke scrape-ai-news

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

const SOURCES = {
  'bensbites': 'https://bensbites.beehiiv.com/posts',
  'rundown': 'https://www.therundown.ai/posts',
}

async function fetchWithTimeout(url, timeout = 10000) {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeout)
  
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      signal: controller.signal
    })
    clearTimeout(id)
    return response
  } catch (e) {
    clearTimeout(id)
    throw e
  }
}

function parseArticles(html, source) {
  // Simple parsing - in production use a proper HTML parser
  const articles = []
  const titleMatch = html.match(/<h3[^>]*>([^<]+)<\/h3>/g) || []
  const urlMatch = html.match(/href="([^"]+)"/g) || []
  
  // Return mock data for demo
  return [
    {
      id: `${source}_${Date.now()}`,
      title: `AI News Update - ${new Date().toLocaleDateString()}`,
      subtitle: `Latest ${source} news about AI, ML and technology`,
      url: `https://example.com/${source}`,
      source: source,
      published_at: new Date().toISOString(),
      saved: false,
      tags: ['AI', 'News'],
      score: Math.floor(Math.random() * 100),
      comments: Math.floor(Math.random() * 50)
    }
  ]
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { action } = await req.json()
    
    if (action === 'scrape') {
      const allArticles = []
      
      // Scrape each source
      for (const [name, url] of Object.entries(SOURCES)) {
        try {
          const response = await fetchWithTimeout(url, 15000)
          const text = await response.text()
          const articles = parseArticles(text, name)
          allArticles.push(...articles)
        } catch (e) {
          console.error(`Error scraping ${name}:`, e.message)
        }
      }
      
      // Sort by date
      allArticles.sort((a, b) => new Date(b.published_at) - new Date(a.published_at))
      
      return new Response(JSON.stringify({ 
        success: true, 
        count: allArticles.length,
        articles: allArticles 
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    if (action === 'status') {
      return new Response(JSON.stringify({ 
        status: 'ok',
        timestamp: new Date().toISOString()
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }
    
    return new Response(JSON.stringify({ error: 'Unknown action' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
    
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})
