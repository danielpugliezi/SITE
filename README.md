# Vai Viralizar?

Projeto de Machine Learning (Computer Science): um modelo que estima a chance de um vídeo curto viralizar a partir do **gancho**, da **estrutura** e do **conteúdo**.

| Pasta | O que tem |
|---|---|
| `notebook/previsor_viral.ipynb` | todo o projeto, passo a passo e documentado (abra no Jupyter Lab) |
| `data/videos.csv` | os 3.000 vídeos (sintéticos) gerados pelo notebook |
| `site/index.html` | site interativo para a apresentação (abra direto no navegador) |
| `site/model.js` | pesos do modelo, exportados pelo notebook (seção 11) |

## Como rodar

```bash
pip install -r requirements.txt
jupyter lab notebook/previsor_viral.ipynb
```

Rode todas as células (Run → Run All Cells). A seção 11 regrava `site/model.js`, então o site sempre usa o modelo que você acabou de treinar.

O site funciona offline: basta abrir `site/index.html` no navegador.
