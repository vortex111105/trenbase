export const config = { runtime: 'edge' };

const SUPABASE_URL = 'https://rbrundkswmlbgkicdnty.supabase.co';
const SITE_URL = 'https://trenbase.vercel.app';

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405 });
  }

  let body;
  try { body = await req.json(); } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
  }

  const { action, email, password } = body;
  const key = process.env.SUPABASE_ANON_KEY;

  if (action === 'google') {
    const redirectTo = SITE_URL + '?auth=callback';
    const url = `${SUPABASE_URL}/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(redirectTo)}`;
    return new Response(JSON.stringify({ url }), {
      status: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }

  if (action === 'signup') {
    try {
      const res = await fetch(`${SUPABASE_URL}/auth/v1/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'apikey': key, 'Authorization': `Bearer ${key}` },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) return new Response(JSON.stringify({ error: data.error_description || data.msg || 'Error al registrarse' }), { status: res.status });
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }

  if (action === 'login') {
    try {
      const res = await fetch(`${SUPABASE_URL}/auth/v1/token?grant_type=password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'apikey': key, 'Authorization': `Bearer ${key}` },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) return new Response(JSON.stringify({ error: data.error_description || data.msg || 'Email o contraseña incorrectos' }), { status: res.status });
      return new Response(JSON.stringify({
        access_token: data.access_token,
        user: data.user,
        email,
      }), { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }

  return new Response(JSON.stringify({ error: 'Invalid action' }), { status: 400 });
}
