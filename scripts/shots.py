#!/usr/bin/env python3
"""Gera o PNG de cada tela de docs/design com o Chrome headless.
Uso: python3 scripts/shots.py [filtro]   (ex.: shots.py w01)
Web: janela 1440 x 6000 e corta o fundo que sobra embaixo. App/WhatsApp: janela 600 x 884 (o Chrome não abre janela estreita) e corta 430 x 884 no centro (moldura 390x844)."""
import subprocess, sys, pathlib
from PIL import Image, ImageChops

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
D = pathlib.Path(__file__).resolve().parent.parent / "docs" / "design"
OUT = D / "png"; OUT.mkdir(exist_ok=True)
filtro = sys.argv[1] if len(sys.argv) > 1 else ""

def shot(html, w, h, png):
    png.unlink(missing_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--user-data-dir=/tmp/rb-chrome", "--no-first-run",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    if not png.exists(): raise SystemExit(f"falhou: {html.name}")

def trim_bottom(png):
    im = Image.open(png).convert("RGB")
    bg = Image.new("RGB", im.size, im.getpixel((im.width - 1, im.height - 1)))
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        im.crop((0, 0, im.width, min(im.height, box[3] + 40))).save(png)

for f in sorted((D / "web").glob("*.html")) + [D / "componentes.html"]:
    if filtro in f.name:
        p = OUT / (f.stem + ".png"); shot(f, 1440, 6000, p); trim_bottom(p); print(p.name)
for sub in ("app", "whatsapp"):
    for f in sorted((D / sub).glob("*.html")):
        if filtro in f.name:
            p = OUT / (f.stem + ".png"); shot(f, 600, 884, p)
            Image.open(p).crop((85, 0, 515, 884)).save(p); print(p.name)
