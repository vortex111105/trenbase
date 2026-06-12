// /api/store-sync.js — Proxy seguro a Shopify REST API y TiendaNube REST API
// El cliente NUNCA llama a las tiendas directamente (CORS + token expuesto).
// Este endpoint actúa de intermediario: recibe credenciales en el body,
// las usa server-side y devuelve data normalizada.
//
// POST /api/store-sync
// Body: { platform, credentials, action }
//
// platform: 'shopify' | 'tiendanube'
// credentials:
//   shopify:     { domain: 'mitienda.myshopify.com', token: 'shpat_...' }
//   tiendanube:  { userId: '123456', token: 'abc123...' }
// action: 'test' | 'sync'
//   test  → valida credenciales, devuelve { ok, storeName }
//   sync  → devuelve { orders: [...], products: [...], lastOrderId }

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

async function shopifyFetch(domain, token, path) {
  const url = `https://${domain}/admin/api/2024-01/${path}`;
  const res = await fetch(url, {
    headers: {
      'X-Shopify-Access-Token': token,
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Shopify ${res.status}: ${err.slice(0, 200)}`);
  }
  return res.json();
}

async function testShopify(domain, token) {
  const data = await shopifyFetch(domain, token, 'shop.json');
  return { ok: true, storeName: data.shop?.name || domain };
}

async function syncShopify(domain, token, sinceId) {
  // Orders: last 50 since sinceId (or all recent)
  const orderPath = sinceId
    ? `orders.json?status=any&limit=50&since_id=${sinceId}&fields=id,created_at,total_price,line_items`
    : `orders.json?status=any&limit=50&fields=id,created_at,total_price,line_items`;

  const [ordersData, productsData] = await Promise.all([
    shopifyFetch(domain, token, orderPath),
    shopifyFetch(domain, token, 'products.json?limit=250&fields=id,title,variants,status'),
  ]);

  const orders = (ordersData.products || ordersData.orders || []).map(o => ({
    id: String(o.id),
    created_at: o.created_at,
    total: parseFloat(o.total_price || 0),
    items: (o.line_items || []).map(li => ({
      name: li.title,
      qty: li.quantity,
      price: parseFloat(li.price),
    })),
  }));

  const products = (productsData.products || []).map(p => ({
    id: String(p.id),
    name: p.title,
    stock: (p.variants || []).reduce((sum, v) => sum + (v.inventory_quantity || 0), 0),
    variants: (p.variants || []).map(v => ({
      id: String(v.id),
      title: v.title,
      stock: v.inventory_quantity || 0,
      price: parseFloat(v.price || 0),
    })),
  }));

  const lastOrderId = orders.length ? orders[orders.length - 1].id : sinceId;
  return { orders, products, lastOrderId };
}

// ── TIENDANUBE ────────────────────────────────────────────────────────────────

async function tiendanubeFetch(userId, token, path) {
  const url = `https://api.tiendanube.com/v1/${userId}/${path}`;
  const res = await fetch(url, {
    headers: {
      Authentication: `bearer ${token}`,
      'User-Agent': 'TrendBase/1.0 (hola@trendbase.app)',
      'Content-Type': 'application/json',
    },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`TiendaNube ${res.status}: ${err.slice(0, 200)}`);
  }
  return res.json();
}

async function testTiendaNube(userId, token) {
  const data = await tiendanubeFetch(userId, token, '');
  return { ok: true, storeName: data.name?.es || data.name?.pt || `TiendaNube #${userId}` };
}

async function syncTiendaNube(userId, token, sinceId) {
  const orderPath = sinceId
    ? `orders?per_page=50&since_id=${sinceId}`
    : `orders?per_page=50`;

  const [orders, products] = await Promise.all([
    tiendanubeFetch(userId, token, orderPath),
    tiendanubeFetch(userId, token, 'products?per_page=250&fields=id,name,variants'),
  ]);

  const normalizedOrders = (Array.isArray(orders) ? orders : []).map(o => ({
    id: String(o.id),
    created_at: o.created_at,
    total: parseFloat(o.total || 0),
    items: (o.products || []).map(li => ({
      name: li.name?.es || li.name?.pt || '',
      qty: li.quantity,
      price: parseFloat(li.price || 0),
    })),
  }));

  const normalizedProducts = (Array.isArray(products) ? products : []).map(p => ({
    id: String(p.id),
    name: p.name?.es || p.name?.pt || '',
    stock: (p.variants || []).reduce((sum, v) => sum + (v.stock || 0), 0),
    variants: (p.variants || []).map(v => ({
      id: String(v.id),
      title: v.values?.map(val => val.es || val.pt || '').join(' / ') || '',
      stock: v.stock || 0,
      price: parseFloat(v.price || 0),
    })),
  }));

  const lastOrderId = normalizedOrders.length
    ? normalizedOrders[normalizedOrders.length - 1].id
    : sinceId;

  return { orders: normalizedOrders, products: normalizedProducts, lastOrderId };
}

// ── HANDLER ───────────────────────────────────────────────────────────────────

export default async function handler(req) {
  if (req.method === 'OPTIONS') return new Response(null, { headers: CORS });
  if (req.method !== 'POST') return json({ error: 'Method not allowed' }, 405);

  let body;
  try { body = await req.json(); } catch {
    return json({ error: 'Invalid JSON' }, 400);
  }

  const { platform, credentials = {}, action = 'test', sinceId } = body;

  if (!platform || !['shopify', 'tiendanube'].includes(platform))
    return json({ error: 'platform debe ser "shopify" o "tiendanube"' }, 400);

  if (!credentials)
    return json({ error: 'Faltan credenciales' }, 400);

  try {
    if (platform === 'shopify') {
      const { domain, token } = credentials;
      if (!domain || !token) return json({ error: 'Shopify requiere domain y token' }, 400);

      // Normalize domain
      const cleanDomain = domain
        .replace(/^https?:\/\//, '')
        .replace(/\/.*$/, '')
        .trim();

      if (action === 'test') {
        const result = await testShopify(cleanDomain, token);
        return json(result);
      }
      if (action === 'sync') {
        const result = await syncShopify(cleanDomain, token, sinceId);
        return json(result);
      }
    }

    if (platform === 'tiendanube') {
      const { userId, token } = credentials;
      if (!userId || !token) return json({ error: 'TiendaNube requiere userId y token' }, 400);

      if (action === 'test') {
        const result = await testTiendaNube(userId, token);
        return json(result);
      }
      if (action === 'sync') {
        const result = await syncTiendaNube(userId, token, sinceId);
        return json(result);
      }
    }

    return json({ error: 'action inválido' }, 400);
  } catch (err) {
    // Friendly error messages
    const msg = err.message || 'Error al conectar con la tienda';
    const isAuth = msg.includes('401') || msg.includes('403');
    return json({
      error: isAuth
        ? 'Credenciales inválidas. Verificá el token y el dominio.'
        : `No se pudo conectar: ${msg}`,
    }, isAuth ? 401 : 500);
  }
}
