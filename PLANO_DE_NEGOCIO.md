# Radar Boi: plano de negócio (v1, 05/11/2026)

> **O leilão mais barato perto da sua fazenda, toda semana.**
> Preço de cada lote dos leilões regionais, com o minuto do vídeo, peso estimado, R$/@ e conferência de cor. No celular e no WhatsApp.

## 1. Nome e marca

| Opção | Domínio .com.br | Por que |
|---|---|---|
| **Radar Boi** (escolhido) | radarboi.com.br **livre** (registro.br, 05/11) | Curto, fácil de falar no rádio ou no leilão, e diz o que faz: "vigia" os leilões |
| Pista Boi | pistaboi.com.br livre | "Pista" é onde o lote entra no leilão |
| Lance Boi | lanceboi.com.br livre | Fala do lance, mas pode parecer que a gente dá lance pelo cliente |

Já estão ocupados: pistacerta, arrobacerta, radardoleilao, lancecerto e boinapista.
- **Próximo passo:** registrar radarboi.com.br (cerca de R$ 40 por ano) e o @radarboi no Instagram, TikTok e YouTube. Pesquisar a marca no INPI (classe 35/42) antes de investir em identidade visual.

## 2. Problema

- Quem faz recria e engorda compra reposição em leilões regionais semanais. São 20 a 30 só no raio de 500 km de Barro Alto.
- Para saber onde está barato, o fazendeiro precisa assistir horas de transmissão no YouTube ou confiar no "ouvi dizer".
- As referências públicas (Scot, CEPEA, Datagro) dão **uma média do estado**. Elas não dizem **em qual leilão perto de você** a @ de reposição está 25% mais barata.
- A tela do leilão diz "NELORE", mas quem declara é o vendedor. No levantamento-piloto, **de 30% a 50% dos lotes "Nelore" tinham animal de outra cor**. O fazendeiro que quer lote padrão branco perde tempo e dinheiro.

## 3. Solução (o que o assinante recebe)

1. **Relatório semanal** no WhatsApp toda segunda, com ranking dos leilões da semana do mais barato ao mais caro, por categoria, era e peso.
2. **Painel no celular** com filtros de fazenda, raio, sexo, peso estimado, "só branco conferido" e margem até o peso de venda.
3. **Link no minuto exato** do lote no vídeo, para o fazendeiro conferir o gado com os próprios olhos.
4. **Alertas.** Quando o catálogo do próximo leilão sai, ou durante a transmissão, avisamos: "lote de 20 bezerras brancas de 12 m entrando agora em Uruaçu".
5. **Margem de recria** usando o custo do próprio cliente (R$/cab/mês, GMD, peso de venda).
6. **Rede de serviços:** freteiros da rota, leiloeiras e, no futuro, financiamento.

**O que não fazemos:** não damos lance, não compramos e não intermediamos. Somos informação. Isso evita risco jurídico e conflito com as leiloeiras.

## 4. Cliente

| Segmento | Quem | Dor | Prioridade |
|---|---|---|---|
| **Recriador/engordador** (como o Gabriel) | 200 a 5.000 cabeças, compra reposição o ano todo | Pagar caro ou comprar lote misturado | **1 (começar aqui)** |
| Corretor/comprador de gado | Compra para terceiros, assiste muitos leilões | Tempo | 2 |
| Criador que vende bezerro | Quer saber em qual leilão vender | Vender barato | 3 |
| Leiloeiras | Querem mais compradores na live | Audiência | Parceria (B2B) |

**Região inicial:** Norte e Centro Goiano, com raio de 500 km de Barro Alto (Uruaçu, Niquelândia, Porangatu, Goianésia, Ceres, Mara Rosa, Campinorte, Santa Terezinha, Nova Crixás, Gurupi/TO). Depois: GO inteiro, TO, MT e MG.

## 5. Tamanho do mercado (estimativa)

- Goiás tem cerca de 24 milhões de cabeças e cerca de 150 mil estabelecimentos com bovinos (IBGE). Os que fazem recria/engorda e compram em leilão são uma fração. Estimamos **5 a 10 mil fazendas em GO/TO** com perfil comprador regular.
- **Meta de 3 anos:** 1.000 assinantes × R$ 120 médio = **R$ 1,44 milhão/ano**.
- **Argumento de valor:** comprar 20 novilhas R$ 300 mais barato por cabeça economiza R$ 6.000 em uma compra. A assinatura de um ano custa menos que isso.

## 6. Concorrência

| Quem | O que faz | Nossa diferença |
|---|---|---|
| Scot, CEPEA, Datagro, Notícias Agrícolas | Média estadual de reposição | Mostramos **o leilão e o lote** com o link do vídeo |
| Canal do Boi, Terraviva, Lance Rural | Transmitem leilões especiais | Cobrimos leilões **semanais de corte regionais** e comparamos todos |
| Apps de leiloeiras (Agrobold, Lance Agro…) | Lance online de cada leiloeira | Somos neutros e comparamos todas as leiloeiras |
| Uboi, Rota Rural | Frete | São possíveis parceiros |

## 7. Modelo de receita

| Plano | Preço | Para quem |
|---|---|---|
| Semanal | R$ 79/mês (R$ 790/ano) | Relatório de segunda no WhatsApp |
| **Pro** | **R$ 149/mês** (R$ 1.490/ano) | Painel, filtros, alertas, margem própria |
| Fazenda+ | R$ 399/mês | Várias fazendas e usuários, freteiros, atendimento |

