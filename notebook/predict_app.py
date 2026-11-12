"""Predicts whether posts will go viral, using viral_model.pkl.

Usage:  python predict_app.py posts.json [--llm]
"""
import json
import pickle
import sys
import warnings
from pathlib import Path

import pandas as pd
import sklearn

import post_extractor as px

HERE = Path(__file__).resolve().parent


def load_model(path=HERE / "viral_model.pkl"):
    with open(path, "rb") as f:
        bundle = pickle.load(f)
    if bundle["sklearn_version"] != sklearn.__version__:
        warnings.warn(f"model saved with scikit-learn {bundle['sklearn_version']}, running {sklearn.__version__}")
    return bundle


def predict(posts, bundle, use_llm=False):
    extract = px.extract_with_llm if use_llm else px.extract_simulated
    X = pd.DataFrame([extract(p) for p in posts])[bundle["features"]]
    chances = bundle["pipeline"].predict_proba(X)[:, 1]
    return [(p.get("id", "?"), float(c), c >= bundle["threshold"]) for p, c in zip(posts, chances)]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    bundle = load_model()
    posts = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(f"{bundle['name']} (trained on {bundle['trained_on']} posts)\n")
    for post_id, chance, viral in predict(posts, bundle, use_llm="--llm" in sys.argv):
        print(f"{post_id:10s} {chance:6.1%}  {'█' * round(chance * 20):20s}  {'VIRAL' if viral else 'not viral'}")
