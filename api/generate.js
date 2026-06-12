// /api/generate.js — Genera productos con IA y los guarda en Supabase
// Se llama cada 6 horas desde un cron job o manualmente
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;
const CRON_SECRET = process.env.CRON_SECRET;

const BATCH_PROMPTS = [
  { label: 'Tecnología y Gadgets', cat: 'Tecnología', count: 50 },
  { label: 'Belleza y Cuidado Personal', cat: 'Belleza', count: 50 },
  { label: 'Hogar y Decoración', cat: 'Hogar', count: 50 },
  { label: 'Moda y Accesorios', cat: 'Moda', count: 50 },
  { label: 'Deportes y Fitness', cat: 'Deportes', count: 50 },
  { label: 'Cocina y Alimentación', cat: 'Hogar', count: 50 },
  { label: 'Cuidado del Cabello y Piel', cat: 'Belleza', count: 50 },
  { label: 'Gadgets y Accesorios Tech', cat: 'Tecnología', count: 50 },
  { label: 'Decoración y Organización', cat: 'Hogar', count: 50 },
  { label: 'Ropa Deportiva y Casual', cat: 'Moda', count: 50 },
];

function makePrompt(label, count) {
  return `Sos un sistema de inteligencia de mercado que monitorea 47.000+ productos en TikTok, Instagram, YouTube, Pinterest, Facebook, Amazon, Mercado Libre, Google Trends y AliExpress para LATAM.

Generá ${count} productos virales de "${label}" para dropshipping en Argentina, Uruguay y Chile.
Respondé SOLO con JSON array, sin markdown, sin texto extra.

Formato:
{"name":"Nombre","cat":"Tecnología","score":95,"change":"+18%","changeNum":18,"plts":["TT","IG"],"margin":52,"marginStr":"45-60%","hot":true,"regions":["AR","UY","CL"],"comp":"Media","priceMin":20,"priceStr":"$20-$50","history":[60,63,67,65,70,74,72,77,80,78,83,86,84,89,92,95]}

- cat: Tecnología, Belleza, Hogar, Moda, o Deportes
- score 35-99, ordenados mayor a menor
- history: exactamente 16 números 0-100
- plts: subconjunto de TT,IG,YT,PT,FB,AM,ML,GT,AE
- regions: subconjunto de AR,UY,CL
- comp: Baja, Media, o Alta
- Productos variados, actuales, sin repetir
- Solo el JSON array`;
}

const SUPPLIERS = [
  { name: 'AliExpress', icon: 'AE', meta: 'Envío estándar · 15-25 días', aff: true },
  { name: 'Dropdeal', icon: 'DD', meta: 'Envío a LATAM · 5-10 días', aff: true },
  { name: 'Droppi', icon: 'DR', meta: 'Pago Contra Entrega Colombia · 2-5 días', aff: true },
  { name: 'Rocketfy', icon: 'RF', meta: 'Envíos Nacionales LATAM · 3-6 días', aff: true },
  { name: 'CJ Dropshipping', icon: 'CJ', meta: 'Bodega LATAM · 7-12 días', aff: false },
  { name: 'TiendaMia', icon: 'TM', meta: 'Importación fácil · 10-15 días', aff: true },
  { name: 'Zendrop', icon: 'ZD', meta: 'Envío express · 3-7 días', aff: false },
  { name: 'Spocket', icon: 'SP', meta: 'Proveedores locales · 5-8 días', aff: true },
];

function searchUrl(platform, name) {
  const q = encodeURIComponent(name);
  const map = {
    AliExpress: `https://www.aliexpress.com/wholesale?SearchText=${q}`,
    Alibaba: `https://www.alibaba.com/trade/search?SearchText=${q}`,
    DHgate: `https://www.dhgate.com/wholesale/search.do?act=search&searchkey=${q}`,
    'CJ Dropshipping': `https://cjdropshipping.com/list.html?searchKey=${q}`,
    Dropdeal: `https://dropdeal.com/search?q=${q}&ref=trendbase`,
    Droppi: `https://droppi.com/search?q=${q}&ref=trendbase`,
    Rocketfy: `https://rocketfy.co/search?q=${q}&ref=trendbase`,
    TiendaMia: `https://tiendamia.com/ar/search?q=${q}&ref=trendbase`,
    Zendrop: `https://app.zendrop.com/find-products?search=${q}`,
    Spocket: `https://app.spocket.co/products?search=${q}`,
  };
  return map[platform] || `https://www.aliexpress.com/wholesale?SearchText=${q}&af=trendbase`;
}

