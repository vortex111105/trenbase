export const config = { runtime: 'edge' };

// ── RATE LIMIT ───────────────────────────────────────────────────────────────
const rateLimitMap = new Map();

function getRateLimit(ip, plan) {
  const now = Date.now();
  const windowMs = 60 * 1000;
  const maxRequests = plan === 'pro' ? 20 : 10;

  const entry = rateLimitMap.get(ip) || { count: 0, resetAt: now + windowMs };
  if (now > entry.resetAt) { entry.count = 0; entry.resetAt = now + windowMs; }
  entry.count++;
  rateLimitMap.set(ip, entry);

  return {
    allowed: entry.count <= maxRequests,
    remaining: Math.max(0, maxRequests - entry.count),
    resetIn: Math.ceil((entry.resetAt - now) / 1000),
  };
}

// ── MODEL TIERS (mínimos tokens, máxima utilidad) ────────────────────────────
// Free/Starter → Haiku: respuestas rápidas, bajo costo
// Pro          → Sonnet: análisis profundo, mayor calidad
const MODEL_BY_PLAN = {
  free:    { model: 'claude-haiku-4-5-20251001', maxTokens: 400  },
  starter: { model: 'claude-haiku-4-5-20251001', maxTokens: 600  },
  pro:     { model: 'claude-sonnet-4-6',          maxTokens: 1200 },
};

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown';

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
  }

  const { messages, system, plan = 'free' } = body;
  if (!messages || !Array.isArray(messages)) {
    return new Response(JSON.stringify({ error: 'Invalid body' }), { status: 400 });
  }

  const limit = getRateLimit(ip, plan);
  if (!limit.allowed) {
    return new Response(JSON.stringify({
      error: `Demasiadas consultas. Esperá ${limit.resetIn} segundos.`
    }), { status: 429, headers: { 'Content-Type': 'application/json' } });
  }

  const { model, maxTokens } = MODEL_BY_PLAN[plan] || MODEL_BY_PLAN.free;

  // Pro conserva más contexto, otros menos (ahorra tokens)
  const historyLimit = plan === 'pro' ? 12 : 6;
  const trimmedMessages = messages.slice(-historyLimit);

  // System prompt compacto — max 800 chars
  const trimmedSystem = (system || '').slice(0, 800);

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model,
        max_tokens: maxTokens,
        system: trimmedSystem,
        messages: trimmedMessages,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      return new Response(JSON.stringify({ error: data.error?.message || 'API error' }), { status: response.status });
    }

    const text = (data.content || [])
      .filter(b => b.type === 'text')
      .map(b => b.text)
      .join('');

    return new Response(JSON.stringify({ text, model }), {
      status: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal error: ' + err.message }), { status: 500 });
  }
}
