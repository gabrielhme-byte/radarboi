// Radar Boi: painel estático. Lê data.json e calcula ranking por R$/@ estimada a partir da fazenda escolhida.
const FAZENDAS = [
  ['Barro Alto/GO', -14.966, -48.908], ['Goianésia/GO', -15.317, -49.117], ['Uruaçu/GO', -14.524, -49.141],
  ['Niquelândia/GO', -14.474, -48.460], ['Porangatu/GO', -13.440, -49.149], ['Goiânia/GO', -16.686, -49.264],
  ['Anápolis/GO', -16.328, -48.953], ['Goianápolis/GO', -16.509, -49.023], ['Ceres/GO', -15.308, -49.598],
  ['São Miguel do Araguaia/GO', -13.275, -50.163], ['Gurupi/TO', -11.729, -49.068]
];
const WA = '5562900000000'; // TODO: número comercial do Radar Boi
const $ = s => document.querySelector(s);
const brl = v => 'R$ ' + Math.round(v).toLocaleString('pt-BR');
const dm = d => d.slice(8, 10) + '/' + d.slice(5, 7);
const CAT = { bezerro: 'Bezerro', bezerra: 'Bezerra', garrote: 'Garrote', novilha: 'Novilha' };
function km(a, b, c, d) {
  const r = Math.PI / 180, x = Math.sin((c - a) * r / 2) ** 2 + Math.cos(a * r) * Math.cos(c * r) * Math.sin((d - b) * r / 2) ** 2;
  return 12742 * Math.asin(Math.sqrt(x));
}
let DB;
fetch('data.json').then(r => r.json()).then(j => { DB = j; init(); });

function init() {
  const f = $('#fFaz');
  FAZENDAS.forEach((z, i) => f.add(new Option(z[0], i)));
  f.add(new Option('📍 Usar minha localização', 'gps'));
  const q = new URLSearchParams(location.search);
  if (q.get('faz')) f.value = q.get('faz');
  ['#fFaz', '#fRaio', '#fSexo', '#fPeso', '#fCor', '#fVenda'].forEach(s => $(s).addEventListener('input', render));
  f.addEventListener('change', () => {
    if (f.value === 'gps' && navigator.geolocation) navigator.geolocation.getCurrentPosition(p => {
      FAZENDAS.push(['Minha localização', p.coords.latitude, p.coords.longitude]);
      f.add(new Option('Minha localização', FAZENDAS.length - 1), f.options.length - 1); f.value = FAZENDAS.length - 1; render();
    });
  });
  $('#btnWa').href = `https://wa.me/${WA}?text=${encodeURIComponent('Quero testar o Radar Boi por 7 dias')}`;
  $('#fonteVenda').textContent = `Venda: ${DB.gorda.fonte}, R$ ${DB.gorda.rs_arroba.toLocaleString('pt-BR')}/@ (${DB.gorda.data}). Atualizado em ${DB.atualizado.split('-').reverse().join('/')}.`;
  const conf = DB.leiloes.filter(l => l.rev).length;
  $('#heroNums').innerHTML = `<div><b>${DB.leiloes.length}</b>leilões lidos</div><div><b>${DB.lotes.length}</b>lotes Nelore</div><div><b>${conf}</b>leilões com cor conferida</div><div><b>500 km</b>de raio</div>`;
  render();
}

