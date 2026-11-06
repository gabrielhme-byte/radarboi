# Radar Boi · Design system v1

Rodada 1, 05/11/2026. Galeria: <https://radarboi.com/design/>

- Tokens e componentes: `docs/design/rb.css`, sem dependência externa.
- Vitrine de componentes e estados: `componentes.html`.
- Telas:
  - `web/` (A, painel)
  - `app/` (C, moldura de 390×844)
  - `whatsapp/` (B)
- PNGs: `png/`, gerados com `python3 scripts/shots.py [filtro]`.
- Telas do app e do WhatsApp geradas por `scripts/gen_app.py`; galeria por `scripts/gen_galeria.py`.

Cada HTML abre com um comentário `<!-- ... -->` com as notas de comportamento para o dev.

## Princípios

1. **Primeiro o número.** O R$/@ é o maior texto de qualquer card. O R$/cab vai embaixo, e logo ao lado o selo contra a Scot.
2. **Sol e dedo grosso.** Contraste AA (4,5:1) em todo texto.
   - Toque mínimo de 48 px, e 56 px no botão principal.
   - Corpo de texto de 18 px no app e 16 px na web.
3. **Sinal fraco.**
   - Fonte do sistema.
   - Imagens leves (JPG de no máximo 60 KB no feed).
   - O app abre com o último ranking salvo e mostra de quando ele é.
4. **Palavra do campo.** Usar @, cabeça (cab.), lote, pista, era, bezerra, novilha, leilão, leiloeira. Evitar "ativo", "item", "listagem" e "dashboard".
5. **Honestidade do dado.**
   - O preço é o *último lance na tela*, não venda confirmada.
   - O peso é *estimado pela era*.
   - Tudo que não é dado real leva a tag `exemplo`.
   - Cor não conferida nunca aparece como "branca".
6. **Uma ação principal por tela.** Quase sempre é "Ver no vídeo" ou "Assistir agora".

## Cores

| Token | Hex | Uso |
|---|---|---|
| `--verde-900` | #163a20 | títulos |
| `--verde-800` | #1f4d2b | marca, barra do topo, chip ligado, KPI destaque |
| `--verde-600` | #2f7a43 | botão principal, links |
| `--verde-100` / `--verde-50` | #e3f1e6 / #f1f8f2 | fundos leves, opção marcada |
| `--amarelo` | #ffd54a | **um** destaque por tela: 1º lugar, preço no KPI escuro, CTA de venda |
| `--amarelo-100` | #fff4cc | tag de margem |
| `--creme` | #f6f3ea | fundo da página |
| `--areia` | #e4dfd0 | bordas |
| `--tinta` / `--cinza` | #1d1d1b / #55554f | texto / texto secundário (6,9:1 no creme) |
| `--barato` + `-bg` | #1e7a3c / #dff0e3 | abaixo da Scot |
| `--caro` + `-bg` | #b3261e / #fde2e0 | acima da Scot, erro |
| `--aviso` + `-bg` | #7a5600 / #fff3d6 | cor não conferida, avisos |
| `--aovivo` | #d32f2f | **só** para o que está na pista agora |
| `--wa`, `--wa-bg`, `--wa-eu` | #075e54… | mockups e botões do WhatsApp |

Verde e vermelho têm sentido de barato e caro, então nunca aparecem sem seta (▼▲) e texto.

## Tipografia

- Fonte do sistema: `-apple-system, Roboto, Segoe UI…`.
- Números com `font-variant-numeric: tabular-nums` (classe `.num`).

| Token | Tamanho / peso | Uso |
|---|---|---|
| `--t-56` | 56 / 800 | título da landing |
| `--t-40` | 40 / 800 | preço principal no detalhe e no destaque do app |
| `--t-32` | 32 / 800 | título de tela, valor de KPI, R$/@ do card de leilão |
| `--t-24` | 24 / 800 | título de seção |
| `--t-20` | 20 / 800 | título de card |
| `--t-18` | 18 / 400 | corpo no app, botões |
| `--t-16` | 16 / 400 | corpo na web |
| `--t-14` | 14 / 600 | legenda, selos (mínimo para texto informativo) |
| `--t-12` | 12 / 700 | só a tag `exemplo` e os rótulos da tab bar |

## Espaço, raio, sombra

- Espaçamento na base 4: `--e-1` 4, `--e-2` 8, `--e-3` 12, `--e-4` 16, `--e-5` 20, `--e-6` 24, `--e-8` 32, `--e-12` 48, `--e-16` 64.
  - Margem lateral: 16 px no app e 28 px na web; o conteúdo da web vai até 1240 px.
- Raios:
  - `--r-1` 8: selos
  - `--r-2` 12: botões e campos
  - `--r-3` 16: cards
  - `--r-pill`: chips
- Sombra única: `--sombra`, usada só em card que flutua (alerta ao vivo, notificação).

## Componentes

O nome do componente vem primeiro, depois a classe CSS.

