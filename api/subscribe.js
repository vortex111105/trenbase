export const config = { runtime: 'edge' };

const VARIANT_IDS = {
  starter: '1744638',
  pro: '1744624',
  business: '1744644',
};

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
  }

  const { plan, email } = body;
  const variantId = VARIANT_IDS[plan];
  if (!variantId) return new Response(JSON.stringify({ error: 'Invalid plan' }), { status: 400 });

  try {
    const res = await fetch('https://api.lemonsqueezy.com/v1/checkouts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': `Bearer ${process.env.LEMONSQUEEZY_API_KEY}`,
      },
      body: JSON.stringify({
        data: {
          type: 'checkouts',
          attributes: {
            checkout_data: { email: email || '' },
            product_options: {
              redirect_url: 'https://trenbase.vercel.app?subscribed=1',
              receipt_link_url: 'https://trenbase.vercel.app?subscribed=1',
            },
          },
          relationships: {
            store: { data: { type: 'stores', id: '397047' } },
            variant: { data: { type: 'variants', id: variantId } },
          },
        },
      }),
    });

    const data = await res.json();
    if (!res.ok) return new Response(JSON.stringify({ error: JSON.stringify(data) }), { status: res.status });
    const checkoutUrl = data.data?.attributes?.url;
    return new Response(JSON.stringify({ url: checkoutUrl }), {
      status: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
