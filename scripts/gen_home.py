#!/usr/bin/env python3
"""Gera docs/index.html (página inicial de radarboi.com) a partir da W01 aprovada.
Rodar: python3 scripts/gen_home.py. Troque WA pelo número comercial quando existir."""
import pathlib, re, urllib.parse
R = pathlib.Path(__file__).resolve().parent.parent
WA = "5562900000000"  # TODO: número comercial do Radar Boi (mesmo placeholder do painel)
def wa(txt): return f"https://wa.me/{WA}?text=" + urllib.parse.quote(txt)
TESTE = wa("Quero testar o Radar Boi por 7 dias")
s = (R / "docs/design/web/w01-landing.html").read_text()
rep = [
 ('<title>W01 · Landing · Radar Boi</title>',
  '<title>Radar Boi · o leilão mais barato perto da sua fazenda</title>\n'
  '<meta name="description" content="Leilões de gado da sua região, lote por lote, do mais barato ao mais caro: R$/@, cor conferida e o vídeo no minuto do lance. Teste 7 dias grátis.">\n'
  '<meta property="og:title" content="Radar Boi · o leilão mais barato perto da sua fazenda">\n'
  '<meta property="og:description" content="Ranking dos leilões da sua região por R$/@, com cor conferida e link do vídeo no minuto do lote.">\n'
  '<meta property="og:image" content="https://radarboi.com/design/img/rmlJbmSu1i4_10_1.jpg">\n'
  '<meta name="theme-color" content="#1f4d2b">\n<link rel="icon" href="design/marca/app-verde.svg">\n<link rel="apple-touch-icon" href="design/marca/icone-radarboi-verde.png">'),
 ('href="../rb.css"', 'href="design/rb.css"'),
 ('<!-- Tela W01 · Landing de venda.', '<!-- Página inicial (gerada por scripts/gen_home.py a partir da W01).'),
 ('<a class="rb-logo claro" style="color:#fff">', '<a class="rb-logo claro" style="color:#fff;text-decoration:none" href="./">'),
 ('<nav><a>Como funciona</a><a>Cor conferida</a><a>WhatsApp</a><a>Planos</a><a>Entrar</a></nav>',
  '<nav><a href="#como">Como funciona</a><a href="#cor">Cor conferida</a><a href="#whatsapp">WhatsApp</a><a href="#planos">Planos</a><a href="painel/">Ver o painel</a></nav>'),
 ('<a class="rb-btn" style="color:#fff;border-color:#ffffff60;min-height:64px">Ver um resumo de exemplo</a>',
  '<a class="rb-btn" href="painel/" style="color:#fff;border-color:#ffffff60;min-height:64px">Ver os leilões da semana</a>'),
 ('<section class="sec">\n  <h2>"Nelore"', '<section class="sec" id="cor">\n  <h2>"Nelore"'),
 ('<section class="sec" style="padding-top:0">\n  <h2>Como funciona</h2>', '<section class="sec" id="como" style="padding-top:0">\n  <h2>Como funciona</h2>'),
 ('<section class="wa">', '<section class="wa" id="whatsapp">'),
 ('<span class="rb-tag rb-tag--exemplo">exemplo · lote real de 28/10</span>', '<span class="rb-tag">lote real · WM Uruaçu · 28/10</span>'),
 ('<a class="rb-btn rb-btn--sec rb-btn--full">Falar no WhatsApp</a>', f'<a class="rb-btn rb-btn--sec rb-btn--full" href="{wa("Quero saber do plano Fazenda+ do Radar Boi")}">Falar no WhatsApp</a>'),
]
for a, b in rep:
    assert a in s, a[:60]
    s = s.replace(a, b)
s = s.replace('src="../img/', 'src="design/img/')
# todos os botões "Testar 7 dias grátis" e o CTA final vão para o WhatsApp
s = re.sub(r'<a class="(rb-btn[^"]*)"([^>]*)>(Testar 7 dias grátis|Começar pelo WhatsApp)</a>',
           lambda m: f'<a class="{m.group(1)}" href="{TESTE}"{m.group(2)}>{m.group(3)}</a>', s)
assert 'section class="sec" id="planos"' in s
MOBILE = """
html{scroll-behavior:smooth}a.rb-btn{text-decoration:none}
@media(max-width:980px){
 .lp-top .in{height:68px;padding:0 18px;gap:12px}.lp-top nav{display:none}
 .lp-top .rb-btn{min-height:44px!important;font-size:15px!important;padding:0 14px}
 .hero{padding:96px 0 44px}.hero .in{grid-template-columns:1fr;gap:32px;padding:0 18px}
 .hero h1{font-size:36px;letter-spacing:-.8px}.hero p.l{font-size:18px;margin:16px 0 22px}
 .hero .ctas{flex-direction:column;align-items:stretch}.hero .ctas .rb-btn{width:100%}
 .prev{padding:16px}.prev .v{font-size:20px}.prev .n{font-size:16px}
 .nums .in{grid-template-columns:1fr 1fr;padding:22px 18px}.nums b{font-size:28px}
 .sec{padding:48px 18px}.sec h2{font-size:28px}.sec .lead{font-size:17px;margin-bottom:24px}
 .cor,.wa .sec,.faq,.planos{grid-template-columns:1fr}.wa .sec{gap:28px}
 .passos{grid-template-columns:1fr 1fr;gap:12px}.passo{padding:16px}.passo h3{font-size:18px}.passo p{font-size:15px}
 .cor .b .t{flex-direction:column;align-items:flex-start;gap:6px}.cor .b div[style*="display:flex"]{flex-wrap:wrap}
 .planos{gap:26px}.seg{display:flex;width:100%}.seg span{flex:1;text-align:center;padding:10px 8px;font-size:15px}
 .cta-f .sec{flex-direction:column;align-items:stretch;gap:20px;padding:36px 18px}.cta-f h2{font-size:26px}
 footer .in{flex-direction:column;gap:10px;padding:22px 18px}
 .lista li{font-size:17px}
}
@media(max-width:520px){.passos{grid-template-columns:1fr}.hero h1{font-size:32px}}
"""
s = s.replace("</style></head>", MOBILE + "</style></head>", 1)
(R / "docs/index.html").write_text(s)
print("docs/index.html ok")
