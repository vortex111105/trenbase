// /api/push-product.js — Crea un producto en Shopify o TiendaNube desde TrendBase
// El cliente envía las credenciales + datos del producto; el servidor hace la llamada
// para evitar exponer tokens en el frontend.
//
// POST /api/push-product
// Body: { platform, credentials, product }
//   platform: 'shopify' | 'tiendanube'
//   credentials (shopify):    { domain, token }
//   credentials (tiendanube): { userId, token }
//   product: { name, description, price_local, currency, image_url, cost_usd, margin }

export const config = { runtime: 'edge' };

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

// ── SHOPIFY ───────────────────────────────────────────────────────────────────

async function pushToShopify(domain, token, product) {
  const url = `https://${domain}/admin/api/2024-01/products.json`;

  const body = {
    product: {
      title: product.name,
      body_html: product.description || `<p>Producto trending detectado por TrendBase. Categoría: ${product.cat || ''}. Margen estimado: ${product.margin || 0}%.</p>`,
      vendor: 'TrendBase',
      product_type: product.cat || 'Dropshipping',
      tags: ['trendbase', 'dropshipping', product.cat || ''].filter(Boolean).join(','),
      images: product.image_url ? [{ src: product.image_url }] : [],
      variants: [{
        price: String(product.price_local || 0),
        inventory_management: 'shopify',
        inventory_quantity: 10,
        fulfillment_service: 'manual',
        requires_shipping: true,
      }],
    },
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'X-Shopify-Access-Token': token,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Shopify ${res.status}: ${err.slice(0, 300)}`);
  }

  const data = await res.json();
  const productId = data.product?.id;
  const adminUrl = `https://${domain}/admin/products/${productId}`;
  const storeUrl = `https://${domain.replace('.myshopify.com', '')}.myshopify.com/products/${data.product?.handle}`;

  return { ok: true, product_id: String(productId), admin_url: adminUrl, store_url: storeUrl };
}

// ── TIENDANUBE ────────────────────────────────────────────────────────────────

async function pushToTiendaNube(userId, token, product) {
  const url = `https://api.tiendanube.com/v1/${userId}/products`;

  const body = {
    name: { es: product.name },
    description: { es: product.description || `Producto trending detectado por TrendBase. Margen estimado: ${product.margin || 0}%.` },
    variants: [{
      price: String(product.price_local || 0),
      stock: 10,
    }],
    images: product.image_url ? [{ src: product.image_url }] : [],
    categories: [],
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      Authentication: `bearer ${token}`,
      'User-Agent': 'TrendBase/1.0 (hola@trendbase.app)',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`TiendaNube ${res.status}: ${err.slice(0, 300)}`);
  }

  const data = await res.json();
  const productId = data.id;

  return {
    ok: true,
    product_id: String(productId),
    admin_url: `https://www.tiendanube.com/tiendas/${userId}/admin/products/${productId}`,
    store_url: data.permalink || null,
  };
}

// ── HANDLER ───────────────────────────────────────────────────────────────────

export default async function handler(req) {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  let body;
  try { body = await req.json(); } catch {
    return json({ error: 'JSON inválido' }, 400);
  }

  const { platform, credentials, product } = body;

  if (!platform || !credentials || !product?.name) {
    return json({ error: 'Faltan campos: platform, credentials, product.name' }, 400);
  }

  try {
    if (platform === 'shopify') {
      const { domain, token } = credentials;
      if (!domain || !token) return json({ error: 'Credenciales Shopify incompletas (domain, token)' }, 400);
      const result = await pushToShopify(domain, token, product);
      return json(result);
    }

    if (platform === 'tiendanube') {
      const { userId, token } = credentials;
      if (!userId || !token) return json({ error: 'Credenciales TiendaNube incompletas (userId, token)' }, 400);
      const result = await pushToTiendaNube(userId, token, product);
      return json(result);
    }

    return json({ error: `Plataforma no soportada: ${platform}` }, 400);

  } catch (e) {
    console.error('[push-product]', e.message);
    return json({ error: e.message }, 500);
  }
}
