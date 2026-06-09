// Proxy para buscar imágenes de productos por nombre
// Usa DuckDuckGo instant answers (sin API key, sin límites)
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, max-age=86400'); // cache 24hs

  const { q } = req.query;
  if (!q) return res.status(400).json({ error: 'Missing query' });

  try {
    // DuckDuckGo instant answer API
    const query = encodeURIComponent(q + ' producto');
    const url = `https://api.duckduckgo.com/?q=${query}&format=json&no_html=1&skip_disambig=1`;
    
    const r = await fetch(url, {
      headers: { 'User-Agent': 'TrendBase/1.0' }
    });
    const data = await r.json();

    // Try to get image from DDG result
    if (data.Image && data.Image.length > 0) {
      return res.json({ url: data.Image });
    }

    // Try related topics
    for (const topic of (data.RelatedTopics || [])) {
      if (topic.Icon?.URL) {
        return res.json({ url: topic.Icon.URL });
      }
    }

    return res.json({ url: null });
  } catch(e) {
    return res.json({ url: null });
  }
}
