"""
prever.py — abre o modelo salvo (.pkl) e prevê posts novos, fora do notebook.

Uso:
    python prever.py ../data/posts_novos.json          (extração simulada)
    python prever.py ../data/posts_novos.json --llm    (extração com LLM; precisa de ANTHROPIC_API_KEY)

Autor: Gustavo Pugliezi
"""
import json
import pickle
import sys
from pathlib import Path

import pandas as pd

import viralidade as vz  # precisa estar importável: o .pkl referencia vz.criar_features

PKL = Path(__file__).resolve().parent.parent / "modelo" / "previsor_viral.pkl"


def carregar_modelo(caminho=PKL):
    with open(caminho, "rb") as f:
        return pickle.load(f)


def prever_posts(posts, pacote, usar_llm=False):
    extrair = vz.extrair_com_llm if usar_llm else vz.extrair_simulado
    feats = pd.DataFrame([extrair(p) for p in posts])[pacote["colunas"]]
    probs = pacote["pipeline"].predict_proba(feats)[:, 1]
    return [(p["id"], float(pr), int(pr >= pacote["limiar"])) for p, pr in zip(posts, probs)]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pacote = carregar_modelo()
    posts = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(f"Modelo: {pacote['nome']} (treinado com {pacote['n_treino']} posts)\n")
    for pid, prob, classe in prever_posts(posts, pacote, usar_llm="--llm" in sys.argv):
        barra = "█" * round(prob * 20)
        print(f"{pid:10s} {prob:6.1%}  {barra:20s}  {'VIRAL' if classe else 'não viral'}")
