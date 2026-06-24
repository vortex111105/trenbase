export const config = { runtime: 'edge' };

const PLAN_BY_PRICE = {
  'pri_01kvxv1dmsz2329sdcz0dk687v': 'starter',
  'pri_01kvxv3kpba8vgcxp52s5z1tz9': 'pro',
};

async function verifySignature(req, rawBody) {
  const signature = req.headers.get('Paddle-Signature');
  const secret = process.env.PADDLE_WEBHOOK_SECRET;
  if (!secret) return true;
  if (!signature) return false;

  const parts = Object.fromEntries(
    signature.split(';').map(p => { const [k, ...v] = p.split('='); return [k, v.join('=')]; })
  );
  const { ts, h1 } = parts;

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sigBytes = await crypto.subtle.sign('HMAC', key, encoder.encode(`${ts}:${rawBody}`));
  const computed = Array.from(new Uint8Array(sigBytes)).map(b => b.toString(16).padStart(2, '0')).join('');

  return computed === h1;
}

async function updateUserPlan(email, plan, subscriptionId) {
  const supabaseUrl = process.env.SUPABASE_URL;
  const serviceKey = process.env.SUPABASE_SERVICE_KEY;

  // Find user by email
  const searchRes = await fetch(`${supabaseUrl}/auth/v1/admin/users?email=${encodeURIComponent(email)}&page=1&per_page=1`, {
    headers: { 'apikey': serviceKey, 'Authorization': `Bearer ${serviceKey}` },
  });
  if (!searchRes.ok) return;

  const { users } = await searchRes.json();
  const user = users?.[0];
  if (!user) return;

  // Update app_metadata so JWT reflects the new plan on next refresh
  await fetch(`${supabaseUrl}/auth/v1/admin/users/${user.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', 'apikey': serviceKey, 'Authorization': `Bearer ${serviceKey}` },
    body: JSON.stringify({ app_metadata: { plan, paddle_subscription_id: subscriptionId || null } }),
  });
}

export default async function handler(req) {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 });

  const rawBody = await req.text();

  const valid = await verifySignature(req, rawBody);
  if (!valid) return new Response('Invalid signature', { status: 401 });

  let event;
  try { event = JSON.parse(rawBody); } catch { return new Response('Invalid JSON', { status: 400 }); }

  const { event_type, data } = event;

  if (event_type === 'subscription.activated' || event_type === 'subscription.updated') {
    const email = data.customer?.email;
    const priceId = data.items?.[0]?.price?.id;
    const plan = PLAN_BY_PRICE[priceId] || 'starter';
    if (email) await updateUserPlan(email, plan, data.id);
  }

  if (event_type === 'subscription.canceled' || event_type === 'subscription.past_due') {
    const email = data.customer?.email;
    if (email) await updateUserPlan(email, 'free', null);
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}