function render() {
  const z = FAZENDAS[+$('#fFaz').value] || FAZENDAS[0];
  const raio = +$('#fRaio').value; $('#fRaioV').textContent = raio + ' km';
  const sexo = $('#fSexo').value, pz = $('#fPeso').value, soOk = $('#fCor').checked, venda = +$('#fVenda').value * DB.gorda.rs_arroba;
  const [a0, a1] = pz ? pz.split('-').map(Number) : [0, 99];
  const LE = {};
  DB.leiloes.forEach(l => { l.km = Math.round(km(z[1], z[2], l.lat, l.lon)); LE[l.v] = l; });
  const lotes = DB.lotes.filter(l => {
    const le = LE[l.v]; if (!le || le.km > raio) return false;
    if (sexo && l.s !== sexo) return false;
    if (soOk ? l.cor !== 'ok' : (l.cor === 'reprovado' || l.cor === 'duvidoso')) return false;
    if (pz && (!l.kg || l.kg / 30 < a0 || l.kg / 30 > a1)) return false;
    return true;
  }).map(l => ({ ...l, arr: l.kg ? l.kg / 30 : null }));

  // ranking por leilão
  const g = {};
  lotes.forEach(l => { (g[l.v] = g[l.v] || []).push(l); });
  const rows = Object.entries(g).map(([v, ls]) => {
    const cab = ls.reduce((s, l) => s + l.q, 0), pm = ls.reduce((s, l) => s + l.q * l.p, 0) / cab;
    const cw = ls.filter(l => l.kg), cabw = cw.reduce((s, l) => s + l.q, 0);
    const kg = cabw ? cw.reduce((s, l) => s + l.q * l.kg, 0) / cabw : null;
    return { le: LE[v], cab, n: ls.length, pm, kg, ra: kg ? pm / (kg / 30) : null };
  }).sort((a, b) => (a.ra ?? 1e9) - (b.ra ?? 1e9));
  const tot = lotes.reduce((s, l) => s + l.q, 0);
  const totKg = lotes.filter(l => l.kg).reduce((s, l) => s + l.q * l.kg, 0), totKgCab = lotes.filter(l => l.kg).reduce((s, l) => s + l.q, 0);
  const medP = tot ? lotes.reduce((s, l) => s + l.q * l.p, 0) / tot : 0;
  const medA = totKgCab ? lotes.filter(l => l.kg).reduce((s, l) => s + l.q * l.p, 0) / (totKg / 30) : 0;
  const ref = DB.ref.bezerra12, refA = ref.rs_cab / (ref.kg / 30);
  $('#resumo').innerHTML = tot ? `
    <div>Média na região<b>${brl(medP)}/cab</b>${tot} cabeças · ${lotes.length} lotes</div>
    <div>R$ por @ estimada<b>${brl(medA)}/@</b>referência Scot GO bezerra 12m: ${brl(refA)}/@</div>
    <div>Mais barato<b>${rows[0] ? rows[0].le.cidade + ' · ' + brl(rows[0].ra || rows[0].pm) + (rows[0].ra ? '/@' : '') : '-'}</b>${rows[0] ? rows[0].le.km + ' km · ' + dm(rows[0].le.data) : ''}</div>
    <div>Margem média até ${$('#fVenda').value}@<b>${brl(venda - medP)}/cab</b>sem custo de recria, frete e comissão</div>`
    : `<div>Nenhum lote com esses filtros. Aumente o raio ou desmarque "só brancos conferidos".</div>`;

  $('#tLeiloes').innerHTML = '<tr><th>#</th><th>Leilão</th><th>Cidade</th><th class="n">Distância</th><th>Data</th><th class="n">Cab.</th><th class="n">R$/cab</th><th class="n">Peso est.</th><th class="n">R$/@ est.</th><th class="n">vs Scot</th><th class="n">Margem</th><th>Cor</th><th></th></tr>' +
    rows.map((r, i) => {
      const d = r.ra ? (r.ra / refA - 1) * 100 : null, cls = d == null ? '' : d < -5 ? 'bom' : d > 5 ? 'ruim' : '';
      const rv = r.le.rev, cor = rv ? `<span class="tag ok">${rv.ok} ok</span> <span class="tag rep">${rv.reprovado + rv.duvidoso} fora</span>` : '<span class="tag nc">não conferida</span>';
      return `<tr><td>${i + 1}º</td><td>${r.le.casa}<div class="peq">${r.le.nome}</div></td><td>${r.le.cidade}/${r.le.uf}</td><td class="n">${r.le.km} km</td><td>${dm(r.le.data)}</td><td class="n">${r.cab}${r.cab < 20 ? ' <span class="peq">(pouco)</span>' : ''}</td>` +
        `<td class="n">${brl(r.pm)}</td><td class="n">${r.kg ? Math.round(r.kg) + ' kg' : '-'}</td><td class="n ${cls}">${r.ra ? brl(r.ra) : '-'}</td><td class="n ${cls}">${d == null ? '-' : (d > 0 ? '+' : '') + d.toFixed(0) + '%'}</td>` +
        `<td class="n">${brl(venda - r.pm)}</td><td>${cor}</td><td><a href="https://youtu.be/${r.le.v}" target="_blank">vídeo</a></td></tr>`;
    }).join('');

  const ls = lotes.slice().sort((a, b) => (a.arr ? a.p / a.arr : 1e9) - (b.arr ? b.p / b.arr : 1e9)).slice(0, 200);
  $('#tLotes').innerHTML = '<tr><th>#</th><th>Cidade</th><th class="n">Dist.</th><th>Data</th><th>Categoria</th><th class="n">Qtd</th><th class="n">Idade</th><th class="n">R$/cab</th><th class="n">Peso est.</th><th class="n">R$/kg</th><th class="n">R$/@</th><th class="n">Margem</th><th>Cor</th><th>Vídeo</th></tr>' +
    ls.map((l, i) => {
      const le = LE[l.v], tag = l.cor === 'ok' ? '<span class="tag ok">branco</span>' : '<span class="tag nc">não conferida</span>';
      return `<tr><td>${i + 1}º</td><td>${le.cidade}</td><td class="n">${le.km} km</td><td>${dm(le.data)}</td><td>${CAT[l.c]}</td><td class="n">${l.q}</td><td class="n">${l.i ? l.i + ' m' : '-'}</td><td class="n">${brl(l.p)}</td>` +
        `<td class="n">${l.kg ? l.kg + ' kg' : '-'}</td><td class="n">${l.kg ? 'R$ ' + (l.p / l.kg).toFixed(2).replace('.', ',') : '-'}</td><td class="n"><b>${l.arr ? brl(l.p / l.arr) : '-'}</b></td><td class="n">${brl(venda - l.p)}</td><td>${tag}</td><td><a href="${l.u}" target="_blank">${l.m}</a></td></tr>`;
    }).join('');
}