- Teste grátis de 30 dias, com cartão ou Pix recorrente (Asaas, Iugu ou Mercado Pago).
- **Receitas futuras:** destaque pago para leiloeiras ("leilão em destaque"), indicação de frete, dados agregados para frigoríficos e bancos (anônimos).

## 8. Operação: como os dados são feitos

O pipeline já funciona no protótipo (pasta `fazenda/.tools`):

1. **Descoberta:** busca as transmissões nos canais das leiloeiras (YouTube) e na agenda.
2. **Leitura:** baixa o vídeo em baixa resolução, lê a tarja de lote/quantidade/idade/lance por OCR e monta os lotes com o minuto.
3. **Cor:** monta folhas com 3 imagens por lote. **Hoje a conferência é humana.** Isso é o gargalo.
4. **Médias e ranking:** calcula por categoria, era, R$/@ estimado e margem, e gera o PDF e o `data.json` do painel.

**Para escalar** (prioridade técnica):
- Classificador automático de cor (visão computacional) com revisão humana só dos casos em dúvida. Meta: 15 min de revisão por leilão.
- Leitura ao vivo durante a transmissão, para os alertas.
- Parcerias com leiloeiras para receber o catálogo com **peso real** e trocar o peso estimado.

**Custos mensais estimados no início:** servidor e armazenamento R$ 300–800; WhatsApp Business API R$ 0,05–0,30 por mensagem; domínio e e-mail R$ 50; revisor de cor de meio período R$ 1.500–2.500.

## 9. Riscos e cuidados

| Risco | Como tratar |
|---|---|
| Direito de imagem/conteúdo das leiloeiras | Não republicar vídeo, só preço e link para o vídeo original (que gera audiência para elas). Oferecer parceria. |
| Preço errado (lance ≠ venda, erro de leitura) | Sempre mostrar "último lance na tela" e o link do minuto. Revisão por amostragem. Botão "reportar erro". |
| Peso estimado ≠ real | Aviso claro e busca de catálogo com peso |
| Leiloeira bloquear | Diversificar fontes. Parcerias. Valor para ela: mais compradores. |
| Dependência do YouTube | Fontes alternativas: sites das leiloeiras, Canal do Boi, catálogos |
| LGPD | Guardar só dados de contato do assinante, com termo de uso e política de privacidade |

**Jurídico:** abrir um CNPJ (MEI não serve para software/assinatura; o caminho é ME no Simples, anexo III/V), contrato de sócios (quotas, quem faz o quê, vesting) e termos de uso.

## 10. Plano de lançamento (90 dias)

| Semana | O que | Meta |
|---|---|---|
| **1–2** | Registrar domínio e redes. Painel no ar (feito). Relatório de segunda automático. Lista de 30 fazendeiros conhecidos. | 10 testadores ativos |
| 3–4 | Teste grátis. Ligar para cada testador: "o que você usou? pagaria quanto?" | 5 dizem "pagaria" |
| 5–6 | Cobrança via Pix/cartão. Grupo/lista de transmissão de WhatsApp. Conferência de cor semi-automática. | **10 pagantes** |
| 7–8 | Alertas de lote barato. Margem com custo próprio. Conteúdo semanal no Instagram: "onde a bezerra branca está mais barata esta semana". | 25 pagantes |
| 9–12 | Parceria com 2 ou 3 leiloeiras (catálogo com peso). Ampliar para GO inteiro. | **50 pagantes, cerca de R$ 6 mil/mês** |

**Canais de venda:** indicação entre fazendeiros (o maior), presença nos próprios leilões (QR code no curral), sindicatos rurais, revendas de nutrição/insumos, Instagram/TikTok com o "ranking da semana" e as próprias leiloeiras.

## 11. Números (cenário base)

| | Mês 3 | Mês 6 | Mês 12 | Mês 24 |
|---|---|---|---|---|
| Assinantes | 50 | 150 | 400 | 1.000 |
| Receita/mês (ticket R$ 120) | R$ 6 mil | R$ 18 mil | R$ 48 mil | R$ 120 mil |
| Custo/mês | R$ 4 mil | R$ 8 mil | R$ 18 mil | R$ 40 mil |
| Resultado/mês | R$ 2 mil | R$ 10 mil | R$ 30 mil | R$ 80 mil |

**Investimento inicial estimado:** R$ 5–15 mil (domínio, marca, cobrança, revisor de cor por 3 meses, anúncios locais). Dá para começar sem investidor.

## 12. Indicadores para acompanhar toda semana

- Leilões cobertos e lotes lidos
- % de lotes com cor conferida
- Erros reportados
- Testadores ativos, conversão teste → pago, cancelamento mensal (meta < 5%)
- "Economia gerada": quantos assinantes compraram por indicação nossa e quanto economizaram (vira depoimento)

## 13. Divisão entre sócios (sugestão para discutir)

| Frente | Quem |
|---|---|
| Produto, dados e tecnologia (pipeline, painel, app) | Gabriel e o agente |
| Vendas e relacionamento (fazendeiros, leiloeiras, sindicatos) | Sócio |
| Conferência de cor e qualidade dos dados | Revisor contratado, ou os dois no início |
| Financeiro, jurídico e CNPJ | Definir |
