# Generador del sitio de DR-USA.
#
# Las paginas NO se escriben a mano (regla de la fabrica Index01): todo el texto
# vive en herramientas/sitio.json y este script escribe index.html (ingles, en la
# raiz) y es/index.html (espanol). Para cambiar un texto se edita el JSON y se
# vuelve a correr:
#
#   python herramientas/generar.py
#
# Mientras "lanzado" sea false, cada pagina sale con noindex. Se cambia a true
# solo al pasar la checklist de lanzamiento del estudio.

import json, os, sys, io
from html import escape

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIOMAS = ("en", "es")
VERSION_CSS = 1
VERSION_JS = 1


def e(texto):
    return escape(texto, quote=True)


def cargar():
    with open(os.path.join(RAIZ, "herramientas", "sitio.json"), encoding="utf-8") as f:
        return json.load(f)


def json_ld(d, t):
    datos = {
        "@context": "https://schema.org",
        "@type": "AutoRepair",
        "name": d["marca"],
        "description": t["descripcion"],
        "areaServed": d["zona"],
        "knowsLanguage": ["en", "es"],
        "inLanguage": "en" if t is d["en"] else "es",
    }
    if d["dominio"]:
        datos["url"] = "https://" + d["dominio"] + "/" + t["ruta"]
    return json.dumps(datos, ensure_ascii=False, indent=2)


def opciones_radio(nombre, respuestas):
    return "".join(
        f'<label><input type="radio" name="{nombre}" value="{e(r)}">{e(r)}</label>'
        for r in respuestas
    )


