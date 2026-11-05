#!/usr/bin/env python3
"""Gera docs/design/index.html (galeria para aprovação). Rodar depois de shots.py."""
import pathlib
D = pathlib.Path(__file__).resolve().parent.parent / "docs" / "design"

GR = [
 ("Web · painel (A)", "web", [
  ("w01-landing", "Landing de vendas", "Planos e “testar 30 dias grátis”"),
  ("w02-entrar", "Entrar pelo WhatsApp", "Número + código de 6 dígitos"),
  ("w03-onboarding", "Onboarding", "Fazenda, o que compra, raio e cor"),
  ("w04-painel", "Ranking de leilões", "Painel principal, do mais barato ao mais caro"),
  ("w05-lotes", "Lotes com filtros", "16 lotes, um por um"),
  ("w06-lote", "Detalhe do lote", "Foto, preço, @, margem, vídeo no minuto"),
  ("w07-agenda", "Agenda", "Próximos leilões no raio, 09 a 13/11"),
  ("w08-alertas", "Alertas", "Regra de aviso + histórico"),
  ("w09-conta", "Conta e planos", "Fazenda, custos, plano, pagamento"),
 ]),
 ("App · celular (C)", "app", [
  ("a01-splash", "Splash", ""), ("a02-onb-fazenda", "Onboarding 1", "Fazenda"),
  ("a03-onb-compra", "Onboarding 2", "O que compra"), ("a04-onb-raio-cor", "Onboarding 3", "Raio, cor, aviso"),
  ("a05-home", "Início", "Resumo + ao vivo"), ("a06-lotes", "Lotes", "Feed com foto"),
  ("a07-lote", "Detalhe do lote", ""), ("a08-agenda", "Agenda", ""),
  ("a09-alertas", "Alertas", "Entrando agora"), ("a10-notificacao", "Notificação", "Tela bloqueada"),
  ("a11-salvos", "Salvos", "Aba dentro de Lotes"), ("a12-conta", "Conta", "Fazenda e plano"),
 ]),
 ("WhatsApp (B)", "whatsapp", [
  ("z01-resumo-segunda", "Resumo de segunda", "6h, ranking da semana"),
  ("z02-alerta-entrando", "Alerta entrando agora", "Com foto e botão"),
 ]),
 ("Design system", "", [
  ("componentes", "Componentes e estados", "Cores, tipos, cards, vazio, carregando, erro, sem sinal"),
 ]),
]

cards = []
for titulo, sub, itens in GR:
    app = sub in ("app", "whatsapp")
    h = []
    for k, t, d in itens:
        href = f"{sub}/{k}.html" if sub else f"{k}.html"
        h.append(f'''<figure class="{'m' if app else 'w'}"><a href="{href}"><img loading="lazy" src="png/{k}.png" alt="{t}"></a>
<figcaption><b>{t}</b>{'<span>'+d+'</span>' if d else ''}<em><a href="{href}">HTML</a> · <a href="png/{k}.png">PNG</a></em></figcaption></figure>''')
    cards.append(f'<section><h2>{titulo} <small>{len(itens)} telas</small></h2><div class="g {"gm" if app else "gw"}">{"".join(h)}</div></section>')

html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Radar Boi · Telas para aprovação · rodada 1</title>
<link rel="stylesheet" href="rb.css">
<style>
.w-main{{max-width:1360px}}
section{{margin-top:36px}}
h2{{font:800 26px/1.2 var(--fonte);color:var(--verde-900);margin-bottom:14px}} h2 small{{font-size:15px;color:var(--cinza);font-weight:600}}
.g{{display:grid;gap:18px}} .gw{{grid-template-columns:repeat(3,1fr)}} .gm{{grid-template-columns:repeat(6,1fr)}}
figure{{margin:0;background:#fff;border:1px solid var(--areia);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
figure img{{display:block;width:100%;background:#eee}}
figure.w img{{max-height:300px;object-fit:cover;object-position:top}} figure.w>a{{display:block;max-height:300px;overflow:hidden}}
figcaption{{padding:10px 12px 12px;font-size:14px;display:flex;flex-direction:column;gap:2px}}
figcaption b{{font-size:16px}} figcaption span{{color:var(--cinza)}} figcaption em{{font-style:normal;margin-top:4px;font-weight:600}}
.dec{{background:var(--amarelo);border-radius:18px;padding:20px 24px;margin-top:22px}}
.dec h3{{font:800 20px/1.2 var(--fonte);color:var(--verde-900);margin:0 0 10px}}
.dec ol{{margin:0;padding-left:22px;font-size:17px;line-height:1.5}}
</style></head><body>
<header class="w-top"><div class="in"><span class="rb-logo claro" style="color:#fff"><i>◎</i>Radar Boi</span><nav><a class="is-on">Telas · rodada 1</a><a href="https://github.com/gabrielhme-byte/radarboi/blob/main/docs/design/README.md">Design system (README)</a></nav><span style="color:#cfe3d4">05/11/2026</span></div></header>
<main class="w-main">
<h1 class="w-h1">Telas para aprovação · rodada 1</h1>
<div class="w-sub">Experiência A+B (painel web + WhatsApp) e a base do app (C). Dados reais de data.json (leilões de 26/10 a 04/11, 936 lotes). Filtro padrão: fêmeas 6–8@, 100% brancas, até 250 km de Barro Alto/GO. O que não é dado real está marcado <span class="rb-tag rb-tag--exemplo">exemplo</span>.</div>
<div class="dec"><h3>Para o Gabriel decidir</h3><ol>
<li><b>Número principal = R$/@ grande</b>, com R$/cab embaixo e o selo contra a Scot (barato ≤ −3%, caro ≥ +3%).</li>
<li><b>“Só 100% brancas” ligado por padrão</b>: mostra 16 de 269 lotes. Os leilões sem conferência aparecem à parte, marcados “cor não conferida”.</li>
<li><b>Teste de 30 dias do Pro sem cartão</b>, entrando só com o WhatsApp; no dia 25 a gente manda o link de pagamento (Pix recorrente).</li>
</ol></div>
{''.join(cards)}
<div style="height:40px"></div>
</main></body></html>"""
(D / "index.html").write_text(html)
print("index.html ok")
