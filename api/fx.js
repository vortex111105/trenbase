// Tipos de cambio reales USD → ARS, UYU, CLP
// Fuentes: BCRA (ARS), exchangerate-api.com libre (UYU/CLP)
// Cache: 30 minutos en Vercel Edge

const CACHE_TTL = 1800; // segundos

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', `public, s-maxage=${CACHE_TTL}, stale-while-revalidate=3600`);

  try {
    // Fuente 1: BCRA (Banco Central República Argentina) — dólar oficial/blue promedio
    const [arsRes, multiRes] = await Promise.allSettled([
      fetch('https://api.bluelytics.com.ar/v2/latest'),
      fetch('https://open.er-api.com/v6/latest/USD'),
    ]);

    let ARS = 1050;
    let UYU = 39;
    let CLP = 970;

    // ARS desde Bluelytics (promedio oficial + blue)
    if (arsRes.status === 'fulfilled' && arsRes.value.ok) {
      const arsData = await arsRes.value.json();
      // Usar el tipo "blue" que es el más representativo del mercado real
      const blue = arsData?.blue;
      const oficial = arsData?.oficial;
      if (blue?.value_sell) ARS = Math.round(blue.value_sell);
      else if (oficial?.value_sell) ARS = Math.round(oficial.value_sell);
    }

    // UYU y CLP desde open.er-api.com (libre, sin clave)
    if (multiRes.status === 'fulfilled' && multiRes.value.ok) {
      const multiData = await multiRes.value.json();
      const rates = multiData?.rates || {};
      if (rates.UYU) UYU = Math.round(rates.UYU);
      if (rates.CLP) CLP = Math.round(rates.CLP);
    }

    return res.json({
      base: 'USD',
      rates: { ARS, UYU, CLP },
      updated_at: new Date().toISOString(),
    });
  } catch (e) {
    // Fallback con valores aproximados si las APIs fallan
    return res.json({
      base: 'USD',
      rates: { ARS: 1050, UYU: 39, CLP: 970 },
      updated_at: new Date().toISOString(),
      fallback: true,
    });
  }
}
