# Arquitectura de Datos de TrendBase

Para eliminar por completo los "mocks" y conectar los datos reales de Google Trends y TikTok, sigue esta arquitectura:

## 1. El Problema de Vercel (Serverless)
El archivo `/api/generate.js` corre en Vercel. Vercel Serverless Functions están diseñadas para ejecutar Node.js de forma rápida (máx 10 segundos). 
Ejecutar scrapers de Python (`google_trends.py`, `tiktok_scraper.py`) requiere más tiempo y un entorno diferente.

## 2. Solución: Microservicio de Scraping (Worker)
Debes alojar los scripts de Python en una plataforma diseñada para workers o contenedores, como:
- **Render.com** (Background Worker)
- **Railway.app** 
- **DigitalOcean Droplet**

### Flujo de Trabajo (Cron Job diario):
1. El script de Python consulta todos los productos de Supabase que no se han actualizado hoy.
2. Para cada producto, extrae su término clave (`p.name`).
3. Llama a `google_trends.py` para obtener su historial de búsquedas (`history`).
4. Llama a `tiktok_scraper.py` (o Apify API) para obtener sus anuncios top (`p.ads.views`).
5. Calcula el puntaje de saturación basado en las tiendas en Shopify (usando StoreLeads API) y lo guarda en `p.saturation` y `p.storeCount`.
6. Actualiza la fila del producto en Supabase.

## 3. Cambios en el Frontend (Ya implementados)
El archivo `index.html` ya ha sido modificado para dejar de "inventar" estos números con `Math.random()`. 
Ahora lee directamente:
- `p.saturation`
- `p.storeCount`
- `p.ads[0].views`

Si estos datos no existen en la base de datos (porque el worker de Python aún no los ha llenado), la plataforma mostrará "0" o "N/A", obligando a que los datos provengan de una fuente verídica.
