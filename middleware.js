export const config = {
  matcher: '/api/:path*',
};

export default function middleware(request) {
  const userAgent = request.headers.get('user-agent') || '';
  const origin = request.headers.get('origin') || '';
  const url = request.url;

  // Bloqueo de bots y scrapers
  const botPatterns = [
    /curl/i, /python-requests/i, /postmanruntime/i, /scrapy/i,
    /wget/i, /headless/i, /puppeteer/i, /playwright/i,
    /insomnia/i, /spider/i, /crawler/i
  ];

  for (const pattern of botPatterns) {
    if (pattern.test(userAgent)) {
      return new Response(
        JSON.stringify({ error: 'Acceso denegado: bot bloqueado.' }),
        { status: 403, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }

  // Validación de CORS para rutas API
  const allowedOrigins = [
    'https://www.trendbase.app',
    'https://trendbase.app',
    'https://trenbase.vercel.app',
    'https://www.trenbase.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:5500',
    'http://localhost:5500'
  ];

  if (url.includes('/api/')) {
    if (origin && !allowedOrigins.includes(origin) && !origin.endsWith('.vercel.app')) {
      return new Response(
        JSON.stringify({ error: 'CORS: Origin no autorizado.' }),
        { status: 403, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }

  return undefined;
}
