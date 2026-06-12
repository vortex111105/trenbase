import { NextResponse } from '@vercel/edge';

export const config = {
  matcher: '/api/:path*',
};

export default function middleware(request) {
  const userAgent = request.headers.get('user-agent') || '';
  const origin = request.headers.get('origin') || '';
  const url = request.url;

  // 1. Bloqueo de Bots y Scrapers comunes
  const botPatterns = [
    /curl/i,
    /python-requests/i,
    /postmanruntime/i,
    /scrapy/i,
    /wget/i,
    /headless/i,
    /puppeteer/i,
    /playwright/i,
    /insomnia/i,
    /spider/i,
    /crawler/i
  ];

  for (const pattern of botPatterns) {
    if (pattern.test(userAgent)) {
      return new NextResponse(
        JSON.stringify({ error: 'Acceso denegado: Herramienta automatizada o bot bloqueado por política de seguridad.' }),
        { status: 403, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }

  // 2. Validación de CORS y Origin para rutas API
  // Protege los endpoints de IA y Base de datos para que solo TrendBase pueda usarlos.
  const allowedOrigins = [
    'https://trenbase.vercel.app',
    'https://www.trenbase.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:5500',
    'http://localhost:5500' // Entornos locales
  ];

  if (url.includes('/api/')) {
    // Permitir el cron job de Vercel a generate.js
    if (url.includes('/api/generate') && request.headers.get('x-cron-secret')) {
      return NextResponse.next();
    }

    // Validar el origen si existe
    if (origin && !allowedOrigins.includes(origin)) {
      // Permitir previsualizaciones automáticas de Vercel (*.vercel.app)
      if (!origin.endsWith('.vercel.app')) {
        return new NextResponse(
          JSON.stringify({ error: 'CORS policy violation: Origin no autorizado.' }),
          { status: 403, headers: { 'Content-Type': 'application/json' } }
        );
      }
    }

    // Evitar cross-site scripting básico desde el navegador (Fetch)
    const secFetchSite = request.headers.get('sec-fetch-site');
    if (secFetchSite === 'cross-site') {
      return new NextResponse(
        JSON.stringify({ error: 'CORS policy violation: Cross-site requests están bloqueados.' }),
        { status: 403, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }

  return NextResponse.next();
}
