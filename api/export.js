export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { platform, url, token, product } = req.body;

  if (!platform || !url || !token || !product) {
    return res.status(400).json({ error: 'Faltan credenciales o datos del producto' });
  }

  try {
    if (platform === 'shopify') {
      const cleanUrl = url.replace(/^https?:\/\//, '').replace(/\/$/, '');
      const apiUrl = `https://${cleanUrl}/admin/api/2024-01/products.json`;

      const shopifyPayload = {
        product: {
          title: product.name,
          body_html: `<strong>¡Producto Tendencia!</strong><br><br>${product.description || ''}`,
          vendor: "TrendBase Dropshipping",
          product_type: product.cat || "General",
          tags: "trendbase, dropshipping",
          variants: [
            {
              price: product.price ? product.price.toString() : "0.00",
              requires_shipping: true
            }
          ],
          images: product.img ? [{ src: product.img }] : []
        }
      };

      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Shopify-Access-Token': token
        },
        body: JSON.stringify(shopifyPayload)
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.errors ? JSON.stringify(data.errors) : 'Error al conectar con Shopify');
      }

      return res.status(200).json({ success: true, message: 'Producto exportado a Shopify', data });
      
    } else if (platform === 'tiendanube') {
      // TiendaNube requires store_id, often extracted from the token or provided. 
      // This is a simplified best-effort implementation for TiendaNube API.
      // Usually format: Authentication: bearer {token}
      const userAgent = "TrendBase (contacto@trendbase.app)";
      
      return res.status(400).json({ 
        error: 'La integración con TiendaNube requiere de una App Partner oficial. Por ahora usa la integración de Shopify o descarga el CSV (ahora eliminado).' 
      });
    }

    return res.status(400).json({ error: 'Plataforma no soportada' });

  } catch (error) {
    console.error('[/api/export]', error.message);
    return res.status(500).json({ error: error.message });
  }
}
