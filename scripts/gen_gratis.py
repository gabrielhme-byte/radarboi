#!/usr/bin/env python3
"""Telas do plano Radar Grátis (proposta do CEO, aguardando OK do Gabriel).
Gera web/w10..w13, app/a13..a15, whatsapp/z03. Rodar: python3 scripts/gen_gratis.py && python3 scripts/shots.py w1 && ... a1 / z03

Dados reais (docs/data.json), "hoje" = segunda 09/11/2026:
- Painel grátis = 7 dias de atraso -> leilões de 26/10 a 02/11, fêmeas de todas as eras e cores, até 250 km de Barro Alto/GO
  (16 leilões; R$/@ = soma R$ / soma @ estimadas, ponderado por cabeça).
- Resumo grátis = semana anterior 02 a 06/11, mesmo recorte: 1º Uruaçu R$ 270/@, 2º Niquelândia R$ 335/@, 3º Bela Vista de Goiás R$ 345/@.
- Lotes bloqueados: 4 lotes / 16 cab. no filtro padrão (fêmeas 6–8@ = 180–240 kg, cor ok, ≤250 km) de 02 a 06/11.
  (05/11: o lote qP6lHvAU3Bw 01:43:20 foi REPROVADO na cor; não usar.)
- "Você perdeu" = lote real rmlJbmSu1i4, quarta 28/10, WM Uruaçu: 7 bezerras brancas 12 m, ~210 kg, R$ 2.330/cab = R$ 333/@,
  24% abaixo da Scot (R$ 438/@). Minuto 1:05:30; live começou 20:19 -> ~21h25 (horário estimado pelo início da live).
"""
import math, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gen_app import page, sb, tab, WA_CSS, WAH, WAIN, FEED_CSS  # noqa: E402

R = pathlib.Path(__file__).resolve().parent.parent
D = R / "docs" / "design"
LEGAL = "Radar Boi é um produto da Starcore Produtos de Tecnologia Ltda, CNPJ 39.573.543/0001-33"

# ---------- dados reais ----------
data = json.loads((R / "docs" / "data.json").read_text())
LA, LO = -14.966, -48.908
def km(a, b):
    p = math.radians
    return 2 * 6371 * math.asin(math.sqrt(math.sin(p(a - LA) / 2) ** 2 + math.cos(p(LA)) * math.cos(p(a)) * math.sin(p(b - LO) / 2) ** 2))
def ranking(d0, d1):
    out = []
    for a in data["leiloes"]:
        if not (d0 <= a["data"] <= d1): continue
        k = km(a["lat"], a["lon"])
        if k > 250: continue
        ls = [l for l in data["lotes"] if l["v"] == a["v"] and l["s"] == "F" and l["p"] and l["kg"]]
        if not ls: continue
        q = sum(l["q"] for l in ls)
        arr = sum(l["p"] * l["q"] for l in ls) / sum(l["kg"] / 30 * l["q"] for l in ls)
        cab = sum(l["p"] * l["q"] for l in ls) / q
        out.append(dict(arr=round(arr), cab=round(cab), cidade=a["cidade"], casa=a["casa"].split(" - ")[0], data=a["data"], km=round(k), q=q, n=len(ls)))
    return sorted(out, key=lambda x: x["arr"])
RK = ranking("2026-10-26", "2026-11-02")
SEM = ranking("2026-11-02", "2026-11-06")
assert [x["arr"] for x in SEM[:3]] == [270, 335, 345], SEM[:3]
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
import datetime as dt
def dfmt(s):
    d = dt.date.fromisoformat(s); return f"{DIAS[d.weekday()]} {d.day:02d}/{d.month:02d}"
def brl(n): return f"{n:,}".replace(",", ".")
CAB_TOT = sum(x["q"] for x in RK)

PERDEU_TXT = "Quarta 28/10, por volta das 21h25, entrou em Uruaçu um lote de <b>7 bezerras brancas</b> de 12 meses a <b>R$ 333/@</b>, <b>24% abaixo da Scot</b>. Os assinantes receberam o alerta na hora."
PERDEU_SRC = "WM Leilões, Uruaçu · lance R$ 2.330/cab · ~210 kg (estimado pela era) · vídeo no minuto 1:05:30 · horário estimado pelo início da live (20:19)"

def web(title, nota, css, corpo, nav_on="", gratis=True, nav=True):
    navs = [("Ranking", False), ("Lotes", True), ("Agenda", False), ("Alertas", True), ("Conta", False)]
    nv = "".join(f'<a class="{"is-on" if n == nav_on else ""}">{n}{" 🔒" if b and gratis else ""}</a>' for n, b in navs) if nav else ""
    chip = '<span class="rb-plano rb-plano--gratis">Radar Grátis</span>' if gratis else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Radar Boi</title>
<link rel="stylesheet" href="../rb.css">
<style>{css}</style></head>
<body>
<!-- {title}. Plano Radar Grátis: APROVADO pelo Gabriel. Cobrança Mercado Pago: cartão mensal ou Pix anual.
     {nota} -->
<header class="w-top"><div class="in">
  <span class="rb-logo claro" style="color:#fff"><i>◎</i>Radar Boi</span>
  <nav>{nv}</nav>{chip}
  <div class="av">G</div>
