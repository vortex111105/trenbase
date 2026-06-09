// /api/track.js — Guarda ventas y respuestas de onboarding en Supabase
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { type, user_id, product_name, product_cat, product_score, answer, plan } = req.body;

  if (!type || !user_id) return res.status(400).json({ error: 'Missing fields' });

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
