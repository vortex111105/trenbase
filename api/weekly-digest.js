// /api/weekly-digest.js — Email semanal con los 5 mejores productos trending
// Corre los lunes a las 13:00 UTC (10:00 AR) via cron de Vercel
// Usa Resend.com para envío (free hasta 3k emails/mes)
//
// Pre-requisito: RESEND_API_KEY en las env vars de Vercel
// Dominio del remitente debe estar verificado en Resend (el de Hostinger)

const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY;
const RESEND_KEY = process.env.RESEND_API_KEY;
const FROM_EMAIL = process.env.DIGEST_FROM_EMAIL || 'TrendBase <alertas@trendbase.app>';
const CRON_SECRET = process.env.CRON_SECRET;

export default async function handler(req, res) {
  // Verificar que viene del cron de Vercel o llamada manual autorizada
  const auth = req.headers['authorization'] || req.query?.secret;
  const isVercelCron = req.headers['x-vercel-cron'] === '1';
  if(!isVercelCron && auth !== `Bearer ${CRON_SECRET}`) {
    return res.status(401).json({ error: 'No autorizado' });
  }

  if(!RESEND_KEY) {
    return res.status(500).json({ error: 'RESEND_API_KEY no configurada. Agregala en Vercel → Project Settings → Environment Variables.' });
  }

  try {
    // 1. Obtener top 5 productos por score
    const productsRes = await fetch(
      `${SUPABASE_URL}/rest/v1/products?select=name,cat,score,margin,comp,regions,img_kw&order=score.desc&limit=5`,
      { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
    );
    const products = await productsRes.json();

    // 2. Obtener todos los usuarios con email
    const usersRes = await fetch(
      `${SUPABASE_URL}/rest/v1/rpc/get_user_emails`,
      { method: 'POST', headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}`, 'Content-Type': 'application/json' }, body: '{}' }
    );
    let emails = [];
    if(usersRes.ok) {
      const userData = await usersRes.json();
      emails = (userData || []).map(u => u.email).filter(Boolean);
    }

    // Fallback: usar el email de admin si no hay usuarios
    if(!emails.length) {
      emails = [process.env.ADMIN_EMAIL || 'ifraga.ok@gmail.com'];
    }

    const weekStr = new Date().toLocaleDateString('es-AR', { day: 'numeric', month: 'long' });
    const htmlContent = buildDigestHtml(products || [], weekStr);

    // 3. Enviar emails en batches de 50
    let sent = 0, errors = 0;
    for(let i = 0; i < emails.length; i += 50) {
      const batch = emails.slice(i, i + 50);
      const result = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { Authorization: `Bearer ${RESEND_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: FROM_EMAIL,
          to: batch,
          subject: `🔥 Top 5 productos trending esta semana — ${weekStr}`,
          html: htmlContent,
        })
      });
      if(result.ok) sent += batch.length;
      else errors += batch.length;
    }

    return res.json({ ok: true, sent, errors, recipients: emails.length });

  } catch(e) {
    console.error('[weekly-digest]', e.message);
    return res.status(500).json({ error: e.message });
  }
}

function buildDigestHtml(products, weekStr) {
  const productRows = products.map((p, i) => {
    const medal = ['🥇','🥈','🥉','4️⃣','5️⃣'][i] || '';
    const compColor = { Baja: '#10b981', Media: '#f59e0b', Alta: '#ef4444' };
    const color = compColor[p.comp] || '#6b7280';
    return `
      <tr style="border-bottom:1px solid #f3f4f6;">
        <td style="padding:16px 8px;font-size:20px;width:40px;">${medal}</td>
        <td style="padding:16px 8px;">
          <div style="font-size:15px;font-weight:800;color:#111827;margin-bottom:4px;">${p.name}</div>
          <div style="font-size:11px;color:#6b7280;font-family:monospace;text-transform:uppercase;">${p.cat}</div>
        </td>
        <td style="padding:16px 8px;text-align:center;">
          <div style="font-size:24px;font-weight:900;color:#111827;">${p.score}</div>
          <div style="font-size:10px;color:#9ca3af;font-family:monospace;">SCORE</div>
        </td>
        <td style="padding:16px 8px;text-align:center;">
          <div style="font-size:16px;font-weight:700;color:#10b981;">${p.margin}%</div>
          <div style="font-size:10px;color:#9ca3af;font-family:monospace;">MARGEN</div>
        </td>
        <td style="padding:16px 8px;text-align:center;">
          <div style="font-size:12px;font-weight:700;color:${color};">${p.comp}</div>
          <div style="font-size:10px;color:#9ca3af;font-family:monospace;">COMP.</div>
        </td>
      </tr>`;
  }).join('');

  return `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f9fafb;margin:0;padding:0;">
  <div style="max-width:600px;margin:0 auto;padding:32px 16px;">
    <div style="background:#111827;border-radius:16px;padding:32px;text-align:center;margin-bottom:24px;">
      <div style="font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;">TrendBase</div>
      <div style="font-size:13px;color:#9ca3af;margin-top:4px;">Inteligencia de dropshipping para LATAM</div>
    </div>

    <div style="background:#fff;border-radius:16px;padding:24px;margin-bottom:24px;border:1px solid #e5e7eb;">
      <h2 style="font-size:20px;font-weight:800;color:#111827;margin:0 0 4px 0;">🔥 Top 5 productos de la semana</h2>
      <p style="font-size:13px;color:#6b7280;margin:0 0 20px 0;">Semana del ${weekStr} — Ordenados por TrendScore</p>
      <table style="width:100%;border-collapse:collapse;">
        <tbody>${productRows}</tbody>
      </table>
    </div>

    <div style="text-align:center;margin-bottom:24px;">
      <a href="https://trendbase.app/dashboard.html" style="display:inline-block;background:#111827;color:#fff;font-size:14px;font-weight:700;padding:14px 32px;border-radius:12px;text-decoration:none;">Ver todos los productos →</a>
    </div>

    <div style="text-align:center;font-size:11px;color:#9ca3af;padding-top:16px;border-top:1px solid #f3f4f6;">
      Recibís este email porque sos usuario de TrendBase.<br>
      <a href="https://trendbase.app" style="color:#6b7280;">trendbase.app</a>
    </div>
  </div>
</body>
</html>`;
}