</div></header>
<main class="w-main">
{corpo}
</main>
<footer class="rb-rodape">Dados de transmissões públicas de leilões. Não compramos, não vendemos e não damos lance.<br><b>{LEGAL}</b></footer>
</body></html>"""

S = {}

# =====================================================================
# W10 · Seu teste acabou
# =====================================================================
W10_CSS = """
.hero{display:grid;grid-template-columns:1.35fr 1fr;gap:28px;align-items:stretch;margin-top:8px}
.hero h1{font:800 40px/1.1 var(--fonte);color:var(--verde-900);letter-spacing:-1px}
.hero p.s{font-size:19px;color:var(--cinza);margin:10px 0 18px;max-width:640px}
.guard{display:flex;gap:10px;flex-wrap:wrap}
.guard span{background:#fff;border:1px solid var(--areia);border-radius:12px;padding:10px 14px;font-size:16px}
.guard span b{color:var(--verde-800)}
.planos{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:30px}
.pc{background:#fff;border:2px solid var(--areia);border-radius:18px;padding:20px;display:flex;flex-direction:column;gap:10px;position:relative}
.pc.rec{border-color:var(--verde-600);box-shadow:0 10px 30px #1f4d2b22}
.pc .fita{position:absolute;top:-13px;left:20px;background:var(--amarelo);color:var(--verde-900);font:800 13px/1 var(--fonte);padding:6px 10px;border-radius:999px;text-transform:uppercase;letter-spacing:.5px}
.pc h3{font:800 20px/1.2 var(--fonte)}
.pc .p{font:800 34px/1 var(--fonte);color:var(--verde-900)}.pc .p small{font-size:15px;color:var(--cinza);font-weight:600}
.pc .an{font-size:14px;color:var(--cinza);min-height:20px}
.pc ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px;font-size:15px}
.pc li{display:flex;gap:8px;align-items:flex-start}.pc li::before{content:"✓";color:var(--barato);font-weight:900}
.pc li.x{color:#77756d}.pc li.x::before{content:"🔒";font-size:12px;margin-top:2px}
.pc .rb-btn{margin-top:auto}
.cmp{margin-top:30px}
.cmp table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--areia);border-radius:16px;overflow:hidden;font-size:16px}
.cmp th,.cmp td{padding:13px 16px;border-top:1px solid #eee;text-align:left}
.cmp th{background:var(--creme);font-size:14px;color:var(--cinza);text-transform:uppercase;letter-spacing:.5px;border-top:0}
.cmp td:nth-child(2){color:#4a4a45}.cmp td:nth-child(3){font-weight:700;color:var(--verde-800)}
.pag{display:flex;align-items:center;gap:14px;margin-top:22px;background:#fff;border:1px solid var(--areia);border-radius:16px;padding:16px 20px;font-size:16px}
"""
S["web/w10-teste-acabou"] = web("W10 · Seu teste acabou", """Aparece no 1º acesso depois do fim do teste de 7 dias (e é o destino do link do WhatsApp do dia 7).
     Padrão pré-selecionado: Pro (o que a pessoa usou). Se fechar a tela ou tocar em "Ficar no Radar Grátis", a conta vira status gratuita:
     NADA é apagado (fazenda, filtros, salvos, custos). Assinar = 1 toque: link do Mercado Pago (cartão todo mês ou Pix anual); os filtros voltam como estavam.
     Números de "nos seus 7 dias" vêm da conta (aqui: exemplo). O bloco "você perdeu" usa o melhor lote real e de cor conferida que passou no filtro dela.""", W10_CSS, f"""
<div class="hero">
  <div>
    <span class="rb-tag" style="background:var(--aviso-bg);color:var(--aviso)">Teste do Pro terminou em 08/11 <span class="rb-tag rb-tag--exemplo" style="margin-left:4px">exemplo</span></span>
    <h1 style="margin-top:12px">Seu teste de 7 dias acabou, Gabriel.<br>Como você quer continuar?</h1>
    <p class="s">Nada foi apagado. Sua fazenda, seus filtros e seus lotes salvos ficam guardados. Para voltar ao Pro é um toque.</p>
    <div class="guard"><span>📍 <b>Barro Alto/GO</b> · 250 km</span><span>🐂 <b>Fêmeas 6–8@</b> · 100% brancas</span><span>★ <b>2</b> lotes salvos</span><span>💰 custos preenchidos</span></div>
  </div>
  <div class="rb-perdeu"><div class="tp">🔴 Você perdeu</div><img src="../img/rmlJbmSu1i4_10_1.jpg" alt=""><div class="cp"><div class="q">{PERDEU_TXT}</div><div class="src">{PERDEU_SRC}</div></div></div>
</div>
<div class="planos">
  <div class="pc"><h3>Radar Grátis</h3><div class="p">R$ 0</div><div class="an">para sempre</div>
    <ul><li>Resumo de segunda: 3 cidades e R$/@</li><li>Painel com 7 dias de atraso</li><li>1 alerta ao vivo por mês</li><li class="x">Nome do leilão e link do lote</li><li class="x">Filtro de peso e cor</li><li class="x">Margem</li></ul>
    <a class="rb-btn rb-btn--sec rb-btn--full">Ficar no Radar Grátis</a></div>
  <div class="pc"><h3>Semanal</h3><div class="p">R$ 79<small>/mês</small></div><div class="an">ou R$ 790/ano</div>
    <ul><li>Resumo de segunda completo</li><li>Ranking com nome do leilão</li><li>Link do lote no vídeo</li><li class="x">Alerta entrando agora</li></ul>
    <a class="rb-btn rb-btn--sec rb-btn--full">Assinar o Semanal</a></div>
  <div class="pc rec"><span class="fita">O que você usou</span><h3>Pro</h3><div class="p">R$ 149<small>/mês</small></div><div class="an">ou R$ 1.490/ano (2 meses grátis)</div>
    <ul><li>Painel ao vivo, filtro de peso e cor</li><li>Alerta "entrando agora", sem limite</li><li>Margem com os seus custos</li><li>Tudo do Semanal</li></ul>
    <a class="rb-btn rb-btn--pri rb-btn--full">Voltar para o Pro</a></div>
  <div class="pc"><h3>Fazenda+</h3><div class="p">R$ 399<small>/mês</small></div><div class="an">várias fazendas</div>
    <ul><li>3 fazendas e 5 pessoas</li><li>Freteiros da rota</li><li>Atendimento direto</li><li>Tudo do Pro</li></ul>
    <a class="rb-btn rb-btn--sec rb-btn--full">Falar com a gente</a></div>
</div>
<div class="pag">💳 <span><b>Cartão</b> todo mês ou <b>Pix anual</b> (2 meses grátis), pelo Mercado Pago. Cancela quando quiser, sem ligação.</span><span style="margin-left:auto">🎁 Ou <a><b>indique 1 fazendeiro</b></a> que assine e ganhe 1 mês de Pro.</span></div>
<div class="cmp"><table>
<tr><th>O que muda</th><th>Radar Grátis</th><th>Pro</th></tr>
<tr><td>Resumo de segunda no WhatsApp</td><td>3 primeiras cidades e R$/@</td><td>Completo, com leilão, lote e margem</td></tr>
<tr><td>Painel de leilões</td><td>7 dias de atraso, só consulta</td><td>Ao vivo, atualizado a cada leilão</td></tr>
<tr><td>Filtro de peso e cor</td><td>🔒</td><td>✓</td></tr>
<tr><td>Lote por lote, com foto e vídeo no minuto</td><td>🔒</td><td>✓</td></tr>
<tr><td>Alerta "entrando agora"</td><td>1 por mês</td><td>Sem limite</td></tr>
<tr><td>Margem com os seus custos</td><td>🔒</td><td>✓</td></tr>
<tr><td>Sua fazenda, filtros e salvos</td><td>Guardados</td><td>Guardados</td></tr>
</table></div>
""", gratis=True, nav=False)

# =====================================================================
# W11 · Painel no Radar Grátis (7 dias de atraso)
# =====================================================================
rows = []
for i, x in enumerate(RK, 1):
    rows.append(f"""<tr><td class="po">{i}º</td><td><b>{x['cidade']}</b><small>{x['casa']}</small></td><td>{dfmt(x['data'])}</td><td class="num">{x['km']} km</td><td class="num">{x['q']} cab.</td><td class="num v">R$ {x['arr']}/@</td><td class="num">R$ {brl(x['cab'])}</td><td><span class="rb-cadeado">lotes</span></td></tr>""")
W11_CSS = """
.lay{display:grid;grid-template-columns:1fr 340px;gap:28px;align-items:start;margin-top:18px}
.filtros{display:flex;gap:10px;flex-wrap:wrap;align-items:center;background:#fff;border:1px solid var(--areia);border-radius:16px;padding:14px 16px;margin:18px 0}
.filtros .lb{font:700 15px/1 var(--fonte);color:var(--cinza);margin-right:4px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
.kpi-b .val{display:flex;align-items:center;gap:8px}
table.rk{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--areia);border-radius:16px;overflow:hidden}
.rk th{background:var(--creme);text-align:left;font-size:13px;color:var(--cinza);text-transform:uppercase;letter-spacing:.5px;padding:10px 12px}
.rk td{padding:10px 12px;border-top:1px solid #eee;font-size:16px;vertical-align:middle}
.rk td small{display:block;color:var(--cinza);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}
.rk td:not(:nth-child(2)){white-space:nowrap}
.rk .po{font:800 17px/1 var(--fonte);color:var(--verde-800);width:44px}
.rk .v{font:800 19px/1 var(--fonte);color:var(--verde-900);white-space:nowrap}
.lado>*{margin-bottom:16px}
.alg{background:#fff;border:1px solid var(--areia);border-radius:16px;padding:16px}
.alg h3{font-size:18px}.alg p{margin:6px 0 10px;color:var(--cinza);font-size:15px}
.cont{display:flex;gap:6px;margin:8px 0 12px}.cont i{flex:1;height:10px;border-radius:5px;background:var(--verde-600)}
"""
S["web/w11-painel-gratis"] = web("W11 · Painel no Radar Grátis", """Mesmo W04, em modo consulta: dados com 7 dias de atraso (corte = hoje − 7 dias; aqui hoje = seg 09/11 → leilões até 02/11).
     Sem filtro de peso e cor: o recorte é fixo em fêmeas (ou machos, conforme o perfil), todas as eras e cores, no raio da fazenda.
     Bloqueado (rb-cadeado / rb-chip.is-bloq): lotes, comparação com a Scot, margem, filtros de peso e cor, PDF. Clique em qualquer 🔒 abre W10.
     IMPORTANTE p/ dev: dado bloqueado NÃO vai no HTML/JSON da conta grátis (nada de esconder com CSS). O blur das telas usa valores falsos.""", W11_CSS, f"""
<div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div><h1 class="w-h1">Onde a @ estava mais barata</h1><div class="w-sub">Leilões de 26/10 a 02/11 · fêmeas de todas as eras e cores · até 250 km de Barro Alto/GO</div></div>
</div>
<div class="rb-atraso" style="margin-top:18px"><span class="ic">⏱</span><div><b>Você está vendo dados de 7 dias atrás, como cotação atrasada.</b><br>No Pro, o ranking atualiza a cada leilão e o alerta chega com o lote na pista.</div><a class="rb-btn rb-btn--pri">Ver ao vivo no Pro</a></div>
<div class="filtros"><span class="lb">Filtros</span><span class="rb-chip is-on">Fêmeas</span><span class="rb-chip is-on">Até 250 km</span><span class="rb-chip is-bloq">Peso 6–8@</span><span class="rb-chip is-bloq">Só 100% brancas</span><span class="rb-chip is-bloq">Vender com 15@</span><span class="rb-cadeado" style="margin-left:auto">Baixar PDF</span></div>
<div class="kpis">
  <div class="rb-kpi rb-kpi--destaque"><div class="rot">Mais barato</div><div class="val num">R$ {RK[0]['arr']}<small>/@</small></div><div class="sub">{RK[0]['cidade']} · {RK[0]['km']} km · {dfmt(RK[0]['data'])}</div></div>
  <div class="rb-kpi"><div class="rot">Leilões no raio</div><div class="val num">{len(RK)}</div><div class="sub">{brl(CAB_TOT)} fêmeas na pista</div></div>
  <div class="rb-kpi kpi-b"><div class="rot">Contra a Scot</div><div class="val"><span class="rb-cadeado" style="font-size:16px">só no Pro</span></div><div class="sub">quanto abaixo da referência</div></div>
  <div class="rb-kpi kpi-b"><div class="rot">Margem até 15@</div><div class="val"><span class="rb-cadeado" style="font-size:16px">só no Pro</span></div><div class="sub">com os seus custos</div></div>
</div>
<div class="lay">
  <div>
    <table class="rk"><tr><th>#</th><th>Cidade · leiloeira</th><th>Data</th><th>Distância</th><th>Fêmeas</th><th>R$/@ est.</th><th>R$/cab</th><th></th></tr>{''.join(rows)}</table>
    <div class="rb-nota" style="margin-top:12px">R$/@ = soma dos lances ÷ soma das @ estimadas pela era (8 m 180 kg, 12 m 210 kg, 18 m 270 kg), ponderado por cabeça. Mistura todas as eras e cores, por isso não é comparável com o ranking do Pro.</div>
  </div>
  <aside class="lado">
    <div class="rb-perdeu"><div class="tp">🔴 Você perdeu</div><img src="../img/rmlJbmSu1i4_10_1.jpg" alt=""><div class="cp"><div class="q" style="font-size:17px">{PERDEU_TXT}</div><div class="src">{PERDEU_SRC}</div><a class="rb-btn rb-btn--pri rb-btn--full" style="font-size:17px">Receber o próximo na hora</a></div></div>
    <div class="alg"><h3>🔔 Seu alerta grátis de novembro</h3><p>1 alerta "entrando agora" por mês, para você sentir como é.</p><div class="cont"><i></i></div><b>1 disponível</b><span class="muted"> · vale para o próximo lote do seu filtro</span></div>
    <div class="alg" style="background:var(--verde-50);border-color:#cfe3d4"><h3>🎁 Ganhe 1 mês de Pro</h3><p>Indique um fazendeiro. Se ele assinar, você ganha 1 mês do Pro.</p><a class="rb-btn rb-btn--sec rb-btn--full" style="font-size:17px">Indicar no WhatsApp</a></div>
  </aside>
</div>
""", nav_on="Ranking")

# =====================================================================
# W12 · Como fica cada tela bloqueada
# =====================================================================
FAKE_ROW = """<div class="fr"><span class="ph"></span><div><b>0 bezerras · 00 meses</b><small>Cidade · Leiloeira · 00 km</small></div><b>R$ 0.000</b><b class="g">R$ 000/@</b><b>R$ 0.000</b><span class="rb-btn rb-btn--sec" style="min-height:40px;font-size:15px">▶ 0:00:00</span></div>"""
W12_CSS = """
.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:22px}
.pn{background:#fff;border:1px solid var(--areia);border-radius:18px;padding:18px}
.pn>h2{font:800 20px/1.2 var(--fonte);color:var(--verde-900);display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.pn>h2 code{font:600 13px/1 ui-monospace,Menlo,monospace;color:var(--cinza)}
.pn>p{color:var(--cinza);font-size:15px;margin:6px 0 14px}
.fr{display:grid;grid-template-columns:110px 1fr 90px 100px 90px 110px;gap:12px;align-items:center;padding:12px;border:1px solid var(--areia);border-radius:12px;margin-bottom:8px;background:#fff}
.fr .ph{height:46px;border-radius:8px;background:linear-gradient(135deg,#7a8f6a,#c9c2a8)}
.fr small{display:block;color:var(--cinza)}
.lk{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-top:1px solid #eee;font-size:17px}
.ex{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.mini-ag{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.mini-ag div{border:1px solid var(--areia);border-radius:12px;padding:12px}
.mini-ag b{display:block;font-size:17px}.mini-ag small{color:var(--cinza)}
.mini-ag .r{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-weight:700}
"""
S["web/w12-bloqueios"] = web("W12 · Telas bloqueadas no Radar Grátis", """Catálogo de como cada tela fica para a conta grátis. Componentes: Bloqueio (.rb-bloq: blur + cadeado + CTA),
     CampoBloqueado (.rb-cadeado), ChipBloqueado (.rb-chip.is-bloq), AvisoAtraso (.rb-atraso), CardVocePerdeu (.rb-perdeu), SeloPlano (.rb-plano).
     Regra de texto: sempre dizer O QUE a pessoa ganha ("lote por lote, com foto e vídeo"), nunca só "conteúdo bloqueado".
     Todo 🔒 é clicável e abre W10 (escolha de plano). Atrás do blur vão valores falsos (0.000), nunca o dado real.""", W12_CSS, f"""
<h1 class="w-h1">Como fica cada tela no Radar Grátis</h1>
<div class="w-sub">Regra: o grátis vê <b>o mercado</b> (cidade e R$/@, com atraso); o Pro vê <b>o lote</b> (qual, onde, quando, quanto sobra). Todo cadeado abre a escolha de plano (W10).</div>
<div class="grid">
  <div class="pn"><h2>Componentes <code>Bloqueio · CampoBloqueado · ChipBloqueado</code></h2><p>Três jeitos de bloquear, do mais forte ao mais leve.</p>
    <div class="ex" style="margin-bottom:14px"><span class="rb-cadeado">lotes</span><span class="rb-cadeado">só no Pro</span><span class="rb-chip is-bloq">Só 100% brancas</span><span class="rb-chip is-bloq">Peso 6–8@</span><span class="rb-plano rb-plano--gratis" style="background:var(--verde-800)">Radar Grátis</span></div>
    <div class="rb-atraso"><span class="ic">⏱</span><div><b>Dados de 7 dias atrás.</b> No Pro, ao vivo.</div><a class="rb-btn rb-btn--pri">Ver ao vivo</a></div>
  </div>
  <div class="pn"><h2>Ranking <code>W04 → W11</code></h2><p>Aberto, com 7 dias de atraso. Sem nome do lote, Scot, margem nem filtros de peso e cor.</p>
    <div class="lk"><span>Uruaçu · WM Leilões · qua 28/10</span><b>R$ 303/@</b></div>
    <div class="lk"><span>Contra a Scot</span><span class="rb-cadeado">só no Pro</span></div>
    <div class="lk"><span>Margem até 15@</span><span class="rb-cadeado">só no Pro</span></div>
    <div class="lk"><span>Ver os lotes deste leilão</span><span class="rb-cadeado">lotes</span></div>
  </div>
  <div class="pn" style="grid-column:1/3"><h2>Lotes <code>W05</code></h2><p>A lista inteira fica atrás do cadeado. O grátis vê quantos lotes havia, não quais.</p>
    <div class="rb-bloq"><div class="atras">{FAKE_ROW*4}</div>
      <div class="cad"><span class="i">🔒</span><h4>4 lotes (16 cabeças) passaram no seu filtro de 02 a 06/11</h4><p>Lote por lote, com foto, cor conferida e o vídeo no minuto do lance. É do Pro.</p>
        <div style="display:flex;gap:10px"><a class="rb-btn rb-btn--pri">Voltar para o Pro · R$ 149/mês</a><a class="rb-btn rb-btn--sec">🎁 Indicar e ganhar 1 mês</a></div></div></div>
  </div>
  <div class="pn"><h2>Detalhe do lote <code>W06</code></h2><p>O grátis só chega aqui pelo alerta grátis do mês ou pelo "você perdeu". Mostra o preço; esconde o vídeo e a margem.</p>
    <div class="lk"><span>7 bezerras brancas · 12 m</span><b>R$ 333/@</b></div>
    <div class="lk"><span>Lance na tela</span><b>R$ 2.330/cab</b></div>
    <div class="lk"><span>▶ Vídeo no minuto do lance</span><span class="rb-cadeado">só no Pro</span></div>
    <div class="lk"><span>Margem com os seus custos</span><span class="rb-cadeado">só no Pro</span></div>
  </div>
  <div class="pn"><h2>Alertas <code>W08</code></h2><p>1 alerta "entrando agora" grátis por mês, no filtro salvo. Depois de usado, a regra fica pausada até o mês virar.</p>
    <div class="lk"><span>🔴 Bezerra/novilha branca 6–8@ entrando agora</span><span class="rb-toggle is-on"></span></div>
    <div style="display:flex;gap:6px;margin:4px 0 8px"><i style="flex:1;height:10px;border-radius:5px;background:var(--verde-600)"></i></div>
    <div class="muted" style="font-size:15px"><b style="color:var(--tinta)">1 de 1 disponível em novembro.</b> Depois: alertas sem limite no Pro.</div>
    <div class="lk"><span>Criar outro aviso</span><span class="rb-cadeado">só no Pro</span></div>
  </div>
  <div class="pn"><h2>Agenda <code>W07</code></h2><p>Aberta: é informação pública. O aviso de catálogo e de entrada é do Pro. <span class="rb-tag rb-tag--exemplo">datas exemplo</span></p>
    <div class="mini-ag"><div><b>Uruaçu</b><small>qua 11/11 · 55 km</small><div class="r"><span>🔔 Avisar</span><span class="rb-cadeado">Pro</span></div></div><div><b>Niquelândia</b><small>ter 10/11 · 73 km</small><div class="r"><span>🔔 Avisar</span><span class="rb-cadeado">Pro</span></div></div></div>
  </div>
  <div class="pn"><h2>Conta <code>W09</code></h2><p>Mostra o plano grátis e o que está guardado. Voltar é um toque.</p>
    <div class="lk"><span>Plano</span><b>Radar Grátis</b></div>
    <div class="lk"><span>Fazenda, filtros e 2 lotes salvos</span><b class="g">guardados</b></div>
    <a class="rb-btn rb-btn--pri rb-btn--full" style="margin-top:10px">Voltar para o Pro com 1 toque</a>
  </div>
</div>
""", nav_on="")

# =====================================================================
# W13 · Indique e ganhe
# =====================================================================
W13_CSS = """
.lay{display:grid;grid-template-columns:1.1fr 1fr;gap:28px;align-items:start;margin-top:10px}
.big{font:800 44px/1.08 var(--fonte);color:var(--verde-900);letter-spacing:-1px}
.lk2{display:flex;gap:10px;align-items:center;background:#fff;border:2px solid var(--verde-600);border-radius:14px;padding:8px 8px 8px 16px;margin-top:20px;font:700 19px/1 var(--fonte)}
.lk2 span{flex:1}
.passos{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}
.passos div{background:#fff;border:1px solid var(--areia);border-radius:14px;padding:14px}
.passos b{display:block;font:800 26px/1 var(--fonte);color:var(--amarelo);-webkit-text-stroke:1px var(--verde-800);margin-bottom:6px}
.wa{background:var(--wa-bg);border-radius:18px;padding:18px}
.wa .m{background:var(--wa-eu);border-radius:10px;padding:10px 12px;font-size:16px;line-height:1.4;box-shadow:0 1px 1px #0001}
.wa .m .lnk{background:#fff;border-radius:8px;margin-top:8px;padding:10px;font-size:14px;border-left:4px solid var(--verde-600)}
.st{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}
.ind .it{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-top:1px solid #eee;font-size:16px}
"""
S["web/w13-indique"] = web("W13 · Indique e ganhe 1 mês de Pro", """Link pessoal radarboi.com/i/{codigo}. Quem entra pelo link ganha o teste normal de 7 dias.
     Recompensa: quando o indicado paga a 1ª mensalidade (qualquer plano pago), quem indicou ganha 1 mês de Pro (no grátis: vira Pro por 1 mês;
     no pago: 1 mensalidade a menos). Sem limite. Aviso no WhatsApp para os dois. Antifraude: mesmo CPF/telefone não conta; pagamento estornado cancela o prêmio.
     Regras aprovadas pelo Gabriel.""", W13_CSS, f"""
<div class="lay">
  <div>
    <span class="rb-tag rb-tag--margem">🎁 Indique e ganhe</span>
    <h1 class="big" style="margin-top:12px">Indique um fazendeiro.<br>Se ele assinar, você ganha <span style="background:var(--amarelo);padding:0 8px;border-radius:8px">1 mês de Pro</span>.</h1>
    <p class="w-sub">Vale para cada vizinho, parceiro ou comprador que assinar. Sem limite.</p>
    <div class="lk2"><span>radarboi.com/i/gabriel <span class="rb-tag rb-tag--exemplo">exemplo</span></span><a class="rb-btn rb-btn--sec" style="min-height:48px">Copiar</a></div>
    <a class="rb-btn rb-btn--wa rb-btn--full" style="margin-top:12px;font-size:20px">Mandar no WhatsApp</a>
    <div class="passos"><div><b>1</b>Você manda o link no WhatsApp</div><div><b>2</b>Ele testa 7 dias grátis</div><div><b>3</b>Ele assina: você ganha 1 mês de Pro</div></div>
  </div>
  <div>
    <div class="wa"><div class="muted small" style="margin-bottom:8px">Mensagem pronta (dá para editar antes de mandar)</div>
      <div class="m">Opa! Tô usando o <b>Radar Boi</b>: ele mostra os leilões aqui da região do mais barato ao mais caro, com o R$/@ de cada lote e o vídeo no minuto do lance. Testa 7 dias grátis:
        <div class="lnk"><b>Radar Boi · O leilão mais barato perto da sua fazenda</b><br><span class="muted">radarboi.com/i/gabriel</span></div></div></div>
    <div class="w-card ind" style="margin-top:16px"><h3 style="font-size:19px;margin-bottom:6px">Suas indicações <span class="rb-tag rb-tag--exemplo">exemplo</span></h3>
      <div class="it"><span>José · Goianésia</span><span class="rb-tag" style="background:var(--aviso-bg);color:var(--aviso)">testando · 3 dias</span></div>
      <div class="it"><span>Marcos · Uruaçu</span><span class="rb-tag" style="background:var(--barato-bg);color:var(--barato)">assinou · +1 mês pra você</span></div>
      <div class="it"><span>Total ganho</span><b>1 mês de Pro</b></div>
    </div>
    <div class="rb-nota" style="margin-top:12px">O prêmio entra quando o indicado paga a 1ª mensalidade. Mesmo telefone ou CPF não conta duas vezes.</div>
  </div>
</div>
""", nav_on="Conta")

# =====================================================================
# APP
# =====================================================================
A13_CSS = """
.ta{padding:4px 18px 0;flex:1;overflow:hidden}
.ta h1{font:800 27px/1.12 var(--fonte);color:var(--verde-900);letter-spacing:-.4px;margin:6px 0 6px}
.ta p.s{font-size:16px;color:var(--cinza);margin:0 0 12px}
.op{display:flex;align-items:center;gap:12px;background:#fff;border:2px solid var(--areia);border-radius:16px;padding:12px 14px;margin-bottom:9px}
.op.on{border-color:var(--verde-600);background:var(--verde-50)}
.op .rd{width:24px;height:24px;border-radius:50%;border:2px solid #b5b2a6;flex:none}
.op.on .rd{border:7px solid var(--verde-600)}
.op b{font-size:18px;display:block}.op small{font-size:14px;color:var(--cinza);display:block;line-height:1.3}
.op .p{margin-left:auto;text-align:right;font:800 19px/1.1 var(--fonte);white-space:nowrap}.op .p small{font-size:12px}
.bt{padding:10px 18px 30px;background:var(--creme)}
"""
S["app/a13-teste-acabou"] = page("A13 · Seu teste acabou (app)", sb() + f"""
<div class="ta">
  <h1>Seu teste de 7 dias acabou.</h1>
  <p class="s">Sua fazenda, filtros e salvos ficam guardados. Voltar é um toque.</p>
  <div class="rb-perdeu" style="margin-bottom:12px"><div class="tp">🔴 Você perdeu</div><div class="cp" style="padding:10px 12px"><div class="q" style="font-size:15px">Qua 28/10, ~21h25, em Uruaçu: <b>7 bezerras brancas</b> a <b>R$ 333/@</b>, <b>24% abaixo da Scot</b>. Os assinantes receberam na hora.</div></div></div>
  <div class="op on"><span class="rd"></span><div><b>Pro</b><small>Ao vivo, peso e cor, alerta sem limite</small></div><div class="p">R$ 149<br><small>/mês</small></div></div>
  <div class="op"><span class="rd"></span><div><b>Semanal</b><small>Resumo completo de segunda</small></div><div class="p">R$ 79<br><small>/mês</small></div></div>
  <div class="op"><span class="rd"></span><div><b>Radar Grátis</b><small>3 cidades no resumo, painel 7 dias atrasado, 1 alerta/mês</small></div><div class="p">R$ 0</div></div>
  <div style="text-align:center;font-size:15px;margin-top:6px">🎁 <a><b>Indique 1 fazendeiro</b></a> e ganhe 1 mês de Pro</div>
</div>
<div class="bt"><a class="rb-btn rb-btn--pri rb-btn--full" style="font-size:20px">Continuar no Pro</a><div class="muted" style="text-align:center;font-size:13px;margin-top:8px">Cartão todo mês ou Pix anual · Mercado Pago</div></div>
""", A13_CSS, nota="Abre no lugar da Início no 1º acesso após o fim do teste. Pro pré-selecionado. Fechar = Radar Grátis (nada é apagado).")

FAKE_CARD = """<article class="rb-lote"><div class="foto" style="background:linear-gradient(135deg,#7a8f6a,#c9c2a8)"></div><div class="corpo"><div class="tit"><h3>0 bezerras · 00 m</h3><span class="cab num">R$ 0.000</span></div><div class="linha"><span class="arroba num">R$ 000/@</span></div><div class="meta">Cidade · 00 km · dia 00/00</div></div></article>"""
A14_CSS = FEED_CSS + """
.at{margin:0 16px 10px;background:var(--aviso-bg);border:1.5px solid #e9cf8a;border-radius:14px;padding:10px 12px;font-size:14px;color:#4a3a00;display:flex;gap:10px;align-items:center}
.at b{color:var(--tinta)}
.feed .rb-bloq{border-radius:16px}
.feed .rb-bloq .atras{display:flex;flex-direction:column;gap:12px}
.feed .rb-bloq .cad h4{font-size:19px}.feed .rb-bloq .cad p{font-size:15px}
"""
S["app/a14-lotes-gratis"] = page("A14 · Lotes no Radar Grátis (app)", sb() + f"""
<div class="a-hd"><h1>Lotes</h1><span class="rb-plano rb-plano--gratis" style="background:var(--verde-800)">Radar Grátis</span></div>
<div class="chs"><span class="rb-chip is-on">Fêmeas</span><span class="rb-chip is-on">250 km</span><span class="rb-chip is-bloq">6–8@</span><span class="rb-chip is-bloq">Brancas</span></div>
<div class="at">⏱ <span><b>Dados de 7 dias atrás.</b> Até 02/11.</span></div>
<div class="a-body pad0"><div class="feed">
  <div class="rb-bloq"><div class="atras">{FAKE_CARD*2}</div>
    <div class="cad"><span class="i">🔒</span><h4>4 lotes passaram no seu filtro de 02 a 06/11</h4><p>Com foto, cor conferida e o vídeo no minuto do lance. É do Pro.</p>
      <a class="rb-btn rb-btn--pri rb-btn--full">Voltar para o Pro</a><a class="rb-btn rb-btn--txt" style="font-size:16px">🎁 Indicar e ganhar 1 mês</a></div></div>
</div></div>""" + tab("lotes"), A14_CSS, nota="Feed bloqueado: o servidor não manda lotes para conta grátis, só a contagem. Os cards atrás do blur são falsos. Chips 🔒 abrem A13.")

A15_CSS = """
.ix{padding:4px 18px 0;flex:1;overflow:hidden}
.ix .gift{width:72px;height:72px;border-radius:20px;background:var(--amarelo);display:grid;place-items:center;font-size:40px;margin:6px 0 12px}
.ix h1{font:800 28px/1.12 var(--fonte);color:var(--verde-900);letter-spacing:-.4px}
.ix p.s{font-size:17px;color:var(--cinza);margin:8px 0 16px}
.ps{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}
.ps div{display:flex;gap:12px;align-items:center;background:#fff;border:1px solid var(--areia);border-radius:14px;padding:12px 14px;font-size:16px}
.ps b{width:32px;height:32px;border-radius:50%;background:var(--verde-800);color:var(--amarelo);display:grid;place-items:center;flex:none}
.cp{display:flex;align-items:center;gap:8px;background:#fff;border:2px dashed var(--verde-600);border-radius:14px;padding:10px 12px;font:700 17px/1 var(--fonte)}
.cp span{flex:1}
"""
S["app/a15-indique"] = page("A15 · Indique e ganhe (app)", sb() + """
<div class="a-hd"><a style="font-weight:700;text-decoration:none;font-size:17px">← Conta</a></div>
<div class="ix">
  <div class="gift">🎁</div>
  <h1>Indique um fazendeiro e ganhe 1 mês de Pro</h1>
  <p class="s">Se ele assinar, o mês entra na sua conta. Sem limite de indicações.</p>
  <div class="ps"><div><b>1</b>Você manda o link no WhatsApp</div><div><b>2</b>Ele testa 7 dias grátis</div><div><b>3</b>Ele assina e você ganha 1 mês</div></div>
  <div class="cp"><span>radarboi.com/i/gabriel</span><span class="rb-tag rb-tag--exemplo">exemplo</span></div>
  <div style="margin-top:14px;font-size:16px"><span class="muted">Indicados: 2 · assinaram: 1 ·</span> <b class="g">+1 mês ganho</b> <span class="rb-tag rb-tag--exemplo">exemplo</span></div>
</div>
<div style="padding:10px 18px 30px"><a class="rb-btn rb-btn--wa rb-btn--full" style="font-size:20px">Mandar no WhatsApp</a></div>
""", A15_CSS, nota="Botão abre o WhatsApp com a mensagem pronta (wa.me/?text=). Conta grátis e paga veem a mesma tela.")

# =====================================================================
# WhatsApp · resumo de segunda, versão grátis
# =====================================================================
s1, s2, s3 = SEM[:3]
S["whatsapp/z03-resumo-gratis"] = page("Z03 · WhatsApp: resumo de segunda (Radar Grátis)", WAH + f"""
<div class="cv">
  <span class="dia">SEGUNDA</span>
  <div class="m"><b>Bom dia, Gabriel! ☀️ Resumo da semana (grátis)</b><br>Fêmeas até 250 km de Barro Alto. Leilões de 02 a 06/11:
    <table class="num"><tr><td>🥇 {s1['cidade']}</td><td>R$ {s1['arr']}/@</td></tr><tr><td>🥈 {s2['cidade']}</td><td>R$ {s2['arr']}/@</td></tr><tr><td>🥉 {s3['cidade']}</td><td>R$ {s3['arr']}/@</td></tr></table>
    🔒 Leilão, lote, vídeo e margem: só no Pro.
    <div style="margin-top:8px;padding:8px 10px;border-left:4px solid var(--aovivo);background:#fff4f3;border-radius:6px">🔴 <b>Você perdeu:</b> quarta 28/10, ~21h25, entrou em Uruaçu um lote de <b>7 bezerras brancas</b> a <b>R$ 333/@</b>, <b>24% abaixo da Scot</b>. Os assinantes receberam o alerta na hora.</div>
    <div style="margin-top:8px">🎁 Indique 1 fazendeiro que assine e ganhe 1 mês de Pro.</div>
    <div class="h">06:00</div>
    <div class="bt"><span>⭐ Voltar pro Pro</span><span>🎁 Indicar</span></div></div>
  <div class="m eu">qual leilão de uruaçu?<div class="h">07:05 ✓✓</div></div>
  <div class="m">Fica no Pro. Seus filtros estão guardados: toque em <b>Voltar pro Pro</b>. 👍<div class="h">07:05</div></div>
</div>""" + WAIN, WA_CSS, nota="Template utilidade. Ranking = 3 primeiras cidades, só R$/@ (fêmeas, todas as eras e cores, raio da fazenda). Sem nome do leilão, sem link do lote, sem margem. Bloco 'você perdeu' = melhor lote real da semana no filtro salvo da conta. Horário ~21h25 = início da live (20:19) + minuto 1:05:30. Lote trocado em 05/11: o de 04/11 (qP6lHvAU3Bw 1:43:20) foi reprovado na cor.")

if __name__ == "__main__":
    for k, v in S.items():
        p = D / (k + ".html"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(v); print(p.relative_to(D))
    print("RK", [(x["cidade"], x["arr"]) for x in RK[:3]], "SEM", [(x["cidade"], x["arr"]) for x in SEM[:3]], "cab", CAB_TOT)