def pagina(d, lang):
    t = d[lang]
    base = "" if lang == "en" else "../"
    otro = "es" if lang == "en" else "en"
    ruta_otro = "es/" if lang == "en" else "../"
    robots = "" if d["lanzado"] else '<meta name="robots" content="noindex, nofollow">\n'
    c = t["cotizar"]

    puertas = "\n".join(
        f'      <a class="door" href="#{p["ancla"]}">\n'
        f'        <span class="label">{e(p["etiqueta"])}</span>\n'
        f'        <h3>{e(p["titulo"])} <span class="arrow" aria-hidden="true">→</span></h3>\n'
        f'        <p>{e(p["texto"])}</p>\n'
        f'      </a>'
        for p in t["puertas"]
    )
    pasos = "\n".join(
        f'        <li><h3>{e(p["titulo"])}</h3><p>{e(p["texto"])}</p></li>' for p in t["como"]["pasos"]
    )

    def puntos(lista):
        return "\n".join(
            f'        <li><b>{e(p["titulo"])}</b><span>{e(p["texto"])}</span></li>' for p in lista
        )

    limites = "\n".join(
        f'        <div class="limit"><b>{e(p["titulo"])}</b><span>{e(p["texto"])}</span></div>'
        for p in t["limites"]["items"]
    )
    soy = "".join(
        f'<option value="">{e(o)}</option>' if i == 0 else f'<option>{e(o)}</option>'
        for i, o in enumerate(c["soy_opciones"])
    )
    idioma_nav = (
        f'<span aria-current="true">EN</span><span aria-hidden="true">·</span><a href="es/" hreflang="es" lang="es">ES</a>'
        if lang == "en" else
        f'<a href="../" hreflang="en" lang="en">EN</a><span aria-hidden="true">·</span><span aria-current="true">ES</span>'
    )

    return f"""<!doctype html>
<!-- Generado por herramientas/generar.py desde herramientas/sitio.json. No editar a mano. -->
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t["titulo"])}</title>
<meta name="description" content="{e(t["descripcion"])}">
{robots}<link rel="alternate" hreflang="{lang}" href="./">
<link rel="alternate" hreflang="{otro}" href="{ruta_otro}">
<link rel="alternate" hreflang="x-default" href="{base}">
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&amp;family=Atkinson+Hyperlegible:wght@400;700&amp;family=IBM+Plex+Mono:wght@400&amp;display=swap">
<link rel="stylesheet" href="{base}assets/css/style.css?v={VERSION_CSS}">
</head>
<body data-whatsapp="{e(d["whatsapp"])}">
<a class="skip" href="#main">{e(t["saltar"])}</a>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./">{e(d["marca"])}<small>{e(t["lema"])}</small></a>
    <nav class="lang" aria-label="{e(t["nav_idioma"])}">{idioma_nav}</nav>
  </div>
</header>

<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <canvas id="hero-canvas" aria-hidden="true"></canvas>
    <div class="hero-copy">
      <div class="wrap">
        <span class="label">{e(t["hero"]["etiqueta"])}</span>
        <h1 id="hero-title">{e(t["hero"]["titulo"])}</h1>
        <p class="lead">{e(t["hero"]["entrada"])}</p>
        <div class="btns">
          <a class="btn btn-primary" href="#cotizar">{e(t["hero"]["boton_cotizar"])}</a>
          <a class="btn btn-ghost" href="#talleres">{e(t["hero"]["boton_taller"])}</a>
        </div>
      </div>
    </div>
  </section>

  <section class="doors" aria-label="{e(t["puertas_aria"])}">
    <div class="grid">
{puertas}
    </div>
  </section>

  <section aria-labelledby="como-title">
    <div class="wrap stack gap-lg">
      <div class="stack">
        <span class="label">{e(t["como"]["etiqueta"])}</span>
        <h2 id="como-title">{e(t["como"]["titulo"])}</h2>
      </div>
      <ol class="steps">
{pasos}
      </ol>
    </div>
  </section>

  <section class="band" id="talleres" aria-labelledby="talleres-title">
    <div class="wrap split">
      <div class="stack">
        <span class="label">{e(t["talleres"]["etiqueta"])}</span>
        <h2 id="talleres-title">{e(t["talleres"]["titulo"])}</h2>
        <p class="prose">{e(t["talleres"]["texto"])}</p>
        <div class="btns"><a class="btn btn-primary" href="#cotizar">{e(t["talleres"]["boton"])}</a></div>
      </div>
      <ul class="points">
{puntos(t["talleres"]["puntos"])}
      </ul>
    </div>
  </section>

  <section id="autos" aria-labelledby="autos-title">
    <div class="wrap split">
      <div class="stack">
        <span class="label">{e(t["autos"]["etiqueta"])}</span>
        <h2 id="autos-title">{e(t["autos"]["titulo"])}</h2>
        <p class="prose">{e(t["autos"]["texto"])}</p>
      </div>
      <ul class="points">
{puntos(t["autos"]["puntos"])}
      </ul>
    </div>
  </section>

  <section class="band" aria-labelledby="limites-title">
    <div class="wrap stack gap-lg">
      <div class="stack">
        <span class="label">{e(t["limites"]["etiqueta"])}</span>
        <h2 id="limites-title">{e(t["limites"]["titulo"])}</h2>
      </div>
      <div class="limits">
{limites}
      </div>
    </div>
  </section>

  <section class="quote" id="cotizar" aria-labelledby="cotizar-title">
    <div class="wrap stack gap-lg">
      <div class="stack">
        <span class="label">{e(c["etiqueta"])}</span>
        <h2 id="cotizar-title">{e(c["titulo"])}</h2>
        <p class="prose">{e(c["texto"])}</p>
      </div>
      <form id="quote-form" novalidate>
        <div class="field"><label for="q-name">{e(c["nombre"])}</label><input type="text" id="q-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="q-area">{e(c["zona"])}</label><input type="text" id="q-area" name="area" autocomplete="postal-code" required></div>
        <div class="field"><label for="q-vehicle">{e(c["vehiculo"])}</label><input type="text" id="q-vehicle" name="vehicle"></div>
        <div class="field"><label for="q-who">{e(c["soy"])}</label><select id="q-who" name="who">{soy}</select></div>
        <fieldset class="full"><legend>{e(c["borde"])}</legend><div class="choices">{opciones_radio("edge", c["respuestas"])}</div></fieldset>
        <fieldset><legend>{e(c["pintura"])}</legend><div class="choices">{opciones_radio("paint", c["respuestas"])}</div></fieldset>
        <fieldset><legend>{e(c["repintado"])}</legend><div class="choices">{opciones_radio("repaint", c["respuestas"])}</div></fieldset>
        <div class="field full"><label for="q-notes">{e(c["notas"])}</label><textarea id="q-notes" name="notes"></textarea></div>
        <p class="photo-note">{e(c["nota_fotos"])}</p>
        <div class="form-actions">
          <button class="btn btn-primary" type="submit">{e(c["enviar"])}</button>
          <span class="form-status" id="form-status" role="status"></span>
        </div>
      </form>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 {e(d["marca"])} · {e(d["zona"])}</span>
    <span>{e(t["pie_sitio"])} <a href="https://index01.net">index01.net</a></span>
  </div>
</footer>

<script type="application/ld+json">
{json_ld(d, t)}
</script>
<script src="{base}assets/js/main.js?v={VERSION_JS}" defer></script>
</body>
</html>
"""


def construir():
    """Devuelve {ruta relativa: html} sin escribir nada (lo usa el comprobador)."""
    d = cargar()
    return {
        "index.html": pagina(d, "en"),
        os.path.join("es", "index.html"): pagina(d, "es"),
    }


def main():
    for ruta, html in construir().items():
        destino = os.path.join(RAIZ, ruta)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print("escrito", ruta)


if __name__ == "__main__":
    main()
