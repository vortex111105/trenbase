// /api/admin.js — Panel de datos para el owner
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;
const ADMIN_SECRET = process.env.ADMIN_SECRET || 'trendbase2025admin';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Simple auth
  const secret = req.headers['x-admin-secret'] || req.query.secret;
  if (secret !== ADMIN_SECRET) return res.status(401).json({ error: 'Unauthorized' });

  try {
    // Get sales summary
    const salesRes = await fetch(`${SUPABASE_URL}/rest/v1/sales?select=product_name,product_cat,created_at&order=created_at.desc&limit=500`, {
      headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
    });
    const sales = await salesRes.json();

    // Get onboarding summary
    const onboardingRes = await fetch(`${SUPABASE_URL}/rest/v1/onboarding?select=answer,plan,created_at&order=created_at.desc&limit=500`, {
      headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` }
    });
    const onboarding = await onboardingRes.json();

    // Aggregate sales by product
    const salesByProduct = {};
    for (const s of (sales || [])) {
      const key = s.product_name;
      salesByProduct[key] = (salesByProduct[key] || 0) + 1;
    }
    const topProducts = Object.entries(salesByProduct)
      .sort((a,b) => b[1]-a[1])
      .slice(0, 20)
      .map(([name, count]) => ({ name, count }));

    // Aggregate onboarding answers
    const answers = { yes: 0, no: 0, exploring: 0 };
    for (const o of (onboarding || [])) {
      if (answers[o.answer] !== undefined) answers[o.answer]++;
    }

    return res.json({
      total_sales: sales?.length || 0,
      top_products: topProducts,
      onboarding_total: onboarding?.length || 0,
      onboarding_answers: answers,
      recent_sales: (sales || []).slice(0, 10),
    });
  } catch(e) {
    return res.status(500).json({ error: e.message });
  }
}
