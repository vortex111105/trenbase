# Lista de Tareas para Mañana 🚀

Esta es la hoja de ruta para continuar con el desarrollo de TrendBase en nuestra próxima sesión:

## 1. Conexión de APIs y Scrapers (Python -> Supabase)
- [ ] Mover los scripts `google_trends.py` y `tiktok_scraper.py` a un entorno de ejecución (como un worker).
- [ ] Configurar un "Cron Job" para que ejecuten las búsquedas diariamente.
- [ ] Conectar los resultados de Python para que actualicen automáticamente la base de datos de Supabase (`history`, `saturation`, `views`, etc.).
- [ ] Probar el pipeline completo (Python extrae -> Vercel/Supabase recibe -> Frontend muestra).

## 2. Sistema de Afiliados (Affiliates)
- [ ] Revisar y configurar la lógica de enlaces de afiliados para los proveedores VIP (AliExpress, Dropi, Dropdeal, etc.).
- [ ] Asegurarnos de que los parámetros de afiliado (ej. `?ref=trendbase`) se añadan dinámicamente en cada botón de "Ver link" o "Vender este producto".
- [ ] (Si aplica) Configurar un dashboard o webhook para rastrear conversiones o clicks salientes.

## 3. Pruebas Finales de Datos
- [ ] Asegurarnos de que cuando la base de datos se actualice de noche, el dashboard del usuario lo refleje de inmediato por la mañana sin retrasos ni cachés agresivos.
- [ ] Validar que la interfaz no colapse si un scraper falla y envía un "0" o "N/A".
