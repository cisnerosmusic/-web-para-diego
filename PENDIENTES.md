# Pendientes

Lo que queda por hacer. Nada más. Lo hecho vive en el historial de git. Cuando algo se termina, se borra de aquí en el mismo commit que lo cierra.

## 1. Espera las respuestas del cliente

Bloquean el lanzamiento. Cada una cambia `herramientas/sitio.json` y se regenera.

1. **Nombre de la marca.** "DR-USA" es provisional: confirmar el nombre exacto de la LLC y si la marca es ese nombre o el suyo. Al confirmarlo, `"marca_confirmada": true`.
2. **WhatsApp de trabajo.** Va en `"whatsapp"` (solo dígitos, con código de país). Sin él, el formulario avisa que el número no está configurado.
3. **Dominio.** ¿Existe? ¿Quién es el titular? Va en `"dominio"`; después: `CNAME`, URLs absolutas en hreflang, `sitemap.xml` y `llms.txt`.
4. **Zona de servicio.** Hoy dice "Miami, FL". Ciudades o condados exactos.
5. **Fotos antes/después** con el protocolo de `PRODUCT.md`, para la galería (fase 2).
6. **Logo.** Si existe, en vector.
7. **Política de bots de IA** para `robots.txt`.

## 2. Para lanzar

1. Pasar la checklist de lanzamiento del estudio.
2. Lighthouse móvil con 95 o más de rendimiento, medido y anotado con fecha.
3. Probar el formulario de punta a punta en un teléfono real, en los dos idiomas.
4. `"lanzado": true` y regenerar.
