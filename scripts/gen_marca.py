#!/usr/bin/env python3
"""Logo Radar Boi (B1 aprovada pelo Gabriel em 05/11): anel de radar + varredura + ponto (o lote achado) + Nelore de perfil.
Gera docs/design/marca/*.svg e o HTML usado para os PNGs. Rodar: python3 scripts/gen_marca.py"""
import pathlib
R = pathlib.Path(__file__).resolve().parent.parent
M = R / "docs/design/marca"
VERDE, AMARELO, ESCURO = "#1f4d2b", "#ffd54a", "#163a20"
BOI = '''<path fill="{c}" d="M9 58 C8 55 9 52 11 50 C14 45 18 40 22 37 C25 35 28 34.5 31 35 C32 29 36 24.5 41 24.5 C46 24.5 49 28 50.5 32 C52 33.5 55 34 58 34 L80 33.5 C85 33.5 88.5 35.5 89.5 39 C90.5 44 90 52 88.5 58 C88 61 87 63.5 86 65 L86.5 78 L87 81 L79.5 81 L79.5 76 L79 68 L77.5 68 L77 76 L77 81 L70.5 81 L70.8 76 L71 67.5 C64 68.5 56 69 49 68.5 L49 76 L49.5 81 L42.5 81 L42.5 76 L42.3 69 L41 69 L40.6 76 L41 81 L34 81 L34.2 76 L34 68.5 C31.5 68 29 67 27 65 C24.5 63 22.5 60.5 21 58 C19.5 59.5 17 61.5 14 62 C11.5 62.3 9.5 60.8 9 58 Z"/>
<path fill="{c}" d="M25.5 37 C23.5 33 23.6 28.5 26 25 C28.6 28.5 29.6 32.5 29 36.5 Z"/>
<path fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" d="M89.5 40 C91.5 47 91.6 57 91 66"/>
<path fill="{c}" d="M91 64 C93.2 66.5 93.2 71 91 73.5 C88.8 71 88.8 66.5 91 64 Z"/>
<circle cx="19.5" cy="43.5" r="1.4" fill="{bg}"/><circle cx="11.3" cy="56" r="1" fill="{bg}"/>'''
def simbolo(c, bg):
    return (f'<circle cx="50" cy="50" r="45" fill="none" stroke="{c}" stroke-width="6"/>'
            f'<path fill="{c}" fill-opacity=".2" d="M50 50 L50 5 A45 45 0 0 1 88.97 27.5 Z"/>'
            f'<circle cx="76" cy="20" r="5" fill="{c}"/>'
            f'<g transform="translate(48 56) scale(.78) translate(-50 -52)">{BOI.format(c=c, bg=bg)}</g>')
def svg(c, bg, fundo=None, raio=0, pad=0):
    vb = f"{-pad} {-pad} {100+2*pad} {100+2*pad}"
    f = f'<rect x="{-pad}" y="{-pad}" width="{100+2*pad}" height="{100+2*pad}" rx="{raio}" fill="{fundo}"/>' if fundo else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{f}{simbolo(c, bg)}</svg>'
ARQ = {
  "icone-verde.svg": svg(AMARELO, VERDE, VERDE, 0, 12),          # quadrado, fundo verde
  "icone-amarelo.svg": svg(VERDE, AMARELO, AMARELO, 0, 12),
  "app-verde.svg": svg(AMARELO, VERDE, VERDE, 30, 12),           # cantos arredondados (ícone app / site)
  "app-amarelo.svg": svg(VERDE, AMARELO, AMARELO, 30, 12),
  "simbolo-verde.svg": svg(VERDE, "#ffffff"),                    # só o símbolo, sem fundo
  "simbolo-branco.svg": svg("#ffffff", VERDE),
}
if __name__ == "__main__":
    for n, s in ARQ.items(): (M / n).write_text(s)
    # página para os PNGs
    def wm(cls): return f'<div class="wm {cls}"><img src="{"app-verde.svg" if cls=="esc" else "app-amarelo.svg"}"><span>Radar Boi</span></div>'
    html = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Marca · Radar Boi</title><style>
html,body{{margin:0;background:transparent;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}}
.wm{{display:none;align-items:center;gap:26px;padding:28px;font-weight:800;font-size:96px;letter-spacing:-2px;line-height:1}}
.wm img{{width:150px;height:150px}}.esc{{color:{ESCURO}}}.cla{{color:#fff}}
.q{{display:none;width:1080px;height:1080px}}.q img{{width:100%;height:100%;display:block}}
.ig{{display:none;width:1080px;height:1080px;background:{VERDE};place-items:center}}.ig img{{width:760px;height:760px}}
body.esc .wm.esc,body.cla .wm.cla{{display:inline-flex}}body.qv .q.v,body.qa .q.a{{display:block}}body.insta .ig{{display:grid}}
</style></head><body><script>document.body.className=location.hash.slice(1)||'esc'</script>
{wm("esc")}{wm("cla")}<div class="q v"><img src="icone-verde.svg"></div><div class="q a"><img src="icone-amarelo.svg"></div>
<div class="ig"><img src="simbolo-instagram.svg"></div></body></html>'''
    (M / "simbolo-instagram.svg").write_text(svg(AMARELO, VERDE))
    (M / "logo.html").write_text(html)
    print("ok")
