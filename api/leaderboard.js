// API pública para el leaderboard - sin autenticación
const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, max-age=300'); // cache 5 min

  try {
    const salesRes = await fetch(
      `${SUPABASE_URL}/rest/v1/sales?select=product_name,product_cat&limit=500`,
      { headers: { 'apikey': SUPABASE_KEY, 'Authorization': `Bearer ${SUPABASE_KEY}` } }
    );
    const sales = await salesRes.json();

    // Aggregate
    const byProduct = {};
    for (const s of (sales || [])) {
      byProduct[s.product_name] = (byProduct[s.product_name] || 0) + 1;
    }

    const topProducts = Object.entries(byProduct)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([name, count]) => ({ name, count }));

    return res.json({
      total_sales: sales?.length || 0,
      top_products: topProducts,
      active_sellers: Object.keys(byProduct).length,
    });
  } catch(e) {
    return res.json({ total_sales: 0, top_products: [], active_sellers: 0 });
  }
}
