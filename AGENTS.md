# Cómo se trabaja en este repositorio

Nota de operación para cualquier persona o agente que abra este repositorio. Léela antes de tocar nada. Escrita el 12 de octubre de 2026.

## Quién trabaja aquí

El proyecto lo lleva Ernesto Cisneros ([index01.net](https://index01.net)) desde dos máquinas que nunca están en la misma sesión:

| Participante | Dónde | Qué hace |
|---|---|---|
| **Máquina 1** | Casa de Ernesto | Construye. |
| **Máquina 2** | Trabajo de Ernesto en UnlimitedWraps | Construye. |

Ernesto ve la misma conversación con el asistente desde todos sus dispositivos. Aun así, cada máquina corre su propia sesión de trabajo con su propia copia del repositorio.

## La regla que sostiene todo lo demás

**El repositorio es el registro común.** Lo que una sesión decidió, encontró o dejó a medias, si tiene que sobrevivir, va en un archivo de aquí y se empuja. Un hallazgo que se queda en una sesión o en la memoria local de una máquina está perdido para la otra.

## Antes de empezar y al terminar

**Antes:**

1. `git pull`. Puede haber commits de la otra máquina.
2. Lee `PRODUCT.md`: para quién es el sitio y sus principios de acción.
3. Lee `PENDIENTES.md`: lo que queda por hacer. Nada más.

**Al terminar:**

1. `python herramientas/generar.py` si cambiaste textos. Después, `python herramientas/comprobar.py`. No se cierra una tanda con fallos abiertos.
2. Borra de `PENDIENTES.md` lo que quedó hecho y añade lo que quedó abierto, con datos verificables (rutas, comandos), no con impresiones.
3. Commit con un mensaje que explique **por qué**, no solo qué.
4. Empuja. Un commit local no existe para la otra máquina.

## Cómo está hecho

- **Las páginas no se escriben a mano.** Todo el texto vive en `herramientas/sitio.json` y `herramientas/generar.py` escribe `index.html` (inglés, en la raíz) y `es/index.html` (español). El comprobador falla si una página no coincide con lo que produce el generador.
- **El comprobador** (`herramientas/comprobar.py`) corre en cada push con GitHub Actions. Cuando una revisión encuentre algo que el comprobador podría haber cazado, se arregla el fallo y se añade la regla en el mismo commit.
- **El dominio solo sirve el sitio.** `_config.yml` deja fuera de la publicación los documentos de la raíz y `herramientas/`. Un documento nuevo se añade a esa lista.

## Quién manda sobre qué

1. **La voluntad del cliente**, por encima de cualquier criterio técnico o de diseño.
2. **`PRODUCT.md`**: para quién es el sitio y qué tiene que conseguir.
3. **`DESIGN.md`**: cómo se ve y por qué. Los tokens son vinculantes.
4. **`PENDIENTES.md`**: qué falta y en qué orden.

Si un documento contradice al código, el código gana y el documento se corrige en el mismo commit.

## Innegociables

- **Sin raya larga** en ningún texto público. En español, tampoco la construcción ", y": se resuelve con punto o reestructurando. El comprobador vigila las dos.
- **Nada inventado.** Ni años de experiencia, ni reseñas, ni certificaciones, ni fotos de stock. Lo que no viene del cliente no se publica.
- **`noindex` hasta lanzar.** `"lanzado": false` en `sitio.json` mientras el sitio esté en construcción. Solo se cambia al pasar la checklist de lanzamiento del estudio. El comprobador no deja lanzar sin WhatsApp, dominio y nombre de marca confirmado.
- **Este repositorio es público.** Precios, acuerdos, datos personales del cliente y cualquier estrategia comercial interna no se escriben aquí. Viven en la documentación privada del estudio.
- **Una cifra se publica con la fecha y las condiciones en que se midió, o no se publica.**

## Cada máquina

Python 3 sin dependencias externas. La identidad de git se configura por repositorio (`git config --local`), nunca global. `.gitattributes` fija LF para que una regeneración en Windows no marque archivos como modificados sin cambios.
