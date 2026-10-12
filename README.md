# DR-USA

[![Comprobar el sitio](https://github.com/cisnerosmusic/-web-para-diego/actions/workflows/comprobar.yml/badge.svg)](https://github.com/cisnerosmusic/-web-para-diego/actions/workflows/comprobar.yml)

Sitio de DR-USA (nombre provisional): reparación de abolladuras sin pintura en Miami, en el taller o en la casa del cliente. Desarrollo de [index01.net](https://index01.net).

**Estado:** en construcción, con `noindex`. Ver [PENDIENTES.md](PENDIENTES.md).

## Cómo está hecho

HTML, CSS y JS propios, sin frameworks. Las páginas se generan desde datos:

```bash
python herramientas/generar.py     # escribe index.html y es/index.html desde sitio.json
python herramientas/comprobar.py   # reglas del sitio; corre también en cada push
```

## Estructura

| Ruta | Contenido |
|---|---|
| `index.html` | Portada en inglés (generada) |
| `es/index.html` | Portada en español (generada) |
| `assets/` | CSS, JS y favicon |
| `herramientas/sitio.json` | Todo el texto del sitio, en los dos idiomas |
| `herramientas/generar.py` | El generador |
| `herramientas/comprobar.py` | El comprobador |

## Documentos de trabajo

[AGENTS.md](AGENTS.md) (cómo se trabaja) · [PRODUCT.md](PRODUCT.md) (para quién y principios de acción) · [DESIGN.md](DESIGN.md) (cómo se ve y por qué) · [PENDIENTES.md](PENDIENTES.md) (qué falta).
