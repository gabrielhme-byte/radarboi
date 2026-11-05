# Radar Boi

O leilão mais barato perto da sua fazenda, toda semana.

- `site/`: painel estático (HTML/JS) que lê `site/data.json`. Publicado no GitHub Pages.
- `scripts/build_data.py`: gera `data.json` a partir do levantamento em `../fazenda` (pipeline YouTube → OCR → cor → médias).
- `PLANO_DE_NEGOCIO.md`: nome, mercado, preço, operação, riscos, plano de 90 dias.

## Atualizar os dados

```bash
cd ../fazenda && python3 .tools/agg.py DATA && python3 .tools/peso.py DATA
cd ../radarboi && python3 scripts/build_data.py && git add -A && git commit -m "dados DATA" && git push
```
