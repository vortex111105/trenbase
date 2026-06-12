// /api/describe.js — Agente de Marketing
// Una sola llamada a Claude Haiku genera todo el copy de publicación:
// MercadoLibre título + descripción, TikTok script, Instagram caption, SEO keywords
// Costo estimado: ~0.0004 USD por producto (Haiku input+output ~1200 tokens)

export const config = { runtime: 'edge' };

// Rate limit simple por IP
const rlMap = new Map();
function checkRL(ip) {
  const now = Date.now();
  const e = rlMap.get(ip) || { n: 0, reset: now + 60000 };
  if (now > e.reset) { e.n = 0; e.reset = now + 60000; }
  e.n++;
  rlMap.set(ip, e);
  return e.n <= 15; // 15 generaciones/minuto por IP
}

const SYSTEM = `Sos un experto en marketing de dropshipping para LATAM (Argentina, Uruguay, Chile). Generás copy de alta conversión para productos trending. Respondés SOLO con JSON válido, sin markdown.`;

function buildPrompt(product) {
  const { name, cat, score, marginStr, comp, priceStr, plts, regions } = product;
  const plataformas = (plts || []).join(', ');
  const paises = (regions || []).join(', ');

  return `Generá copy de marketing para este producto de dropshipping:
Nombre: ${name}
Categoría: ${cat}
TrendScore: ${score}/100
Margen: ${marginStr}
Competencia: ${comp}
Precio estimado: ${priceStr}
Trending en: ${plataformas}
Países: ${paises}

Respondé SOLO con este JSON (sin markdown):
{
  "ml_titulo": "Título para MercadoLibre, max 60 chars, con keywords de búsqueda",
  "ml_descripcion": "Descripción completa para MercadoLibre, 150-200 palabras, con beneficios, uso, garantía implícita",
  "tiktok_script": "Script para video TikTok 30 segundos. Formato: [0s] Hook. [8s] Problema. [16s] Solución/producto. [24s] CTA.",
  "instagram_caption": "Caption Instagram con emoji, 80-100 palabras + 15 hashtags relevantes en español e inglés",
  "keywords_seo": ["array", "de", "10", "keywords", "para", "google", "shopping"],
  "precio_sugerido_ars": "Precio de venta sugerido en ARS con margen aplicado",
  "punto_diferencial": "1 frase corta que diferencia este producto de la competencia"
}`;
}

export default async function handler(req) {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST', 'Access-Control-Allow-Headers': 'Content-Type' }
    });
  }

  if (req.method !== 'POST')
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown';
  if (!checkRL(ip))
    return new Response(JSON.stringify({ error: 'Rate limit. Esperá 1 minuto.' }), { status: 429 });

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
  }

  const { product, plan = 'free' } = body;
  if (!product?.name)
    return new Response(JSON.stringify({ error: 'Falta product.name' }), { status: 400 });

  // Solo planes con IA pueden generar copy
  if (plan === 'free')
    return new Response(JSON.stringify({ error: 'Requiere plan Starter o Pro', upgrade: true }), { status: 403 });

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey)
    return new Response(JSON.stringify({ error: 'API key no configurada' }), { status: 500 });

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001', // Haiku: rápido y barato para copy estructurado
        max_tokens: 900,
        system: SYSTEM,
        messages: [{ role: 'user', content: buildPrompt(product) }],
      }),
    });

    const data = await response.json();
    if (!response.ok)
      return new Response(JSON.stringify({ error: data.error?.message || 'Error API' }), { status: response.status });

    const raw = (data.content?.[0]?.text || '').trim()
      .replace(/^```json\s*/i, '').replace(/^```\s*/i, '').replace(/\s*```$/i, '');

    let copy;
    try {
      copy = JSON.parse(raw);
    } catch {
      return new Response(JSON.stringify({ error: 'Respuesta inválida de IA', raw }), { status: 500 });
    }

    return new Response(JSON.stringify({ copy, model: 'claude-haiku-4-5-20251001', product: product.name }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'private, max-age=86400', // cache 24hs en cliente
      },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
