// /api/products.js — Lee todos los productos de Supabase
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  try {
    // Fetch all products using offset pagination
    let allRaw = [];
    const pageSize = 1000;
    let offset = 0;

    while (true) {
      const dbRes = await fetch(
        `${SUPABASE_URL}/rest/v1/products?select=id,name,cat,score,change,change_num,plts,margin,margin_str,hot,regions,comp,price_min,price_str,history,rank,suppliers,updated_at&order=score.desc&limit=${pageSize}&offset=${offset}`,
        {
          headers: {
            'apikey': SUPABASE_KEY,
            'Authorization': `Bearer ${SUPABASE_KEY}`,
          }
        }
      );

      const batch = await dbRes.json();
      if (!Array.isArray(batch) || batch.length === 0) break;
      allRaw = allRaw.concat(batch);
      if (batch.length < pageSize) break;
      offset += pageSize;
      if (offset > 5000) break; // safety limit
    }

    if (!allRaw.length) {
      return res.json({ products: [], cached: false, generating: true, count: 0 });
    }

    // Deduplicate by name — keep highest score
    const seen = new Map();
    for (const p of allRaw) {
      const key = (p.name || '').toLowerCase().trim();
      if (!key) continue;
      if (!seen.has(key) || p.score > seen.get(key).score) {
        seen.set(key, p);
      }
    }
    const products = Array.from(seen.values()).sort((a, b) => b.score - a.score);

    const lastUpdate = products[0]?.updated_at;
    const ageMs = lastUpdate ? Date.now() - new Date(lastUpdate).getTime() : Infinity;
    const stale = ageMs > 6 * 60 * 60 * 1000;

    return res.json({
      products,
      cached: true,
      age: Math.floor(ageMs / 1000),
      stale,
      count: products.length,
      lastUpdate
    });

  } catch(e) {
    console.error('[/api/products]', e.message);
    return res.status(500).json({ error: e.message });
  }
}
