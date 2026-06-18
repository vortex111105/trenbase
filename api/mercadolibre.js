export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  const q = req.query?.q;
  if (!q) return res.status(400).json({ error: 'Falta parámetro q' });

  try {
    // Para busquedas publicas de precio sugerido de venta en Argentina (MLA)
    // No requiere Token para lectura basica
    const url = `https://api.mercadolibre.com/sites/MLA/search?q=${encodeURIComponent(q)}&limit=5`;
    const response = await fetch(url);
    const data = await response.json();

    if (!data.results || data.results.length === 0) {
      return res.json({ query: q, average_price_ars: 0, products: [] });
    }

    let total = 0;
    const topProducts = data.results.map(p => {
      total += p.price;
      return {
        id: p.id,
        title: p.title,
        price: p.price,
        currency: p.currency_id,
        link: p.permalink
      };
    });

    const average_price = total / topProducts.length;

    return res.json({
      query: q,
      currency: topProducts[0].currency,
      average_price_ars: average_price,
      products: topProducts
    });

  } catch(e) {
    console.error('[/api/mercadolibre]', e.message);
    return res.status(500).json({ error: e.message });
  }
}
