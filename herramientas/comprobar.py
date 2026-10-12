# Comprobador del sitio de DR-USA. Se pasa antes de cerrar una tanda y corre
# solo en cada push (.github/workflows/comprobar.yml).
#
# Lo que una maquina puede comprobar sola no debe gastar la atencion de nadie.
# Cuando una revision encuentre algo que este script podria haber cazado, se
# arregla el fallo y se anade la regla en el mismo commit.
#
# Uso:  python herramientas/comprobar.py      (sale con codigo 1 si algo falla)

import glob, io, json, os, re, sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))
import generar  # noqa: E402

fallos = []


def falla(regla, detalle):
    fallos.append((regla, detalle))


def leer(ruta):
    with open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
        return f.read()


class Texto(HTMLParser):
    """Texto visible de una pagina, sin scripts ni estilos."""

    def __init__(self):
        super().__init__()
        self.partes, self._fuera = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._fuera += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._fuera -= 1

    def handle_data(self, data):
        if not self._fuera:
            self.partes.append(data)


def paginas():
    for p in sorted(glob.glob(os.path.join(RAIZ, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(p, RAIZ)
        if rel.startswith((".git", "herramientas")):
            continue
        yield rel


datos = generar.cargar()

# 1. Las paginas son lo que dice el generador: nadie las toco a mano.
for ruta, esperado in generar.construir().items():
    if not os.path.exists(os.path.join(RAIZ, ruta)):
        falla("generador", f"{ruta} no existe: corre python herramientas/generar.py")
    elif leer(ruta) != esperado:
        falla("generador", f"{ruta} no coincide con sitio.json: se edito a mano o falta regenerar")

for rel in paginas():
    html = leer(rel)
    lector = Texto()
    lector.feed(html)
    visible = " ".join(lector.partes)

    # 2. Sin raya larga en texto publico (regla universal del estudio).
    if "—" in html:
        falla("raya larga", rel)

    # 3. Sin la construccion ", y" en el texto espanol (regla de estilo de Ernesto).
    if 'lang="es"' in html and re.search(r",\s+y\s", visible):
        falla("coma y", f"{rel}: {re.search(r'.{0,40},\\s+y\\s.{0,20}', visible).group(0)!r}")

    # 4. noindex mientras el sitio no este lanzado, y nunca despues.
    tiene_noindex = 'name="robots" content="noindex' in html
    if not datos["lanzado"] and not tiene_noindex:
        falla("noindex", f"{rel}: el sitio no esta lanzado y la pagina es indexable")
    if datos["lanzado"] and tiene_noindex:
        falla("noindex", f"{rel}: el sitio esta lanzado y la pagina sigue con noindex")

    # 5. Enlaces y recursos locales que existen; anclas que existen.
    ids = set(re.findall(r'\sid="([^"]+)"', html))
    for url in re.findall(r'(?:href|src)="([^"]+)"', html):
        if url.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
            continue
        if url.startswith("#"):
            if url[1:] not in ids:
                falla("ancla", f"{rel}: {url} no existe")
            continue
        limpia = url.split("?")[0].split("#")[0]
        destino = os.path.normpath(os.path.join(RAIZ, os.path.dirname(rel), limpia))
        if limpia.endswith("/") or limpia in ("", "."):
            destino = os.path.join(destino, "index.html")
        if not os.path.exists(destino):
            falla("enlace roto", f"{rel}: {url}")

    # 6. JSON-LD que se puede leer.
    for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            json.loads(bloque)
        except ValueError as err:
            falla("json-ld", f"{rel}: {err}")

    # 7. target=_blank siempre con noopener.
    for etiqueta in re.findall(r"<a\s[^>]*>", html):
        if 'target="_blank"' in etiqueta and "noopener" not in etiqueta:
            falla("noopener", f"{rel}: {etiqueta}")

    # 8. Imagenes con alt.
    for etiqueta in re.findall(r"<img\s[^>]*>", html):
        if " alt=" not in etiqueta:
            falla("alt", f"{rel}: {etiqueta}")

    # 9. hreflang hacia los dos idiomas y x-default.
    for codigo in ("en", "es", "x-default"):
        if f'hreflang="{codigo}"' not in html:
            falla("hreflang", f"{rel}: falta {codigo}")

# 10. El dominio solo sirve el sitio: documentos y herramientas fuera de la publicacion.
config = leer("_config.yml") if os.path.exists(os.path.join(RAIZ, "_config.yml")) else ""
excluidos = set(re.findall(r"^\s*-\s*(\S+)", config, re.M))
for doc in glob.glob(os.path.join(RAIZ, "*.md")):
    if os.path.basename(doc) not in excluidos:
        falla("_config.yml", f"{os.path.basename(doc)} se publicaria en el dominio")
if "herramientas" not in excluidos:
    falla("_config.yml", "herramientas/ se publicaria en el dominio")

# 11. No se lanza con datos a medias.
if datos["lanzado"]:
    for campo in ("whatsapp", "dominio"):
        if not datos[campo]:
            falla("lanzamiento", f"falta '{campo}' en sitio.json")
    if not datos["marca_confirmada"]:
        falla("lanzamiento", "el nombre de la marca no esta confirmado por el cliente")

if fallos:
    for regla, detalle in fallos:
        print(f"FALLA  [{regla}] {detalle}")
    print(f"\n{len(fallos)} fallo(s).")
    sys.exit(1)
print("Todo en orden.")
