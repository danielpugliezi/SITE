# Vai Viralizar?

Projeto de Machine Learning (Computer Science) de **Gustavo Pugliezi**: um modelo de Regressão Logística que estima a chance de um vídeo curto viralizar a partir do **gancho**, da **estrutura** e do **conteúdo**.

| Arquivo | O que tem |
|---|---|
| `notebook/previsor_viral.ipynb` | o projeto completo, nos 12 passos do framework |
| `data/posts.json` | 3.000 posts (simulados) recebidos em JSON |
| `data/gerar_posts.py` | script que gerou os posts |
| `data/posts_novos.json` | 4 posts novos, sem resposta, para testar o modelo |
| `data/dataset.csv` | dataset montado no passo 5 |
| `app/viralidade.py` | especificação das features, extração (LLM ou simulada) e engenharia de features |
| `app/prever.py` | aplicação que abre o `.pkl` e prevê posts novos |
| `modelo/previsor_viral.pkl` | modelo treinado |
| `site/index.html` | site interativo da apresentação (abre direto no navegador) |

## Como rodar

```bash
pip install -r requirements.txt
jupyter lab notebook/previsor_viral.ipynb      # Run → Run All Cells

cd app
python prever.py ../data/posts_novos.json      # usa o modelo .pkl fora do notebook
```
