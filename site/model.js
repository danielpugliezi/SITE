// Gerado automaticamente pelo notebook (seção 11). Não edite à mão.
window.MODELO = {
 "intercepto": -1.967733184554639,
 "numericas": {
  "hook_segundos": {
   "media": 2.41425,
   "desvio": 1.6821579208960535,
   "peso": -0.5574179588730855
  },
  "excesso_duracao": {
   "media": 21.864166666666666,
   "desvio": 20.14989369630079,
   "peso": -0.5256248527998612
  },
  "ritmo_fora_do_ideal": {
   "media": 1.8974583333333332,
   "desvio": 1.1016719293558113,
   "peso": -0.3620829935982562
  }
 },
 "binarias": {
  "rosto_1s": {
   "peso": 0.3960068558454732,
   "media": 0.5066666666666667
  },
  "texto_na_tela": {
   "peso": 0.5024867146367293,
   "media": 0.5433333333333333
  },
  "tem_loop": {
   "peso": 0.5451397404193784,
   "media": 0.2504166666666667
  },
  "audio_em_alta": {
   "peso": 0.5008298453612303,
   "media": 0.365
  },
  "horario_nobre": {
   "peso": 0.1563156515383144,
   "media": 0.2075
  }
 },
 "categoricas": {
  "tipo_hook": {
   "choque": {
    "peso": 0.4557708504677702,
    "media": 0.17875
   },
   "historia": {
    "peso": 0.07530463331451843,
    "media": 0.18875
   },
   "nenhum": {
    "peso": -0.8249653706657628,
    "media": 0.19333333333333333
   },
   "pergunta": {
    "peso": 0.17117674412677192,
    "media": 0.21541666666666667
   },
   "promessa": {
    "peso": 0.12157837624383419,
    "media": 0.22375
   }
  },
  "estrutura": {
   "antes_depois": {
    "peso": 0.36593590778376156,
    "media": 0.18916666666666668
   },
   "lista": {
    "peso": 0.16938054602173067,
    "media": 0.19208333333333333
   },
   "storytime": {
    "peso": 0.2692754336938191,
    "media": 0.21625
   },
   "tutorial": {
    "peso": -0.025595952534807037,
    "media": 0.18791666666666668
   },
   "vlog": {
    "peso": -0.7801307014773706,
    "media": 0.21458333333333332
   }
  },
  "tema": {
   "beleza": {
    "peso": 0.11810360423762147,
    "media": 0.1625
   },
   "culinaria": {
    "peso": -0.06686245155632749,
    "media": 0.16625
   },
   "educacao": {
    "peso": 0.04592713688344923,
    "media": 0.15958333333333333
   },
   "esporte": {
    "peso": -0.2606428035770892,
    "media": 0.16
   },
   "games": {
    "peso": -0.1096897960754612,
    "media": 0.17375
   },
   "humor": {
    "peso": 0.2720295435749511,
    "media": 0.17791666666666667
   }
  }
 },
 "metricas": {
  "Acurácia": 0.745,
  "Precisão": 0.602,
  "Recall": 0.326,
  "F1": 0.423,
  "AUC": 0.772
 },
 "comparacao": {
  "Dummy (sempre 'não')": {
   "Acurácia": 0.713,
   "Precisão": 0.0,
   "Recall": 0.0,
   "F1": 0.0,
   "AUC": 0.5
  },
  "Regressão Logística": {
   "Acurácia": 0.745,
   "Precisão": 0.602,
   "Recall": 0.326,
   "F1": 0.423,
   "AUC": 0.772
  },
  "Árvore de Decisão": {
   "Acurácia": 0.728,
   "Precisão": 0.533,
   "Recall": 0.419,
   "F1": 0.469,
   "AUC": 0.71
  },
  "Random Forest": {
   "Acurácia": 0.75,
   "Precisão": 0.704,
   "Recall": 0.221,
   "F1": 0.336,
   "AUC": 0.772
  }
 },
 "matriz": [
  [
   391,
   37
  ],
  [
   116,
   56
  ]
 ],
 "dados": {
  "total": 3000,
  "treino": 2400,
  "teste": 600,
  "taxa_viral": 0.2866666666666667,
  "taxa_por_hook": {
   "choque": 0.373,
   "historia": 0.281,
   "nenhum": 0.16,
   "pergunta": 0.308,
   "promessa": 0.311
  },
  "taxa_por_gancho_seg": {
   "-0.001–1": 0.396,
   "1–2": 0.326,
   "2–3": 0.288,
   "3–4": 0.205,
   "4–5": 0.135,
   "5–7": 0.113,
   "7–10": 0.066
  }
 }
};
