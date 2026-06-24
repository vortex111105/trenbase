// Estadísticas reales para la landing page
// Consulta Supabase: ventas de hoy, vendedores activos, producto estrella
// Cache: 5 minutos

const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=600');

  try {
    const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD

    const [salesRes, totalRes] = await Promise.all([
      // Ventas de hoy
      fetch(
        `${SUPABASE_URL}/rest/v1/sales?select=product_name,user_id&created_at=gte.${today}T00:00:00Z&limit=1000`,
        { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
      ),
      // Total de ventas históricas (para el contador de "productos analizados")
      fetch(
        `${SUPABASE_URL}/rest/v1/products?select=id&limit=1`,
        { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}`, Prefer: 'count=exact' } }
      ),
    ]);

    let sales_today = 0;
    let active_sellers = 0;
    let top_product = 'Masajeador Facial';
    let products_count = 500;

    if (salesRes.ok) {
      const salesData = await salesRes.json();
      const todaySales = salesData || [];
      sales_today = todaySales.length;

      // Vendedores únicos hoy
      const uniqueUsers = new Set(todaySales.map(s => s.user_id).filter(Boolean));
      active_sellers = uniqueUsers.size;

      // Producto más vendido hoy
      const byProduct = {};
      todaySales.forEach(s => {
        if (s.product_name) byProduct[s.product_name] = (byProduct[s.product_name] || 0) + 1;
      });
      const sorted = Object.entries(byProduct).sort((a, b) => b[1] - a[1]);
      if (sorted.length > 0) top_product = sorted[0][0];
    }

    // Total de productos en la base de datos
    if (totalRes.ok) {
      const countHeader = totalRes.headers.get('content-range');
      if (countHeader) {
        const match = countHeader.match(/\/(\d+)$/);
        if (match) products_count = parseInt(match[1]);
      }
    }

    return res.json({
      sales_today,
      active_sellers,
      top_product,
      products_count,
      updated_at: new Date().toISOString(),
    });
  } catch (e) {
    return res.json({
      sales_today: 0,
      active_sellers: 0,
      top_product: 'Masajeador Facial',
      products_count: 500,
      fallback: true,
    });
  }
}
