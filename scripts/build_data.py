"""Gera docs/data.json a partir do levantamento da fazenda (pipeline YouTube → OCR → cor → médias).
Uso: python3 scripts/build_data.py [DATA]   (padrão: lotes mais recente)"""
import csv, json, os, sys, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FZ = os.path.join(os.path.dirname(ROOT), 'fazenda')
sys.path.insert(0, os.path.join(FZ, '.tools'))
import peso as PZ  # curva de peso por idade e preço da novilha gorda

arqs = sorted(glob.glob(os.path.join(FZ, 'dados', 'lotes_*.csv')))
D = sys.argv[1] if len(sys.argv) > 1 else re.search(r'lotes_(.+)\.csv', arqs[-1]).group(1)
LE = {r['video']: r for r in csv.DictReader(open(os.path.join(FZ, 'leiloes.csv'), encoding='utf-8'))}
REV, COR = {}, {}
p = os.path.join(FZ, 'cor', 'revisao.csv')
for r in csv.DictReader(open(p, encoding='utf-8')):
    COR[(r['video'], r['fim'])] = r['status']   # revisao.csv atual manda na cor (fim do lote = minuto)
    REV.setdefault(r['video'], {'ok': 0, 'reprovado': 0, 'duvidoso': 0})[r['status']] += 1

SEXO = {'bezerro': 'M', 'garrote': 'M', 'bezerra': 'F', 'novilha': 'F'}
lotes, usados = [], set()
for l in csv.DictReader(open(os.path.join(FZ, 'dados', f'lotes_{D}.csv'), encoding='utf-8')):
    if l['nelore'] != 'True' or not l['qtd'] or not l['preco_cab']: continue
    if l['obs'] and not l['obs'].startswith('cor:'): continue   # erro de leitura etc.
    idade = int(float(l['idade_m'])) if l['idade_m'] else None
    kg = round(PZ.peso(idade)) if idade else None
    lotes.append(dict(v=l['video'], c=l['categoria'], s=SEXO[l['categoria']], q=int(l['qtd']), i=idade,
                      p=int(l['preco_cab']), kg=kg, cor=COR.get((l['video'], l['minuto']), 'não conferido'), m=l['minuto'], u=l['link']))
    usados.add(l['video'])

leiloes = []
for v in usados:
    m = LE[v]
    leiloes.append(dict(v=v, nome=m['leilao'], casa=m['leiloeira'], cidade=m['cidade'], uf=m['uf'],
                        lat=float(m['lat']), lon=float(m['lon']), data=m['data'], rev=REV.get(v)))
out = dict(atualizado=D, gorda=dict(rs_arroba=PZ.GORDA, fonte='Datagro novilha GO', data='04/11/2026'),
           ref=dict(bezerra12=dict(rs_cab=3062.98, kg=210, fonte='Scot GO 04/11/2026')),
           leiloes=sorted(leiloes, key=lambda x: x['data']), lotes=lotes)
json.dump(out, open(os.path.join(ROOT, 'docs', 'data.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
print(D, len(leiloes), 'leilões', len(lotes), 'lotes', sum(1 for l in lotes if l['cor'] == 'ok'), 'brancos conferidos')
