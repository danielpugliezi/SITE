"""
viralidade.py — funções compartilhadas entre o notebook e qualquer aplicativo.

Fica num arquivo .py (e não só dentro do notebook) porque o modelo salvo em .pkl
guarda uma *referência* para `criar_features`. Quem abrir o .pkl precisa conseguir
importar este módulo.

Autor: Gustavo Pugliezi
"""
import json
import re
from datetime import datetime

import pandas as pd

# ---------------------------------------------------------------------------
# Passo 2 — definição das features mensuráveis
# Cada feature tem uma regra objetiva de medição. Esta mesma especificação é
# enviada ao LLM no passo 4, para que ele meça igual a um humano.
# ---------------------------------------------------------------------------
ESPEC_FEATURES = {
    "hook_segundos":  "número: segundo (timestamp da transcrição) da primeira frase de gancho; se não houver gancho, use 8",
    "tipo_hook":      "texto, um de: pergunta, choque, promessa, historia, nenhum",
    "rosto_1s":       "0 ou 1: aparece um rosto no primeiro segundo?",
    "texto_na_tela":  "0 ou 1: há texto escrito na tela no início?",
    "duracao_seg":    "número: duração do vídeo em segundos",
    "cortes_por_10s": "número: (número de cortes ÷ duração) × 10, com 1 casa decimal",
    "estrutura":      "texto, um de: lista, tutorial, antes_depois, storytime, vlog",
    "tem_loop":       "0 ou 1: o final emenda no começo?",
    "tema":           "texto, um de: humor, educacao, beleza, games, culinaria, esporte",
    "audio_em_alta":  "0 ou 1: usa um áudio que está em alta?",
    "hora_postagem":  "número inteiro de 0 a 23: hora em que foi postado",
}
COLUNAS = list(ESPEC_FEATURES)

# campos do post que podem ser mostrados a quem extrai as features.
# views e seguidores ficam de FORA: eles definem a resposta (label) e
# mostrá-los seria "vazar a resposta" para dentro das features.
CAMPOS_VISIVEIS = ["id", "plataforma", "legenda", "transcricao", "notas_visuais", "duracao_seg", "postado_em"]


# ---------------------------------------------------------------------------
# Passo 4a — extração com LLM (precisa de ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------
def extrair_com_llm(post, modelo="claude-haiku-5-5"):
    import anthropic
    cliente = anthropic.Anthropic()
    visivel = {k: post[k] for k in CAMPOS_VISIVEIS if k in post}
    prompt = (
        "Você é um anotador de vídeos curtos. Leia o post abaixo e meça cada feature "
        "seguindo exatamente as regras. Responda SOMENTE com um objeto JSON com estas chaves:\n"
        + json.dumps(ESPEC_FEATURES, ensure_ascii=False, indent=1)
        + "\n\nPOST:\n" + json.dumps(visivel, ensure_ascii=False, indent=1)
    )
    resposta = cliente.messages.create(model=modelo, max_tokens=500,
                                       messages=[{"role": "user", "content": prompt}])
    texto = resposta.content[0].text
    return json.loads(texto[texto.find("{"): texto.rfind("}") + 1])


# ---------------------------------------------------------------------------
# Passo 4b — extração simulada (para a sala de aula, sem internet nem chave)
# Lê os mesmos textos que o LLM leria e aplica regras de palavras-chave.
# ---------------------------------------------------------------------------
PADROES_HOOK = [  # a ordem importa: o primeiro que casar vence
    ("choque",   r"para tudo|não acredito|proibid"),
    ("promessa", r"vou te mostrar|o segredo|vai dominar"),
    ("historia", r"te contar|aconteceu|história de"),
    ("pergunta", r"\?\s*$"),
]
PADROES_ESTRUTURA = [
    ("lista", r"\d+ coisas|top \d+"), ("tutorial", r"como fazer|passo a passo"),
    ("antes_depois", r"antes e depois|transformação"), ("storytime", r"storytime|contei tudo"),
    ("vlog", r"vlog|meu dia"),
]
PADROES_TEMA = [
    ("humor", r"#humor|#comedia"), ("educacao", r"#educacao|#aprenda"), ("beleza", r"#beleza|#makeup"),
    ("games", r"#games|#gamer"), ("culinaria", r"#receita|#culinaria"), ("esporte", r"#futebol|#esporte"),
]


def _primeiro(padroes, texto, padrao="nenhum"):
    for nome, regex in padroes:
        if re.search(regex, texto, re.IGNORECASE | re.MULTILINE):
            return nome
    return padrao


def extrair_simulado(post):
    notas = post["notas_visuais"].lower()
    dur = float(post["duracao_seg"])

    # gancho: percorre a transcrição linha a linha, "[00:01.2] frase"
    tipo, segundos = "nenhum", 8.0
    for linha in post["transcricao"].split("\n"):
        m = re.match(r"\[(\d+):(\d+\.\d)\]\s*(.*)", linha)
        if not m:
            continue
        achou = _primeiro(PADROES_HOOK, m.group(3), None)
        if achou:
            tipo, segundos = achou, int(m.group(1)) * 60 + float(m.group(2))
            break

    cortes = re.search(r"(\d+) cortes", notas)
    return {
        "hook_segundos": segundos,
        "tipo_hook": tipo,
        "rosto_1s": int(bool(re.search(r"close no rosto|rosto aparece", notas))),
        "texto_na_tela": int(bool(re.search(r"texto grande|legenda escrita", notas))),
        "duracao_seg": dur,
        "cortes_por_10s": round(int(cortes.group(1)) / dur * 10, 1) if cortes else 0.0,
        "estrutura": _primeiro(PADROES_ESTRUTURA, post["legenda"], "vlog"),
        "tem_loop": int(bool(re.search(r"emenda no começo|mesma cena do início", notas))),
        "tema": _primeiro(PADROES_TEMA, post["legenda"], "humor"),
        "audio_em_alta": int(bool(re.search(r"áudio em alta|som viral", notas))),
        "hora_postagem": datetime.fromisoformat(post["postado_em"]).hour,
    }


# ---------------------------------------------------------------------------
# Passo 5 — engenharia de features (usada dentro do Pipeline salvo no .pkl)
# ---------------------------------------------------------------------------
NUMERICAS = ["hook_segundos", "excesso_duracao", "ritmo_fora_do_ideal"]
BINARIAS = ["rosto_1s", "texto_na_tela", "tem_loop", "audio_em_alta", "horario_nobre"]
CATEGORICAS = ["tipo_hook", "estrutura", "tema"]


def criar_features(d):
    """Transforma as 11 features medidas nas colunas que o modelo usa."""
    d = pd.DataFrame(d).copy()
    d["ritmo_fora_do_ideal"] = (d["cortes_por_10s"] - 4).abs()          # U invertido -> linha reta
    d["horario_nobre"] = d["hora_postagem"].between(18, 22).astype(int)  # degrau -> sim/não
    d["excesso_duracao"] = (d["duracao_seg"] - 30).clip(lower=0)         # só conta o que passa de 30 s
    return d[NUMERICAS + BINARIAS + CATEGORICAS]