| Componente | Classe | Variações e regras |
|---|---|---|
| **Botao** | `.rb-btn` | `--pri` (verde, 56 px), `--sec` (contorno), `--amarelo` (CTA de venda), `--wa` (entrar ou mandar no WhatsApp), `--txt`, `--full`, `.is-disabled`. O texto sempre começa com verbo. |
| **ChipFiltro** | `.rb-chip` | `.is-on` (verde-800 + ✓ amarelo), `--add` (tracejado, abre o filtro). Num grupo de opções exclusivas, só um fica ligado. |
| **SeloCor** | `.rb-selo` | `--ok` "100% brancas" (lote conferido em 3 imagens), `--nc` "cor não conferida", `--fora` "tem animal de outra cor". Vai sobre a foto, no canto inferior esquerdo. |
| **BadgeScot** | `.rb-scot` | `--barato` ▼ (≤ −3%), `--neutro` = (entre −3% e +3%), `--caro` ▲ (≥ +3%). Fórmula: `(R$/@ do lote ÷ R$/@ Scot da era) − 1`. Hoje a referência é a Scot GO bezerra 12 m, R$ 3.062,98/cab ÷ 7@ = R$ 438/@ (04/11). |
| **Tag** | `.rb-tag` | `--margem` (amarela), `--aovivo` (vermelha com ponto), `--exemplo` (tracejada: dado ilustrativo). |
| **Kpi** | `.rb-kpi` | rótulo, valor e sub. `--destaque` (fundo verde e valor amarelo): só um por tela, para o "mais barato". |
| **CardLeilao** | `.rb-leilao` | posição, nome e leiloeira, meta (km, data, cab.), R$/@ + BadgeScot, barra (largura = R$/@ ÷ maior R$/@; traço preto = Scot), rodapé com margem e contagem de cor. `.is-1` deixa a posição em amarelo. |
| **CardLote** | `.rb-lote` | foto 21:8 com SeloCor e minuto do vídeo, título "N bezerras · era", R$/cab, R$/@ + BadgeScot, meta, margem, ações (Ver no vídeo / Salvar). Na web vira **LinhaLote** (tabela, `w05`). |
| **Alerta** | `.rb-alerta` | padrão (vermelho, ao vivo), `--info`, `--aviso`, `--erro`. Ícone, título e uma linha. |
| **FaixaAoVivo** | `.rb-aovivo` | fundo vinho, tag AO VIVO, lote e R$/@, ▶. Só aparece quando há leilão do raio no ar com lote do filtro. |
| **TabBar** | `.rb-tabbar` | 5 abas: Início, Lotes, Agenda, Alertas, Conta. Bolinha vermelha com o número de alertas não vistos. Salvos fica dentro de Lotes (segmento "Todos / ★ Salvos"). |
| **Campo, Opcao, Toggle, Slider** | `.rb-campo`, `.rb-opcao`, `.rb-toggle`, `.rb-slider` | Opcao é um checkbox grande (mín. 56 px) com título e linha de ajuda. Toggle tem 56×32 e toque de 48. |
| **RodapeLegal** | `.rb-rodape` | Em toda tela web, e no app na Conta: "Radar Boi é um produto da Starcore Produtos de Tecnologia Ltda, CNPJ 39.573.543/0001-33" (a Meta exige para aprovar o nome no WhatsApp). `--escuro` vai sobre fundo verde. |
| **Nota** | `.rb-nota` | caixa branca com texto de 14 px: como ler o dado, de onde vem. |

Ícones: nesta rodada são emoji, só para o desenho. Na implementação, trocar por **Lucide** (web e app), mantendo 24 px, traço 2 e a cor do texto.

## Estados (ver `componentes.html`)

| Estado | Componente | Regra |
|---|---|---|
| Vazio | `EstadoVazio` (`.rb-vazio`) | Diz *por que* está vazio e oferece duas saídas: "Aumentar o raio" e "Avisar quando surgir". |
| Carregando | `Carregando` (`.rb-sk`) | Esqueleto no formato do card. Só aparece depois de 300 ms. Nunca um spinner de tela inteira. |
| Erro | `EstadoErro` | "Não deu para carregar", seguido de "Tentar de novo" e "Avisar no WhatsApp". Os filtros não se perdem. |
| Sem sinal | `SemSinal` (`.rb-offline`) | Faixa escura no topo: "mostrando o que foi salvo em DD/MM, HH:MM". Preço e ranking funcionam offline; foto e vídeo esperam o sinal. |

## Telas desta rodada

**Web (A)**
- `w01` landing
- `w02` entrar com WhatsApp
- `w03` onboarding
- `w04` ranking
- `w05` lotes
- `w06` detalhe do lote
- `w07` agenda
- `w08` alertas
- `w09` conta e planos

**App (C)**
- `a01` splash
- `a02`–`a04` onboarding
- `a05` início
- `a06` lotes
- `a07` detalhe
- `a08` agenda
- `a09` alertas
- `a10` notificação "entrando agora"
- `a11` salvos
- `a12` conta

**WhatsApp (B)**
- `z01` resumo de segunda
- `z02` alerta "entrando agora"

## Dados usados

- Fonte: `docs/data.json`, leilões de 26/10 a 04/11/2026 (25 leilões, 936 lotes).
- Fazenda: Barro Alto/GO.
- Filtro padrão:
  - fêmeas
  - 6–8@ (10–15 m)
  - 100% brancas
  - até 250 km
  - venda com 15@ a R$ 364,71/@ (Datagro novilha GO, 04/11)
- Resultado: 16 lotes, 353 cabeças, 3 cidades.
- Ranking:

| Leilão | Data | R$/@ |
|---|---|---|
| Uruaçu | 28/10 | 325 |
| Uruaçu | 04/11 | 328 |
| Niquelândia | 03/11 | 339 |
| Porangatu | 26/10 | 456 |

- Scot: R$ 438/@.
- Curva de peso pela era: 8 m = 180 kg, 12 m = 210 kg, 18 m = 270 kg; 1@ = 30 kg.

## Pontos em aberto para o dev

- **Alerta "entrando agora".** A conferência de cor hoje é manual, depois do leilão. Enquanto não houver conferência ao vivo, o alerta sai com o selo `--nc` "cor a conferir". O mockup mostra a versão final, com a cor já conferida.
- **Horário dos leilões.** Fica "a confirmar" até a leiloeira divulgar. A agenda é uma previsão pela recorrência semanal.
- **Margem.** É 15@ × preço da gorda menos o lance, sem recria, frete e comissão, até o usuário preencher "Meus custos".
