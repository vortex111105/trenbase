// /api/track.js — Guarda ventas y respuestas de onboarding en Supabase
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;
const SITE_URL = process.env.ALLOWED_ORIGIN || 'https://trenbase.vercel.app';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', SITE_URL);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Validate JWT and ensure the user_id matches the authenticated user
  const authHeader = req.headers['authorization'] || '';
  const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;
  if (!token) return res.status(401).json({ error: 'Authorization token required' });

  const userRes = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${token}` }
  });
  if (!userRes.ok) return res.status(401).json({ error: 'Invalid or expired token' });
  const authUser = await userRes.json();

  const { type, user_id, product_name, product_cat, product_score, answer, plan } = req.body;

  if (!type || !user_id) return res.status(400).json({ error: 'Missing fields' });
  if (authUser.id !== user_id) return res.status(403).json({ error: 'Forbidden: user_id mismatch' });

  try {
    if (type === 'sale') {
      await fetch(`${SUPABASE_URL}/rest/v1/sales`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({ user_id, product_name, product_cat, product_score })
      });
    } else if (type === 'onboarding') {
      await fetch(`${SUPABASE_URL}/rest/v1/onboarding`, {
        method: 'POST',
        headers: {
          'apikey': SUPABASE_KEY,
          'Authorization': `Bearer ${SUPABASE_KEY}`,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({ user_id, answer, plan })
      });
    }

    return res.status(200).json({ ok: true });
  } catch(e) {
    return res.status(500).json({ error: e.message });
  }
}
