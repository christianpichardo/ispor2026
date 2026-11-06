#!/usr/bin/env python3
"""Genera los QR de los posters ISPOR Europe 2026.

Produce, por cada destino:
  <slug>-navy.svg / <slug>-black.svg   vectorial, para Illustrator/InDesign/PPT
  <slug>-navy.png / <slug>-black.png   raster a 600 dpi para 40 mm
  <slug>-bloque.svg                    QR + leyenda + URL, ya a tamano real

Especificaciones fijadas a proposito:
  - correccion de error Q (25%): tolera dobleces del tubo y reflejos del plotter
  - quiet zone de 4 modulos, incluida en todos los archivos
  - oscuro sobre claro, nunca invertido
  - el bloque mide el QR en 40 mm reales (regla: distancia de escaneo / 10)

Uso:  python qr/make_qr.py
"""

import pathlib
import segno

BASE = "https://christianpichardo.github.io/ispor2026"

TARGETS = [
    # slug,        url,              leyenda impresa sobre el QR
    ("hub",      f"{BASE}/",  "Los dos posters"),
    ("poster-1", f"{BASE}/1/", "Descarga este poster"),
    ("poster-2", f"{BASE}/2/", "Descarga este poster"),
]

NAVY = "#12314f"
BLACK = "#000000"

ERROR = "q"          # 25% de correccion de error
BORDER = 4           # quiet zone, en modulos
QR_MM = 40.0         # lado del simbolo impreso, sin contar la quiet zone
DPI = 600

OUT = pathlib.Path(__file__).parent


def visible_url(url: str) -> str:
    """La URL como se imprime debajo del QR: sin esquema ni barra final."""
    return url.replace("https://", "").rstrip("/")


def bloque_svg(qr: segno.QRCode, url: str, leyenda: str) -> str:
    """QR + leyenda + URL en un SVG con unidades fisicas, listo para pegar."""
    matrix = [list(row) for row in qr.matrix]
    n = len(matrix)                       # modulos del simbolo, sin quiet zone
    mod = QR_MM / n                       # mm por modulo
    quiet = BORDER * mod

    pad_x = 2.0
    leyenda_h = 6.0
    gap_top = 2.0
    url_h = 5.0

    qr_x = pad_x + quiet
    qr_y = leyenda_h + gap_top + quiet
    w = QR_MM + 2 * quiet + 2 * pad_x
    h = leyenda_h + gap_top + QR_MM + 2 * quiet + url_h

    # Un solo path con todos los modulos oscuros: mas liviano y no deja
    # costuras blancas entre rectangulos al rasterizar.
    d = []
    for r, row in enumerate(matrix):
        c = 0
        while c < n:
            if row[c]:
                run = 1
                while c + run < n and row[c + run]:
                    run += 1
                x = qr_x + c * mod
                y = qr_y + r * mod
                d.append(f"M{x:.4f} {y:.4f}h{run * mod:.4f}v{mod:.4f}h{-run * mod:.4f}z")
                c += run
            else:
                c += 1

    font = "'Segoe UI',Arial,Helvetica,sans-serif"
    cx = w / 2

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{w:.2f}mm" height="{h:.2f}mm"
     viewBox="0 0 {w:.4f} {h:.4f}">
  <title>QR {visible_url(url)}</title>
  <rect width="{w:.4f}" height="{h:.4f}" fill="#ffffff"/>
  <text x="{cx:.4f}" y="{leyenda_h - 1.2:.4f}" font-family="{font}"
        font-size="3.6" font-weight="600" fill="{NAVY}"
        text-anchor="middle">{leyenda}</text>
  <path d="{''.join(d)}" fill="{NAVY}" shape-rendering="crispEdges"/>
  <text x="{cx:.4f}" y="{h - 1.3:.4f}" font-family="{font}"
        font-size="2.9" fill="#4a5a6a"
        text-anchor="middle">{visible_url(url)}</text>
</svg>
"""


def main() -> None:
    px_per_mm = DPI / 25.4
    print(f"{'archivo':<34} {'version':<9} {'modulos':<9} mm/modulo")
    print("-" * 68)

    for slug, url, leyenda in TARGETS:
        qr = segno.make(url, error=ERROR)
        n = len(qr.matrix)
        scale = max(1, round(QR_MM * px_per_mm / n))

        for name, color in (("navy", NAVY), ("black", BLACK)):
            qr.save(OUT / f"{slug}-{name}.svg", scale=10, border=BORDER,
                    dark=color, light="#ffffff", unit="mm", svgclass=None,
                    lineclass=None)
            qr.save(OUT / f"{slug}-{name}.png", scale=scale, border=BORDER,
                    dark=color, light="#ffffff", dpi=DPI)

        (OUT / f"{slug}-bloque.svg").write_text(
            bloque_svg(qr, url, leyenda), encoding="utf-8")

        print(f"{slug:<34} {qr.version:<9} {n}x{n:<5} {QR_MM / n:.2f} mm")
        print(f"   -> {url}")

    print("\nQuiet zone 4 modulos, correccion Q, QR impreso a 40 mm.")


if __name__ == "__main__":
    main()