async function generateBatch(apiKey, label, count) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 8000,
      messages: [{ role: 'user', content: makePrompt(label, count) }]
    })
  });

  const raw = await res.text();
  if (!res.ok) throw new Error(`API ${res.status}: ${raw.slice(0, 200)}`);
  const data = JSON.parse(raw);
  let text = (data.content?.[0]?.text || '').trim()
    .replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '').trim();
  const match = text.match(/\[[\s\S]*\]/);
  if (!match) throw new Error('No JSON array en respuesta');
  
  // Try to parse, if fails try to extract valid objects one by one
  try {
    return JSON.parse(match[0]);
  } catch(e) {
    // Extract individual JSON objects
    const objects = [];
    let depth = 0, start = -1;
    const str = match[0];
    for(let i = 0; i < str.length; i++) {
      if(str[i] === '{') { if(depth === 0) start = i; depth++; }
      else if(str[i] === '}') {
        depth--;
        if(depth === 0 && start !== -1) {
          try { objects.push(JSON.parse(str.slice(start, i+1))); } catch(e2) {}
          start = -1;
        }
      }
    }
    if(objects.length === 0) throw new Error('No se pudieron extraer objetos válidos');
    return objects;
  }
}

async function saveToSupabase(products) {
  const rows = products.map((p, idx) => ({
    name: p.name,
    cat: p.cat,
    score: p.score,
    change: p.change,
    change_num: p.changeNum,
    plts: p.plts,
    margin: p.margin,
    margin_str: p.marginStr,
    hot: p.hot,
    regions: p.regions,
    comp: p.comp,
    price_min: p.priceMin,
    price_str: p.priceStr,
    history: p.history,
    rank: idx + 1,
    suppliers: SUPPLIERS.map((s, si) => ({ ...s, url: searchUrl(s.name, p.name), price: `USD ${(p.priceMin * (0.18 + si * 0.03 + (idx % 4) * 0.02)).toFixed(2)}` })),
    updated_at: new Date().toISOString(),
  }));

  // Delete old products and insert new ones
  await fetch(`${SUPABASE_URL}/rest/v1/products`, {
    method: 'DELETE',
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal',
    },
    body: JSON.stringify({})
  });

  // Insert in batches of 50
  for (let i = 0; i < rows.length; i += 50) {
    const batch = rows.slice(i, i + 50);
    const insertRes = await fetch(`${SUPABASE_URL}/rest/v1/products`, {
      method: 'POST',
      headers: {
        'apikey': SUPABASE_KEY,
        'Authorization': `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
      },
      body: JSON.stringify(batch)
    });
    if (!insertRes.ok) {
      const err = await insertRes.text();
      throw new Error(`Supabase insert error: ${err.slice(0, 200)}`);
    }
  }
}

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');

  // Auth check
  const secret = req.query?.secret || req.headers?.['x-cron-secret'];
  if (secret !== CRON_SECRET) {
    return res.status(401).json({ error: 'No autorizado' });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'ANTHROPIC_API_KEY no configurada' });
  if (!SUPABASE_KEY) return res.status(500).json({ error: 'SUPABASE_SERVICE_KEY no configurada' });

  try {
    const allProducts = [];
    const errors = [];

    // Generate batches sequentially to avoid timeouts
    // Each batch = separate API call
    const batchIndex = parseInt(req.query?.batch || '0');
    const batch = BATCH_PROMPTS[batchIndex];

    if (!batch) return res.status(400).json({ error: `Batch ${batchIndex} no existe` });

    console.log(`Generating batch ${batchIndex}: ${batch.label}`);
    const products = await generateBatch(apiKey, batch.label, batch.count);
    
    // Get existing products from DB
    const existingRes = await fetch(`${SUPABASE_URL}/rest/v1/products?select=*&order=score.desc`, {
      headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
    });
    const existing = await existingRes.json();
    
    // If first batch, replace all. Otherwise append
    let combined;
    if (batchIndex === 0) {
      combined = products;
    } else {
      combined = [...(Array.isArray(existing) ? existing.map(p => ({
        name: p.name, cat: p.cat, score: p.score, change: p.change, changeNum: p.change_num,
        plts: p.plts, margin: p.margin, marginStr: p.margin_str, hot: p.hot,
        regions: p.regions, comp: p.comp, priceMin: p.price_min, priceStr: p.price_str, history: p.history
      })) : []), ...products];
    }

    // Sort by score and save
    combined.sort((a, b) => (b.score || 0) - (a.score || 0));
    await saveToSupabase(combined);

    const nextBatch = batchIndex + 1;
    const hasMore = nextBatch < BATCH_PROMPTS.length;

    return res.json({ 
      success: true, 
      batch: batchIndex,
      label: batch.label,
      generated: products.length,
      total: combined.length,
      nextBatch: hasMore ? nextBatch : null,
      done: !hasMore
    });

  } catch(e) {
    console.error('[/api/generate]', e.message);
    return res.status(500).json({ error: e.message });
  }
}
