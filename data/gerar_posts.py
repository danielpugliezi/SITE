"""
Gera data/posts.json: 3.000 posts simulados no formato que a turma recebe.

Os vídeos são sintéticos: suas características são sorteadas e a chance de viralizar
segue regras inspiradas no que criadores observam, mais um fator de sorte.
O notebook NÃO usa estas regras; ele só lê o JSON.

Uso:  python gerar_posts.py
Autor: Gustavo Pugliezi
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

SEED, N = 42, 3000
rng = np.random.default_rng(SEED)

TIPOS = ["pergunta", "choque", "promessa", "historia", "nenhum"]
ESTRUTURAS = ["lista", "tutorial", "antes_depois", "storytime", "vlog"]
TEMAS = ["humor", "educacao", "beleza", "games", "culinaria", "esporte"]

ASSUNTO = {
    "humor": ["a minha vó no churrasco", "o meu cachorro dramático"],
    "educacao": ["buracos negros", "a Revolução Francesa"],
    "beleza": ["delineado gatinho", "pele oleosa"],
    "games": ["o chefe final mais difícil", "o speedrun do mapa novo"],
    "culinaria": ["bolo de cenoura", "pão de queijo de frigideira"],
    "esporte": ["o gol do fim de semana", "treino de embaixadinha"],
}
HASHTAGS = {"humor": "#humor #comedia", "educacao": "#educacao #aprenda", "beleza": "#beleza #makeup",
            "games": "#games #gamer", "culinaria": "#receita #culinaria", "esporte": "#futebol #esporte"}
HOOK = {
    "pergunta": ["Você sabia isso sobre {a}?", "Por que ninguém fala sobre {a}?", "Já pensou em {a}?"],
    "choque": ["PARA TUDO! Olha {a}", "Eu não acredito no que virou {a}", "Isso deveria ser proibido: {a}"],
    "promessa": ["Vou te mostrar {a} em segundos", "O segredo de {a} é esse", "Depois desse vídeo você vai dominar {a}"],
    "historia": ["Deixa eu te contar sobre {a}", "Olha o que aconteceu com {a}", "Essa é a história de {a}"],
}
ENCHIMENTO = ["Oi gente", "Então", "Bom, vamos lá", "Hoje o vídeo é rapidinho", "Tô aqui de novo"]
CORPO = ["E aí eu fui fazer", "Ficou assim", "Pois é", "Comenta aí embaixo", "Valeu por assistir"]
LEGENDA = {
    "lista": ["3 coisas sobre {a}", "Top 5: {a}"], "tutorial": ["Como fazer: {a}", "Passo a passo de {a}"],
    "antes_depois": ["Antes e depois: {a}", "A transformação de {a}"],
    "storytime": ["Storytime: {a}", "Contei tudo sobre {a}"], "vlog": ["Vlog: {a}", "Meu dia com {a}"],
}
NOTAS = {
    "rosto_1s": (["abre com close no rosto", "rosto aparece logo no primeiro segundo"],
                 ["começa mostrando o cenário", "primeiros segundos sem ninguém na tela"]),
    "texto_na_tela": (["texto grande na tela no início", "legenda escrita em cima do vídeo"], ["sem texto na tela"]),
    "tem_loop": (["o final emenda no começo", "termina com a mesma cena do início"], [None]),
    "audio_em_alta": (["usa um áudio em alta", "som viral do momento"], ["áudio original"]),
}
EFEITO_HOOK = {"pergunta": .5, "choque": .8, "promessa": .6, "historia": .4, "nenhum": -.6}
EFEITO_ESTR = {"lista": .3, "tutorial": .2, "antes_depois": .5, "storytime": .3, "vlog": -.4}
EFEITO_TEMA = {"humor": .4, "educacao": 0, "beleza": .1, "games": 0, "culinaria": .2, "esporte": -.1}


def ts(s):
    return f"[{int(s // 60):02d}:{s % 60:04.1f}]"


def um_post(i):
    v = {
        "tipo_hook": rng.choice(TIPOS, p=[.22, .18, .22, .18, .20]),
        "hook_segundos": float(np.round(np.clip(rng.gamma(2.0, 1.2), 0.3, 7.5), 1)),
        "rosto_1s": int(rng.random() < .50), "texto_na_tela": int(rng.random() < .55),
        "duracao_seg": int(rng.integers(10, 91)), "estrutura": rng.choice(ESTRUTURAS),
        "tem_loop": int(rng.random() < .25), "tema": rng.choice(TEMAS),
        "audio_em_alta": int(rng.random() < .35), "hora_postagem": int(rng.integers(0, 24)),
    }
    if v["tipo_hook"] == "nenhum":
        v["hook_segundos"] = 8.0
    n_cortes = max(1, round(rng.uniform(0.5, 8) * v["duracao_seg"] / 10))
    cortes = n_cortes / v["duracao_seg"] * 10

    # regras escondidas + sorte
    pontos = (-1.5 - 0.45 * (v["hook_segundos"] - 2) + EFEITO_HOOK[v["tipo_hook"]]
              + 0.35 * v["rosto_1s"] + 0.45 * v["texto_na_tela"]
              - 0.025 * max(v["duracao_seg"] - 30, 0) - 0.10 * (cortes - 4) ** 2
              + EFEITO_ESTR[v["estrutura"]] + 0.7 * v["tem_loop"] + EFEITO_TEMA[v["tema"]]
              + 0.55 * v["audio_em_alta"] + 0.35 * (18 <= v["hora_postagem"] <= 22)
              + rng.normal(0, 0.6))
    viral = rng.random() < 1 / (1 + np.exp(-pontos))

    # transforma as características em texto, como num post real
    a = rng.choice(ASSUNTO[v["tema"]])
    linhas, t = [], 0.0
    if v["tipo_hook"] != "nenhum":
        while t + 1.0 <= v["hook_segundos"]:
            linhas.append(f"{ts(t)} {rng.choice(ENCHIMENTO)}.")
            t += float(np.round(rng.uniform(1.0, 2.0), 1))
        linhas.append(f"{ts(v['hook_segundos'])} {rng.choice(HOOK[v['tipo_hook']]).format(a=a)}")
        t = v["hook_segundos"]
    else:
        linhas.append(f"{ts(0)} {rng.choice(ENCHIMENTO)}.")
    for _ in range(2):
        t += float(np.round(rng.uniform(2, 6), 1))
        if t < v["duracao_seg"]:
            linhas.append(f"{ts(t)} {rng.choice(CORPO)}.")

    notas = [rng.choice(NOTAS[k][0] if v[k] else NOTAS[k][1]) for k in NOTAS]
    notas = [n for n in notas if n] + [f"edição com {n_cortes} cortes"]

    seguidores = int(np.clip(rng.lognormal(9.5, 1.0), 500, 2_000_000))
    mult = rng.uniform(10, 40) if viral else min(rng.lognormal(0.2, 0.8), 9.9)
    data = datetime(2026, 1, 1) + timedelta(days=int(rng.integers(0, 280)), hours=v["hora_postagem"],
                                            minutes=int(rng.integers(0, 60)))
    return {
        "id": f"post_{i:04d}", "plataforma": str(rng.choice(["tiktok", "reels", "shorts"])),
        "legenda": f"{rng.choice(LEGENDA[v['estrutura']]).format(a=a)} {HASHTAGS[v['tema']]}",
        "transcricao": "\n".join(linhas), "notas_visuais": "; ".join(notas),
        "duracao_seg": v["duracao_seg"], "postado_em": data.isoformat(timespec="minutes"),
        "seguidores": seguidores, "views": int(seguidores * mult),
    }


if __name__ == "__main__":
    posts = [um_post(i) for i in range(1, N + 1)]
    destino = Path(__file__).with_name("posts.json")
    destino.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(posts)} posts salvos em {destino}")
