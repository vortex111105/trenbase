export const config = { runtime: 'edge' };

const PRICE_IDS = {
  starter: 'pri_01kvxv1dmsz2329sdcz0dk687v',
  pro: 'pri_01kvxv3kpba8vgcxp52s5z1tz9',
};

export default async function handler(req) {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST', 'Access-Control-Allow-Headers': 'Content-Type' } });
  }
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
  }

  const { plan, email } = body;
  const priceId = PRICE_IDS[plan];
  if (!priceId) return new Response(JSON.stringify({ error: 'Invalid plan' }), { status: 400 });

  try {
    const payload = {
      items: [{ price_id: priceId, quantity: 1 }],
      checkout: { url: 'https://www.trendbase.app/dashboard?subscribed=1' },
    };
    if (email) payload.customer = { email };

    const res = await fetch('https://api.paddle.com/transactions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.PADDLE_API_KEY}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok) return new Response(JSON.stringify({ error: data }), { status: res.status });

    const checkoutUrl = data.data?.checkout?.url;
    return new Response(JSON.stringify({ url: checkoutUrl }), {
      status: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
