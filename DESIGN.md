# Diseño

## Idea

**La luz del tablero.** El técnico de PDR lee las líneas de un panel LED reflejadas en la chapa: donde hay golpe se doblan; cuando vuelven a quedar rectas, el trabajo está hecho. La portada dibuja eso en un `<canvas>`: el golpe aparece y las líneas se enderezan, en bucle. Con `prefers-reduced-motion` queda el panel quieto y recto.

El sitio es oscuro a propósito, un solo tema: es el taller de noche, donde mejor se lee la luz.

## Color

| Token | Valor | Uso |
|---|---|---|
| `--grafito` | `#14171B` | Fondo. La penumbra del taller. |
| `--grafito-2` | `#0E1013` | Portada y formulario. |
| `--acero` / `--acero-2` | `#343B44` / `#252B32` | Superficies, bandas, bordes. El metal desnudo. |
| `--niebla` | `#98A2AD` | Texto secundario y etiquetas. |
| `--texto` | `#C9D0D7` | Texto corrido. |
| `--led` | `#F3F6F8` | Titulares y líneas de luz. El único brillo fuerte. |
| `--celeste` | `#7CC4EC` | Acento único: cotizar y WhatsApp. Cerca del 3 % de la página. |

## Tipografía

| Rol | Familia | Por qué |
|---|---|---|
| Titulares | Barlow Condensed 600/700 | Nace de la señalética vial; habla el idioma del auto sin caer en lo "racing". Condensada: un titular fuerte cabe en el ancho de un teléfono. |
| Texto | Atkinson Hyperlegible 400/700 | Diseñada para máxima legibilidad: se lee al sol, en el teléfono, junto al auto golpeado. Buenos acentos y eñes. |
| Datos y etiquetas | IBM Plex Mono 400 | Medidas, zonas, etiquetas. Aire de instrumento; cifras de ancho fijo. |

## Reglas

- **Corte a 14°** en los botones, por `clip-path` (desplazamiento = alto × 0,25).
- **Movimiento:** seguidor exponencial `1 - e^(-dt·RATE)` con `RATE = 6`. Nunca un listener de `scroll` para animar; la portada se pausa fuera de pantalla con `IntersectionObserver`.
- **Sin raya larga** en ningún texto público.
- Tokens en `assets/css/style.css`. Un color nuevo entra primero aquí.
