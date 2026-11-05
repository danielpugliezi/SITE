// Gerado pelo notebook (passo 12.3). Não edite à mão.
window.MODELO = {
 "intercepto": -2.3202782093766117,
 "numericas": {
  "hook_segundos": {
   "media": 3.611375,
   "desvio": 2.6862085627717613,
   "peso": -1.124156035428515
  },
  "excesso_duracao": {
   "media": 22.441666666666666,
   "desvio": 19.87653383319693,
   "peso": -0.4627146178251895
  },
  "ritmo_fora_do_ideal": {
   "media": 1.8535833333333336,
   "desvio": 1.090032335784382,
   "peso": -0.3833807990207009
  }
 },
 "binarias": {
  "rosto_1s": {
   "peso": 0.11067668456012912,
   "media": 0.5045833333333334
  },
  "texto_na_tela": {
   "peso": 0.2802049604228852,
   "media": 0.5329166666666667
  },
  "tem_loop": {
   "peso": 0.7588491970208169,
   "media": 0.2525
  },
  "audio_em_alta": {
   "peso": 0.4767702903619536,
   "media": 0.35625
  },
  "horario_nobre": {
   "peso": 0.3180203569622078,
   "media": 0.20708333333333334
  }
 },
 "categoricas": {
  "tipo_hook": {
   "choque": {
    "peso": 0.14245901569740235,
    "media": 0.16916666666666666
   },
   "historia": {
    "peso": 0.12509808262061384,
    "media": 0.18
   },
   "nenhum": {
    "peso": -0.7203131852061546,
    "media": 0.21083333333333334
   },
   "pergunta": {
    "peso": 0.18514409311147864,
    "media": 0.21041666666666667
   },
   "promessa": {
    "peso": 0.26120480538421653,
    "media": 0.22958333333333333
   }
  },
  "estrutura": {
   "antes_depois": {
    "peso": 0.39670940574591823,
    "media": 0.19208333333333333
   },
   "lista": {
    "peso": 0.1519606409285349,
    "media": 0.19583333333333333
   },
   "storytime": {
    "peso": -0.026576529473949593,
    "media": 0.21375
   },
   "tutorial": {
    "peso": -0.028779192505780777,
    "media": 0.20166666666666666
   },
   "vlog": {
    "peso": -0.4997215130871577,
    "media": 0.19666666666666666
   }
  },
  "tema": {
   "beleza": {
    "peso": -0.22694537305372786,
    "media": 0.16458333333333333
   },
   "culinaria": {
    "peso": 0.26356207462747094,
    "media": 0.17083333333333334
   },
   "educacao": {
    "peso": 0.017935807332226387,
    "media": 0.16416666666666666
   },
   "esporte": {
    "peso": -0.18407992745726767,
    "media": 0.16041666666666668
   },
   "games": {
    "peso": -0.1514921698202668,
    "media": 0.15833333333333333
   },
   "humor": {
    "peso": 0.2746123999791247,
    "media": 0.18166666666666667
   }
  }
 },
 "metricas": {
  "Acurácia": 0.7733333333333333,
  "Precisão": 0.581081081081081,
  "Recall": 0.2905405405405405,
  "AUC": 0.7999880411384835
 },
 "comparacao": {
  "Dummy (sempre 'não')": {
   "Acurácia": 0.753,
   "AUC": 0.5
  },
  "Regressão Logística": {
   "Acurácia": 0.773,
   "AUC": 0.8
  },
  "Random Forest": {
   "Acurácia": 0.768,
   "AUC": 0.794
  }
 },
 "matriz": [
  [
   421,
   31
  ],
  [
   105,
   43
  ]
 ],
 "dados": {
  "total": 3000,
  "treino": 2400,
  "teste": 600,
  "taxa_viral": 0.24633333333333332
 }
};
