#!/usr/bin/env python3
"""Gera as telas estáticas do app (docs/design/app/*.html) e do WhatsApp (docs/design/whatsapp/*.html).
Dados: data.json (26/10 a 04/11), fazenda Barro Alto/GO, filtro fêmeas 6–8@, 100% brancas, 250 km, venda 15@.
Rodar: python3 scripts/gen_app.py && python3 scripts/shots.py a"""
import pathlib
D = pathlib.Path(__file__).resolve().parent.parent / "docs" / "design"

def page(title, body, extra_css="", escuro=False, nota=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Radar Boi</title>
<link rel="stylesheet" href="../rb.css">
<style>{extra_css}</style></head>
<body class="app-pg">
<!-- {title}. {nota} -->
<div class="phone{' escuro' if escuro else ''}">
{body}
<span class="home-ind"></span>
</div>
</body></html>"""

def sb(claro=False, hora="9:41"):
    return f'<div class="sb{" claro" if claro else ""}"><span>{hora}</span><span class="di"></span><span>▂▄▆ 4G ▭</span></div>'

def tab(on):
    itens = [("inicio", "⌂", "Início"), ("lotes", "🐂", "Lotes"), ("agenda", "📅", "Agenda"), ("alertas", "🔔", "Alertas"), ("conta", "👤", "Conta")]
    out = []
    for k, i, t in itens:
        bol = '<span class="bol">2</span>' if k == "alertas" and on != "alertas" else ""
        out.append(f'<a class="{"is-on" if k == on else ""}"><span class="i">{i}</span>{t}{bol}</a>')
    return '<nav class="rb-tabbar">' + "".join(out) + "</nav>"

def lote_card(img, tit, cab, arroba, scot, meta, minuto, margem, salvo=False):
    return f"""<article class="rb-lote">
  <div class="foto"><img src="../img/{img}_1.jpg" alt=""><span class="rb-selo rb-selo--ok">100% brancas</span><span class="min">▶ {minuto}</span></div>
  <div class="corpo">
    <div class="tit"><h3>{tit}</h3><span class="cab num">R$ {cab}<small>/cab</small></span></div>
    <div class="linha"><span class="arroba num">R$ {arroba}/@</span><span class="rb-scot rb-scot--barato">{scot}% abaixo da Scot</span></div>
    <div class="meta num">{meta}</div>
    <div class="linha"><span class="rb-tag rb-tag--margem num">Margem até 15@: R$ {margem}</span></div>
    <div class="acoes"><a class="rb-btn rb-btn--pri">▶ Ver no vídeo</a><a class="rb-btn rb-btn--sec">{'★ Salvo' if salvo else '☆ Salvar'}</a></div>
  </div>
</article>"""

ONB_CSS = """
.onb{flex:1;display:flex;flex-direction:column;padding:4px 20px 34px}
.prog{display:flex;gap:6px;margin:6px 0 22px}.prog i{flex:1;height:6px;border-radius:3px;background:#dcd8cc}.prog i.on{background:var(--verde-600)}
.onb .passo{font:800 14px/1 var(--fonte);color:var(--verde-600);text-transform:uppercase;letter-spacing:.8px}
.onb h1{font:800 30px/1.12 var(--fonte);color:var(--verde-900);margin:8px 0 8px;letter-spacing:-.5px}
.onb p.d{font-size:18px;color:var(--cinza);margin:0 0 20px}
.onb .fim{margin-top:auto}
.onb .sub-t{font:800 17px/1 var(--fonte);margin:18px 0 10px}
.onb .rb-opcao{margin-bottom:10px}
.topo{display:flex;justify-content:space-between;align-items:center;padding:0 20px}
.topo a{font-weight:700;text-decoration:none;font-size:17px;min-height:44px;display:flex;align-items:center}
"""

def onb(n, corpo, cta="Continuar"):
    prog = "".join(f'<i class="{"on" if k <= n else ""}"></i>' for k in (1, 2, 3))
    return f"""{sb()}<div class="topo"><a>{'← Voltar' if n > 1 else ''}</a><a>Pular</a></div>
<div class="onb"><div class="prog">{prog}</div><div class="passo">Passo {n} de 3</div>{corpo}
<div class="fim"><a class="rb-btn rb-btn--pri rb-btn--full" style="font-size:20px">{cta}</a></div></div>"""

S = {}

# ---------- A01 splash ----------
S["app/a01-splash"] = page("A01 · Splash", sb(claro=True) + """
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;text-align:center;padding:0 36px;position:relative">
  <div style="position:absolute;width:520px;height:520px;border-radius:50%;border:2px solid #ffffff14;box-shadow:0 0 0 60px #ffffff08,0 0 0 120px #ffffff05;top:50%;left:50%;transform:translate(-50%,-62%)"></div>
  <div style="width:112px;height:112px;border-radius:30px;background:var(--amarelo);color:var(--verde-800);display:grid;place-items:center;font-size:80px;line-height:1;box-shadow:0 14px 30px #0004;position:relative;overflow:hidden"><img src="../marca/app-amarelo.svg" alt="Radar Boi" style="width:100%;height:100%;display:block;border-radius:inherit"></div>
  <div style="font:800 40px/1 var(--fonte);margin-top:24px;letter-spacing:-1px;position:relative">Radar Boi</div>
  <div style="font-size:19px;color:#d2e4d6;margin-top:12px;line-height:1.4;position:relative">O leilão mais barato<br>perto da sua fazenda.</div>
</div>
<div style="padding:0 30px 60px;color:#cfe3d4;text-align:center;font-size:16px">
  <div style="height:6px;border-radius:3px;background:#ffffff22;overflow:hidden;margin-bottom:14px"><div style="width:62%;height:100%;background:var(--amarelo)"></div></div>
  Buscando os leilões da semana…<br><span style="font-size:14px;opacity:.8">Sem sinal? Abre a última versão salva (05/11).</span>
</div>""", escuro=True, nota="Mostra no máximo 2 s. Se não tiver internet, abre a última versão salva e mostra a faixa 'sem sinal'.")

# ---------- A02 onboarding 1 ----------
S["app/a02-onb-fazenda"] = page("A02 · Onboarding 1: fazenda", onb(1, """
<h1>Onde fica sua fazenda?</h1><p class="d">A gente mede a distância de cada leilão a partir dela.</p>
<a class="rb-btn rb-btn--pri rb-btn--full" style="background:var(--verde-800);font-size:19px">📍 Usar minha localização</a>
<div style="text-align:center;color:var(--cinza);margin:14px 0;font-weight:600">ou digite a cidade</div>
<div class="rb-campo"><div class="ent is-foco">🔎 Barro Al|</div></div>
<div style="background:#fff;border:1px solid var(--areia);border-radius:14px;margin-top:8px;overflow:hidden">
  <div style="padding:16px;font:700 19px/1.2 var(--fonte);background:var(--verde-50);display:flex;justify-content:space-between">Barro Alto/GO <span style="color:var(--verde-600)">✓</span></div>
  <div style="padding:16px;font:600 18px/1.2 var(--fonte);border-top:1px solid #eee;color:var(--cinza)">Barro Alto/BA</div>
</div>
<div class="rb-nota" style="margin-top:16px">24 leilões cobertos até 250 km de Barro Alto/GO.</div>
"""), ONB_CSS, nota="Pede permissão de localização só ao tocar no botão. Busca de cidade com autocompletar (IBGE). Salva lat/lon da cidade.")

# ---------- A03 onboarding 2 ----------
S["app/a03-onb-compra"] = page("A03 · Onboarding 2: o que compra", onb(2, """
<h1>O que você compra?</h1><p class="d" style="margin-bottom:6px">Pode marcar mais de um.</p>
<div class="sub-t">Sexo</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div class="rb-opcao is-on" style="margin:0"><span class="box"></span>Fêmeas</div><div class="rb-opcao" style="margin:0"><span class="box"></span>Machos</div></div>
<div class="sub-t">Era</div>
<div class="rb-opcao"><span class="box"></span><div>Até 9 meses<small>desmama</small></div></div>
<div class="rb-opcao is-on"><span class="box"></span><div>10 a 15 meses<small>bezerra de ano</small></div></div>
<div class="rb-opcao"><span class="box"></span><div>16 a 24 meses<small>novilha, garrote</small></div></div>
<div class="sub-t">Peso estimado</div>
<div class="rb-chips"><span class="rb-chip">até 6@</span><span class="rb-chip is-on">6 a 8@</span><span class="rb-chip">8 a 10@</span><span class="rb-chip">10@+</span></div>
"""), ONB_CSS + ".onb .rb-opcao{min-height:60px}", nota="Padrão: Fêmeas, 10–15 m, 6–8@. Peso é estimado pela era (curva Scot GO).")

# ---------- A04 onboarding 3 ----------
S["app/a04-onb-raio-cor"] = page("A04 · Onboarding 3: raio, cor e aviso", onb(3, """
<h1>Até onde e de que cor?</h1>
<div class="sub-t" style="margin-top:6px">Raio de busca</div>
<div style="display:flex;align-items:baseline;gap:10px"><span style="font:800 40px/1 var(--fonte);color:var(--verde-900)" class="num">250 km</span><span class="muted">24 leilões</span></div>
<div class="rb-slider"><i style="width:44%"></i><b style="left:44%"></b></div>
<div style="display:flex;justify-content:space-between;color:var(--cinza);font-size:14px;font-weight:600"><span>50 km</span><span>500 km</span></div>
<div style="background:#fff;border:1px solid var(--areia);border-radius:14px;padding:4px 16px;margin-top:20px">
  <div style="display:flex;align-items:center;gap:12px;padding:14px 0;border-bottom:1px solid #eee"><div style="flex:1"><b style="font-size:18px">Só lotes 100% brancos</b><div class="muted small">Conferimos 3 imagens de cada lote</div></div><span class="rb-toggle is-on"></span></div>
  <div style="display:flex;align-items:center;gap:12px;padding:14px 0"><div style="flex:1"><b style="font-size:18px">Avisar no WhatsApp</b><div class="muted small">Resumo de segunda e "entrando agora"</div></div><span class="rb-toggle is-on"></span></div>
</div>
<div style="background:var(--verde-800);color:#fff;border-radius:16px;padding:16px;margin-top:16px;display:flex;gap:14px;align-items:center">
  <span style="font:800 36px/1 var(--fonte);color:var(--amarelo)" class="num">11</span><span style="font-size:16px;line-height:1.35">lotes serviram pra você nos últimos 10 dias. O mais barato: <b>Uruaçu, R$ 318/@</b>.</span>
</div>
""", "Ver meu radar"), ONB_CSS, nota="O quadro verde recalcula ao mexer no raio/cor. Sem o filtro de cor seriam 269 lotes.")

# ---------- A05 home ----------
HOME_CSS = """
.hi{font:800 26px/1.15 var(--fonte);color:var(--verde-900)}.hi small{display:block;font:600 15px/1.3 var(--fonte);color:var(--cinza)}
.dest{background:var(--verde-800);color:#fff;border-radius:18px;padding:16px 18px;margin-top:12px}
.dest .r{font:600 14px/1.2 var(--fonte);color:#cfe3d4;text-transform:uppercase;letter-spacing:.6px}
.dest .v{font:800 44px/1 var(--fonte);color:var(--amarelo);margin:8px 0 4px;letter-spacing:-1px}.dest .v small{font-size:20px}
.dest .l{font-size:17px}
.dest .s{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.mini{background:#fff;border:1px solid var(--areia);border-radius:16px;overflow:hidden}
.mini .it{display:grid;grid-template-columns:34px 1fr auto;gap:10px;align-items:center;padding:12px 14px;border-top:1px solid #eee}
.mini .it:first-child{border-top:0}
.mini .p{font:800 17px/1 var(--fonte);color:var(--verde-800)}
.mini b{font-size:17px}.mini small{display:block;color:var(--cinza);font-size:14px}
.mini .v{text-align:right;font:800 19px/1.1 var(--fonte)}.mini .v small{font-size:12px;font-weight:800}
"""
S["app/a05-home"] = page("A05 · Início", sb() + """
<div class="a-hd"><div class="hi">Bom dia, Gabriel<small>📍 Barro Alto/GO · até 250 km</small></div><span class="ic">🔔<span class="bol">2</span></span></div>
<div class="a-body">
  <div class="rb-aovivo"><span class="rb-tag rb-tag--aovivo">AO VIVO</span><div class="t"><b>WM Uruaçu · lote 10</b>7 bezerras · R$ 333/@</div><span style="font-size:26px">▶</span></div>
  <div style="margin-top:4px;text-align:right"><span class="rb-tag rb-tag--exemplo">exemplo · lote real de 28/10</span></div>
  <div class="dest">
    <div class="r">Mais barato · 26/10 a 04/11</div>
    <div class="v num">R$ 318<small>/@</small></div>
    <div class="l">Uruaçu · WM Leilões · 55 km · qua 28/10</div>
    <div class="s"><span class="rb-scot rb-scot--barato">27% abaixo da Scot</span><span class="rb-tag" style="background:#ffffff1f;color:#fff">14 cab. · 4 lotes</span></div>
  </div>
  <div class="a-sec">Ranking da semana <a>Ver tudo</a></div>
  <div class="mini num">
    <div class="it"><span class="p">2º</span><div><b>Uruaçu</b><small>55 km · qua 04/11 · 7 cab.</small></div><div class="v g">R$ 331/@<br><small>24% abaixo</small></div></div>
    <div class="it"><span class="p">3º</span><div><b>Niquelândia</b><small>73 km · ter 03/11 · 9 cab.</small></div><div class="v g">R$ 339/@<br><small>23% abaixo</small></div></div>
    <div class="it"><span class="p">4º</span><div><b>Porangatu</b><small>172 km · seg 26/10 · 160 cab.</small></div><div class="v r">R$ 457/@<br><small>4% acima</small></div></div>
  </div>
  <div style="display:flex;justify-content:space-between;margin-top:10px;font-size:14px;color:var(--cinza);font-weight:600"><span>Scot GO bezerra 12 m: R$ 438/@</span><span>Margem média 15@: R$ 2.416</span></div>
</div>""" + tab("inicio"), HOME_CSS, nota="Ordem: faixa ao vivo (só quando tem leilão do raio no ar), destaque do mais barato, ranking resumido. Pull-to-refresh. Offline: mostra a última versão com a faixa 'sem sinal'.")

# ---------- A06 feed de lotes ----------
FEED_CSS = """
.seg2{display:flex;background:#e9e6dc;border-radius:12px;padding:4px;margin:0 16px 10px}
.seg2 span{flex:1;text-align:center;padding:10px;border-radius:9px;font:700 16px/1 var(--fonte);color:var(--cinza)}
.seg2 .on{background:#fff;color:var(--verde-900);box-shadow:0 1px 3px #0002}
.chs{display:flex;gap:8px;overflow:hidden;padding:0 16px 12px;white-space:nowrap}
.feed{padding:0 16px;display:flex;flex-direction:column;gap:12px}
.cont{font:600 15px/1 var(--fonte);color:var(--cinza);padding:0 16px 10px;display:flex;justify-content:space-between}
"""
S["app/a06-lotes"] = page("A06 · Feed de lotes", sb() + """
<div class="a-hd"><h1>Lotes</h1><span class="ic">⚙︎</span></div>
<div class="seg2"><span class="on">Todos (11)</span><span>★ Salvos (2)</span></div>
<div class="chs"><span class="rb-chip is-on">Fêmeas</span><span class="rb-chip is-on">6–8@</span><span class="rb-chip is-on">Brancas</span><span class="rb-chip is-on">250 km</span></div>
<div class="cont"><span>Mais barato por @ primeiro</span><span>↕ Ordenar</span></div>
<div class="a-body pad0"><div class="feed">""" +
    lote_card("rmlJbmSu1i4_26", "3 bezerras · 12 m", "1.920", "274", 37, "Uruaçu · 55 km · qua 28/10 · ~210 kg · R$ 9,14/kg", "2:55:10", "3.551", True) +
    lote_card("faPKYrIsWuU_4", "1 bezerra · 8 m", "1.690", "282", 36, "Niquelândia · 73 km · ter 03/11 · ~180 kg", "0:33:10", "3.781") +
    """</div></div>""" + tab("lotes"), FEED_CSS, nota="CardLote. Lista infinita (20 por página). Foto = 1ª imagem da conferência; toque abre o detalhe (A07). Chips abrem folha de filtros. Imagens com lazy-load e versão leve para 3G.")

# ---------- A07 detalhe ----------
DET_CSS = """
.fot{position:relative;margin-top:-47px;height:250px;background:#000}
.fot img{width:100%;height:100%;object-fit:cover;display:block}
.fot .bk{position:absolute;top:56px;left:14px;width:44px;height:44px;border-radius:50%;background:#000000a0;color:#fff;display:grid;place-items:center;font-size:22px}
.fot .sv{position:absolute;top:56px;right:14px;width:44px;height:44px;border-radius:50%;background:#000000a0;color:var(--amarelo);display:grid;place-items:center;font-size:22px}
.fot .rb-selo{position:absolute;left:14px;bottom:14px;font-size:15px;padding:7px 11px}
.fot .dots{position:absolute;right:14px;bottom:18px;display:flex;gap:6px}.fot .dots i{width:8px;height:8px;border-radius:50%;background:#ffffff80}.fot .dots i.on{background:#fff}
.det{padding:14px 18px 0}
.det h1{font:800 26px/1.15 var(--fonte)}.det .s{color:var(--cinza);font-size:16px;margin-top:4px}
.det .big{display:flex;align-items:center;flex-wrap:wrap;gap:6px 10px;margin:14px 0 4px}.det .big b{white-space:nowrap}.det .big b{font:800 40px/1 var(--fonte);letter-spacing:-1px}.det .big b small{font-size:17px;color:var(--cinza)}
.g4{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.g4 div{background:#fff;border:1px solid var(--areia);border-radius:12px;padding:10px 12px}
.g4 small{display:block;color:var(--cinza);font:600 13px/1.2 var(--fonte)}.g4 b{font:800 20px/1.2 var(--fonte)}
.bar{margin-top:auto;background:#fff;border-top:1px solid var(--areia);padding:12px 16px 30px;display:flex;gap:10px}
.bar .rb-btn--pri{flex:1;font-size:19px}
"""
S["app/a07-lote"] = page("A07 · Detalhe do lote", sb(claro=True) + """
<div class="fot"><img src="../img/rmlJbmSu1i4_10_2.jpg" alt=""><span class="bk">←</span><span class="sv">☆</span><span class="rb-selo rb-selo--ok">100% brancas</span><span class="dots"><i></i><i class="on"></i><i></i></span></div>
<div class="det">
  <h1>7 bezerras · 12 meses</h1><div class="s">WM Leilões · Uruaçu · 55 km · qua 28/10</div>
  <div class="big num"><b class="g">R$ 333<small>/@ est.</small></b><span class="rb-scot rb-scot--barato">24% abaixo da Scot</span></div>
  <div class="muted small">Scot GO bezerra 12 m: R$ 438/@</div>
  <div class="g4 num">
    <div><small>Último lance</small><b>R$ 2.330/cab</b></div>
    <div><small>Lote inteiro</small><b>R$ 16.310</b></div>
    <div><small>Peso estimado</small><b>~210 kg · 7@</b></div>
    <div><small>Margem até 15@</small><b class="g">R$ 3.141</b></div>
  </div>
  <div class="rb-nota" style="margin-top:12px">Preço = último lance na tela. Peso pela era. <a>Reportar erro</a></div>
</div>
<div class="bar"><a class="rb-btn rb-btn--pri">▶ Ver no minuto 1:05:30</a><a class="rb-btn rb-btn--sec" style="width:56px;padding:0;min-height:56px">📤</a></div>
""", DET_CSS, nota="Foto: carrossel das 3 imagens da conferência (deslizar). Botão principal fixo embaixo abre o YouTube em ?t=3930. 📤 manda o lote no WhatsApp. Sem tab bar nesta tela (é um nível abaixo).")

# ---------- A08 agenda ----------
AG_CSS = """
.dias{display:flex;gap:8px;padding:0 16px 12px}
.dias span{flex:1;text-align:center;border-radius:14px;padding:10px 0;background:#fff;border:1px solid var(--areia);font:800 20px/1 var(--fonte)}
.dias span small{display:block;font-size:12px;color:var(--cinza);margin-bottom:4px}
.dias span.on{background:var(--verde-800);color:#fff;border-color:var(--verde-800)}.dias span.on small{color:var(--amarelo)}
.ev{background:#fff;border:1px solid var(--areia);border-radius:16px;padding:14px 16px;margin-bottom:10px}
.ev.is-av{border:2px solid var(--verde-600)}
.ev .t{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.ev b{font:800 19px/1.2 var(--fonte)}.ev small{display:block;color:var(--cinza);font-size:14px;margin-top:2px}
.ev .u{display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding-top:10px;border-top:1px solid #eee;font-size:15px;color:var(--cinza)}
.ev .u b{font-size:18px}
"""
S["app/a08-agenda"] = page("A08 · Agenda", sb() + """
<div class="a-hd"><h1>Agenda</h1><span class="muted" style="font-weight:700">09 a 13/11</span></div>
<div class="dias num"><span><small>SEG</small>09</span><span><small>TER</small>10</span><span class="on"><small>QUA</small>11</span><span><small>QUI</small>12</span><span><small>SEX</small>13</span></div>
<div class="a-body">
  <div style="font:700 15px/1 var(--fonte);color:var(--cinza);margin:2px 0 10px">Quarta, 11/11 · 4 leilões no raio</div>
  <div class="ev is-av"><div class="t"><div><b>Uruaçu</b><small>WM Leilões · 55 km · horário a confirmar</small></div><span class="rb-toggle is-on"></span></div>
    <div class="u num"><span>Última (04/11) <span class="rb-selo rb-selo--ok" style="font-size:12px;padding:3px 7px">brancas</span></span><b class="g">R$ 331/@</b></div></div>
  <div class="ev"><div class="t"><div><b>Corumbá de Goiás</b><small>Corumbá Leilões · 107 km</small></div><span class="rb-toggle"></span></div>
    <div class="u num"><span>Última (04/11) <span class="rb-selo rb-selo--nc" style="font-size:12px;padding:3px 7px">cor não conf.</span></span><b>R$ 397/@</b></div></div>
  <div class="ev"><div class="t"><div><b>Trombas</b><small>Trombas Leilões · 163 km</small></div><span class="rb-toggle"></span></div>
    <div class="u num"><span>Última (28/10) <span class="rb-selo rb-selo--nc" style="font-size:12px;padding:3px 7px">cor não conf.</span></span><b class="g">R$ 355/@</b></div></div>
  <div class="ev"><div class="t"><div><b>Porangatu</b><small>Sindicato Rural · 172 km</small></div><span class="rb-toggle"></span></div>
    <div class="u num"><span>Última (04/11) <span class="rb-selo rb-selo--nc" style="font-size:12px;padding:3px 7px">cor não conf.</span></span><b>R$ 399/@</b></div></div>
</div>""" + tab("agenda"), AG_CSS, nota="Toggle = avisar quando o catálogo sair e quando entrar lote do filtro. Previsão pelos leilões semanais; horário só quando a leiloeira divulga.")

# ---------- A09 alertas ----------
AL_CSS = """
.big-al{background:#fff;border-radius:18px;overflow:hidden;border:2px solid var(--aovivo);box-shadow:var(--sombra)}
.big-al img{width:100%;height:118px;object-fit:cover;display:block}
.big-al .c{padding:12px 14px 14px}
.big-al h3{font:800 20px/1.2 var(--fonte)}
.big-al .p{display:flex;align-items:center;gap:8px;margin:8px 0 12px}.big-al .p b{font:800 26px/1 var(--fonte)}
.al{display:grid;grid-template-columns:44px 1fr;gap:12px;padding:12px 0;border-top:1px solid #e4e0d4}
.al .i{width:44px;height:44px;border-radius:12px;background:#fff;border:1px solid var(--areia);display:grid;place-items:center;font-size:20px}
.al b{font-size:16px;display:block}.al small{color:var(--cinza);font-size:14px}
"""
S["app/a09-alertas"] = page("A09 · Alertas (entrando agora)", sb() + """
<div class="a-hd"><h1>Alertas</h1><a class="rb-btn rb-btn--txt" style="font-size:16px;min-height:44px">Meus avisos (3)</a></div>
<div class="a-body">
  <div class="big-al">
    <img src="../img/rmlJbmSu1i4_10_1.jpg" alt="">
    <div class="c"><span class="rb-tag rb-tag--aovivo">ENTRANDO AGORA</span>
      <h3 style="margin-top:8px">7 bezerras brancas · 12 m</h3><div class="muted">WM Uruaçu · 55 km · ~210 kg</div>
      <div class="p num"><b>R$ 2.330</b><span class="rb-scot rb-scot--barato">R$ 333/@ · 24% abaixo</span></div>
      <a class="rb-btn rb-btn--pri rb-btn--full" style="background:var(--aovivo)">▶ Assistir agora</a>
    </div>
  </div>
  <div style="margin:6px 0 4px;text-align:right"><span class="rb-tag rb-tag--exemplo">exemplo · lote real de 28/10</span></div>
  <div class="a-sec" style="margin-top:8px">Antes</div>
  <div class="al"><span class="i">🔴</span><div><b>7 novilhas · 15 m · R$ 2.650</b><small>WM Uruaçu · qua 04/11 · R$ 331/@ · 24% abaixo</small></div></div>
  <div class="al"><span class="i">🔴</span><div><b>7 bezerras · 12 m · R$ 2.415</b><small>JPS Niquelândia · ter 03/11 · R$ 345/@ · 21% abaixo</small></div></div>
  <div class="al"><span class="i">📅</span><div><b>Resumo da semana chegou</b><small>seg 02/11, 6h · no WhatsApp</small></div></div>
</div>""" + tab("alertas"), AL_CSS, nota="Alerta ao vivo fica no topo enquanto o lote está na pista (até 10 min). Depois vira item da lista 'Antes'. Toque abre a transmissão no minuto atual.")

# ---------- A10 notificação ----------
NOT_CSS = """
.lock{flex:1;background:linear-gradient(180deg,#2c5a37 0%,#163a20 100%);color:#fff;display:flex;flex-direction:column;align-items:center;padding:0 12px;margin-top:-47px;padding-top:47px}
.lock .d{font:600 19px/1 var(--fonte);margin-top:30px;opacity:.9}
.lock .h{font:300 92px/1 var(--fonte);letter-spacing:-2px;margin-top:4px}
.ntf{width:100%;background:#f5f5f2ee;color:var(--tinta);border-radius:22px;padding:14px;margin-top:34px;box-shadow:0 10px 30px #0004}
.ntf .t{display:flex;align-items:center;gap:8px;font:600 14px/1 var(--fonte);color:#555}
.ntf .t i{font-style:normal;width:24px;height:24px;border-radius:6px;background:var(--verde-800);color:var(--amarelo);display:grid;place-items:center;font-size:16px}
.ntf .t span{margin-left:auto}
.ntf b{display:block;font-size:17px;margin-top:8px}.ntf p{margin:3px 0 0;font-size:16px;line-height:1.35}
.ntf img{width:100%;height:96px;object-fit:cover;border-radius:12px;margin-top:10px;display:block}
.ntf .ac{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.ntf .ac span{background:#fff;border-radius:12px;text-align:center;padding:12px;font-weight:700;color:var(--verde-800)}
.ntf2{width:100%;background:#f5f5f2cc;color:var(--tinta);border-radius:22px;padding:12px 14px;margin-top:10px}
"""
S["app/a10-notificacao"] = page("A10 · Notificação 'entrando agora'", sb(claro=True, hora="") + """
<div class="lock"><div class="d">quarta-feira, 28 de outubro</div><div class="h">20:41</div>
  <div class="ntf"><div class="t"><i style="overflow:hidden"><img src="../marca/app-verde.svg" alt="Radar Boi" style="width:100%;height:100%;display:block;border-radius:inherit"></i>RADAR BOI<span>agora</span></div>
    <b>🔴 Entrando agora · WM Uruaçu</b>
    <p>7 bezerras brancas · 12 m · lance R$ 2.330 = R$ 333/@ (24% abaixo da Scot)</p>
    <img src="../img/rmlJbmSu1i4_10_1.jpg" alt="">
    <div class="ac"><span>▶ Assistir</span><span>☆ Salvar</span></div>
  </div>
  <div class="ntf2"><div class="t" style="display:flex;gap:8px;font:600 14px/1 var(--fonte);color:#555"><span style="width:24px;height:24px;border-radius:6px;background:var(--verde-800);color:var(--amarelo);display:grid;place-items:center;overflow:hidden"><img src="../marca/app-verde.svg" alt="Radar Boi" style="width:100%;height:100%;display:block;border-radius:inherit"></span>RADAR BOI<span style="margin-left:auto">19:58</span></div><b style="display:block;margin-top:6px">Catálogo saiu · WM Uruaçu hoje</b><span style="font-size:15px">41 lotes. A gente avisa quando a bezerra branca entrar.</span></div>
  <div style="margin-top:auto;margin-bottom:46px"><span class="rb-tag rb-tag--exemplo" style="background:#ffffff20;color:#ffe48a;border-color:#ffe48a;white-space:normal;text-align:center">exemplo · horário ilustrativo · lote real de 28/10</span></div>
</div>""", NOT_CSS, escuro=True, nota="Push rico (imagem + 2 ações). Mesmo texto do WhatsApp. Ação Assistir abre o vídeo ao vivo; Salvar não abre o app.")

# ---------- A11 salvos ----------
S["app/a11-salvos"] = page("A11 · Salvos", sb() + """
<div class="a-hd"><h1>Lotes</h1><span class="ic">⚙︎</span></div>
<div class="seg2"><span>Todos (11)</span><span class="on">★ Salvos (2)</span></div>
<div class="cont" style="padding-top:4px"><span>Ficam aqui mesmo depois do leilão</span></div>
<div class="a-body pad0"><div class="feed">""" +
    lote_card("rmlJbmSu1i4_26", "3 bezerras · 12 m", "1.920", "274", 37, "Uruaçu · 55 km · qua 28/10 · ~210 kg", "2:55:10", "3.551", True) +
    lote_card("rmlJbmSu1i4_10", "7 bezerras · 12 m", "2.330", "333", 24, "Uruaçu · 55 km · qua 28/10 · ~210 kg", "1:05:30", "3.141", True) +
    """</div></div>""" + tab("lotes"), FEED_CSS, nota="Salvos = aba dentro de Lotes. Lote salvo serve de referência de preço e para 'avisar parecido'. Vazio: ver componentes (EstadoVazio).")

# ---------- A12 perfil ----------
PF_CSS = """
.pf{display:flex;gap:14px;align-items:center;margin-bottom:10px}
.pf .av{width:60px;height:60px;border-radius:50%;background:var(--amarelo);display:grid;place-items:center;font:800 26px/1 var(--fonte);color:var(--verde-900)}
.pf b{font-size:22px;display:block}.pf small{color:var(--cinza);font-size:15px}
.pl{background:var(--amarelo);border-radius:16px;padding:14px 16px;display:flex;justify-content:space-between;align-items:center}
.pl b{font-size:19px;display:block}.pl span{font-size:15px;color:#4a3a00}
.pl .d{font:800 34px/1 var(--fonte);color:var(--verde-900);text-align:center}.pl .d small{display:block;font-size:12px}
.gr{background:#fff;border:1px solid var(--areia);border-radius:16px;margin-top:10px}
.gr .l{display:flex;align-items:center;gap:12px;padding:0 16px;min-height:48px;border-top:1px solid #eee;font-size:17px}
.gr .l:first-child{border-top:0}
.gr .l i{font-style:normal;width:26px;text-align:center}
.legal{text-align:center;color:var(--cinza);font-size:13px;line-height:1.4;margin:10px 8px 4px}
.gr .l span{flex:1}.gr .l em{font-style:normal;color:var(--cinza);font-size:15px}
"""
S["app/a12-conta"] = page("A12 · Conta, fazenda e plano", sb() + """
<div class="a-hd"><h1>Conta</h1></div>
<div class="a-body">
  <div class="pf"><span class="av">G</span><div><b>Gabriel</b><small>(62) 9 ••••-4567 <span class="rb-tag rb-tag--exemplo">exemplo</span></small></div></div>
  <div class="pl"><div><b>Teste grátis do Pro</b><span>Sem cartão. Escolha o plano até 11/11.</span></div><div class="d num">6<small>dias</small></div></div>
  <div class="gr">
    <div class="l"><i>📍</i><span>Fazenda</span><em>Barro Alto/GO ›</em></div>
    <div class="l"><i>🐂</i><span>O que compro</span><em>Fêmeas 6–8@ ›</em></div>
    <div class="l"><i>🛣️</i><span>Raio</span><em>250 km ›</em></div>
    <div class="l"><i>✓</i><span>Só 100% brancas</span><span class="rb-toggle is-on" style="flex:none"></span></div>
    <div class="l"><i>💰</i><span>Meus custos</span><em>R$ 90/cab/mês ›</em></div>
  </div>
  <div class="gr">
    <div class="l"><i>⭐</i><span>Planos</span><em>Pro R$ 149/mês ›</em></div>
    <div class="l"><i>💬</i><span>Falar no WhatsApp</span><em>›</em></div>
    <div class="l"><i>📶</i><span>Modo sinal fraco</span><span class="rb-toggle is-on" style="flex:none"></span></div>
  </div>
  <p class="legal">Radar Boi é um produto da Starcore Produtos de Tecnologia Ltda, CNPJ 39.573.543/0001-33</p>
</div>""" + tab("conta"), PF_CSS, nota="'Modo sinal fraco': fotos menores, sem vídeo embutido, guarda o último ranking offline. 'Meus custos' em exemplo até o usuário preencher.")

# ---------- WhatsApp ----------
WA_CSS = """
.phone{background:var(--wa-bg)}
.wah{background:var(--wa);color:#fff;display:flex;align-items:center;gap:10px;padding:8px 12px 10px;margin-top:-47px;padding-top:55px}
.wah .av{width:40px;height:40px;border-radius:50%;background:var(--amarelo);color:var(--verde-800);display:grid;place-items:center;font-size:26px}
.wah b{font-size:17px;display:block}.wah small{font-size:13px;opacity:.85}
.cv{flex:1;padding:10px 10px 0;display:flex;flex-direction:column;gap:8px;overflow:hidden;background:var(--wa-bg)}
.m{max-width:92%;background:#fff;border-radius:10px;padding:8px 10px;font-size:16px;line-height:1.38;box-shadow:0 1px 1px #0001}
.m.eu{align-self:flex-end;background:var(--wa-eu)}
.m .h{font-size:11px;color:#888;text-align:right;margin-top:2px}
.m img{width:100%;border-radius:8px;display:block;margin-bottom:6px}
.m table{width:100%;border-collapse:collapse;font-size:15px;margin:6px 0}.m td{padding:3px 0}.m td:last-child{text-align:right;font-weight:800}
.m .bt{display:flex;border-top:1px solid #eee;margin:8px -10px -8px}.m .bt span{flex:1;text-align:center;color:#027eb5;font-weight:600;padding:10px 0;font-size:15px}
.m .bt span+span{border-left:1px solid #eee}
.dia{align-self:center;background:#fff;border-radius:8px;padding:4px 10px;font-size:13px;color:#555;box-shadow:0 1px 1px #0001}
.in{background:#f0f0f0;padding:8px 10px 30px;display:flex;gap:8px;align-items:center}
.in span{flex:1;background:#fff;border-radius:20px;padding:10px 14px;color:#999}
.in i{font-style:normal;width:44px;height:44px;border-radius:50%;background:var(--wa);color:#fff;display:grid;place-items:center}
.al{border-left:4px solid var(--aovivo)}
"""
WAH = sb(claro=True) + '<div class="wah"><span>←</span><span class="av" style="overflow:hidden"><img src="../marca/icone-verde.svg" alt="Radar Boi" style="width:100%;height:100%;display:block;border-radius:inherit"></span><div><b>Radar Boi ✓</b><small>conta comercial</small></div></div>'
WAIN = '<div class="in"><span>Mensagem</span><i>🎤</i></div>'
S["whatsapp/z01-resumo-segunda"] = page("Z01 · WhatsApp: resumo de segunda", WAH + """
<div class="cv">
  <span class="dia">SEGUNDA</span>
  <div class="m"><b>Bom dia, Gabriel! ☀️ Resumo da semana</b><br>Bezerra/novilha <b>branca 6–8@</b>, até 250 km de Barro Alto. Leilões de 26/10 a 04/11:
    <table class="num"><tr><td>🥇 Uruaçu · 55 km · qua</td><td class="g">R$ 318/@</td></tr><tr><td>🥈 Niquelândia · 73 km · ter</td><td class="g">R$ 339/@</td></tr><tr><td>🥉 Porangatu · 172 km · seg</td><td class="r">R$ 457/@</td></tr><tr><td style="color:#666">Scot GO (bezerra 12 m)</td><td>R$ 438/@</td></tr></table>
    💰 Lote mais barato: <b>3 bezerras 12 m, R$ 1.920</b> em Uruaçu (R$ 274/@).<br>
    📅 Esta semana: ter Niquelândia · qua Uruaçu. Te aviso quando entrar bezerra branca.
    <div class="h">06:00</div>
    <div class="bt"><span>📊 Ver painel</span><span>📄 PDF</span><span>⚙️ Filtro</span></div></div>
  <div class="m eu">quanto tava a novilha em uruaçu quarta?<div class="h">07:12 ✓✓</div></div>
  <div class="m">Quarta 04/11 em Uruaçu, só um lote de novilha passou na cor: 7 novilhas 15 m a <b>R$ 2.650</b> (R$ 331/@), 100% brancas. O de 14 m (R$ 2.490) tinha animal vermelho e ficou fora.<br>▶ youtu.be/qP6lHvAU3Bw?t=5620<div class="h">07:12</div></div>
</div>""" + WAIN, WA_CSS, nota="Template aprovado na API do WhatsApp (categoria utilidade). Máx. 3 leilões + Scot + 1 lote destaque. Botões de resposta rápida. Data do envio: segunda 6h. Resposta livre do usuário é atendida pelo robô dentro da janela de 24 h.")

S["whatsapp/z02-alerta-entrando"] = page("Z02 · WhatsApp: alerta entrando agora", WAH + """
<div class="cv">
  <span class="dia">QUARTA</span>
  <div class="m">📋 <b>Catálogo saiu · WM Uruaçu, hoje</b><br>41 lotes. Te aviso quando a bezerra branca de 6–8@ entrar na pista.<div class="h">19:58</div></div>
  <div class="m al"><img src="../img/rmlJbmSu1i4_10_1.jpg" alt=""><b>🔴 Entrando agora · WM Uruaçu</b><br>7 bezerras <b>brancas</b> · 12 m · ~210 kg<br>Lance na tela: <b>R$ 2.330</b> = <b>R$ 333/@</b><br><span class="g"><b>24% abaixo da Scot</b></span> · margem até 15@: R$ 3.141
    <div class="h">20:41</div><div class="bt"><span>▶ Assistir agora</span><span>☆ Salvar</span></div></div>
  <div class="m eu">foi vendido por quanto?<div class="h">20:52 ✓✓</div></div>
  <div class="m">O último lance na tela foi R$ 2.330. A gente não confirma a venda: confira no vídeo no minuto 1:05:30. ▶<div class="h">20:52</div></div>
  <span class="rb-tag rb-tag--exemplo" style="align-self:center;white-space:normal;text-align:center;max-width:90%">exemplo · horários ilustrativos · lote real de 28/10</span>
</div>""" + WAIN, WA_CSS, nota="Alerta = template com imagem (1ª foto da conferência). Máx. 5 alertas/dia. Só sai se a cor estiver conferida; enquanto a conferência ao vivo não existir, sai com 'cor a conferir'.")

if __name__ == "__main__":
    for k, v in S.items():
        p = D / (k + ".html"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(v)
        print(p.relative_to(D))
