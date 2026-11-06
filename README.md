# Posters ISPOR Europe 2026 — Aditum Consulting Group

Micrositio que sirve los dos posters vía QR impreso en cada poster.

## URLs definitivas

| Qué | URL | QR |
|---|---|---|
| Hub (los dos posters) | `https://christianpichardo.github.io/ispor2026/` | `qr/hub` |
| Poster 1 | `https://christianpichardo.github.io/ispor2026/1` | `qr/poster-1` |
| Poster 2 | `https://christianpichardo.github.io/ispor2026/2` | `qr/poster-2` |

Las rutas `/1` y `/2` son deliberadamente neutras y no describen el contenido:
así el QR impreso sigue sirviendo aunque cambie el título, el código ISPOR
o el PDF.

## Estructura

```
index.html        hub con los dos posters
1/index.html      landing del poster 1
2/index.html      landing del poster 2
assets/style.css  estilos (sin fuentes web: el wifi del congreso es malo)
pdf/              los PDF que se descargan
qr/               QR en PNG (impresión) y SVG (vectorial para el diseño)
qr/make_qr.py     regenera los QR
.nojekyll         GitHub Pages sirve los archivos tal cual
```

## Regenerar los QR

```bash
python qr/make_qr.py
```

## Especificaciones de impresión del QR

- Tamaño mínimo impreso: **4 cm** de lado (regla: distancia de escaneo ÷ 10).
- Corrección de error **Q (25%)**: tolera dobleces y reflejos del plotter.
- Quiet zone de 4 módulos (ya incluida en los archivos). No recortarla.
- Oscuro sobre claro. Nunca invertido.
- La URL visible en texto debajo del QR, como plan B.
- Colocar a 140–160 cm del piso.
- Probar el **impreso** con tres teléfonos, uno Android viejo.

## Pendientes

- [ ] Poner los dos PDF en `pdf/` como `poster-1.pdf` y `poster-2.pdf`
- [ ] Llenar título, autores, hallazgos y referencias en `1/` y `2/`
- [ ] Códigos de poster ISPOR
- [ ] Datos de `contacto.vcf` (correo institucional, no personal)
- [ ] Decidir si se quita `noindex` para que Google indexe los posters
