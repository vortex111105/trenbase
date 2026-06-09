// /api/aliexpress.js — AliExpress Affiliate API
import crypto from 'crypto';

const APP_KEY = process.env.AE_APP_KEY;
const APP_SECRET = process.env.AE_APP_SECRET;
const TRACKING_ID = process.env.AE_TRACKING_ID || 'trendbase';

function generateSign(params, secret) {
  const sorted = Object.keys(params).sort();
  const str = secret + sorted.map(k => k + params[k]).join('') + secret;
  return crypto.createHash('md5').update(str).digest('hex').toUpperCase();
}

async function searchAE(keywords) {
  const method = 'aliexpress.affiliate.product.query';
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);

  const params = {
    app_key: APP_KEY,
    timestamp,
    sign_method: 'md5',
    method,
    v: '2.0',
    format: 'json',
    keywords,
    page_no: '1',
    page_size: '6',
    tracking_id: TRACKING_ID,
    fields: 'product_id,product_title,product_main_image_url,target_app_sale_price,target_original_price,evaluate_rate,hot_product_commission_rate,product_detail_url',
    sort: 'LAST_VOLUME_DESC',
    target_currency: 'USD',
    target_language: 'ES',
    ship_to_country: 'AR',
  };

  params.sign = generateSign(params, APP_SECRET);

  // Try the correct endpoint for Affiliates API
  const url = 'https://api-sg.aliexpress.com/sync';
  const body = new URLSearchParams(params);

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });

  const text = await res.text();
  console.log('AE raw response:', text.substring(0, 500));

  let data;
  try {
    data = JSON.parse(text);
  } catch(e) {
    throw new Error('AliExpress respondió XML/HTML: ' + text.substring(0, 300));
  }

  if (data.error_response) {
    throw new Error('AE API Error: ' + JSON.stringify(data.error_response));
  }

  const result = data?.aliexpress_affiliate_product_query_response?.resp_result;
  if (!result || result.resp_code !== 200) {
    throw new Error('AE error: ' + (result?.resp_msg || JSON.stringify(data).substring(0, 200)));
  }

  const products = result?.result?.products?.product || [];
  return products.map(p => ({
    id: p.product_id,
    title: p.product_title,
    image: p.product_main_image_url,
    price: p.target_app_sale_price || p.target_original_price,
    commission: p.hot_product_commission_rate,
    rating: p.evaluate_rate,
    url: p.product_detail_url,
  }));
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Content-Type', 'application/json');

  const q = req.query?.q;
  if (!q) return res.status(400).json({ error: 'Falta parámetro q' });
  if (!APP_KEY || !APP_SECRET) return res.status(500).json({ error: 'Credenciales no configuradas', key: !!APP_KEY, secret: !!APP_SECRET });

  try {
    const products = await searchAE(q);
    return res.json({ products, query: q });
  } catch(e) {
    console.error('[/api/aliexpress]', e.message);
    return res.status(500).json({ error: e.message });
  }
}
