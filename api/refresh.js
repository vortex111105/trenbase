// /api/refresh.js — Endpoint del cliente para triggerar generación de productos
// No expone el CRON_SECRET: llama internamente a /api/generate con el header correcto
const CRON_SECRET = process.env.CRON_SECRET;

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');

  if (!CRON_SECRET) {
    return res.status(500).json({ error: 'CRON_SECRET no configurado' });
  }

  const batchIndex = parseInt(req.query?.batch || '0');

  try {
    const baseUrl = process.env.VERCEL_URL
      ? `https://${process.env.VERCEL_URL}`
      : 'http://localhost:3000';

    const response = await fetch(
      `${baseUrl}/api/generate?batch=${batchIndex}`,
      {
        headers: {
          'x-cron-secret': CRON_SECRET,
          'Content-Type': 'application/json',
        },
      }
    );

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
