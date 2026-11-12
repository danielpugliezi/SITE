"""Predicts whether a short video will go viral, using viral_model.pkl.

Usage:
    python predict_app.py                    asks questions about YOUR video
    python predict_app.py posts.json         predicts every post in a JSON file
    python predict_app.py posts.json --llm   same, but an LLM reads the posts (needs ANTHROPIC_API_KEY)
"""
import json
import pickle
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn

import post_extractor as px

HERE = Path(__file__).resolve().parent

HOOK_TYPES = [("question", 'Question      ("Did you know...?")'), ("shock", 'Shock         ("STOP EVERYTHING!")'),
              ("promise", 'Promise       ("I\'ll show you...")'), ("story", 'Story         ("Let me tell you...")'),
              ("none", "No hook, it starts slowly")]
STRUCTURES = [("list", 'List          ("3 things about...", "Top 5")'), ("tutorial", 'Tutorial      ("How to...")'),
              ("before_after", "Before and after"), ("storytime", "Storytime"), ("vlog", "Vlog / a day in my life")]
TOPICS = [("humor", "Humor"), ("education", "Education"), ("beauty", "Beauty"),
          ("gaming", "Gaming"), ("cooking", "Cooking"), ("sports", "Sports")]
LABELS = {"hook_seconds": "hook timing", "hook_type": "hook type", "face_first_second": "face in the first second",
          "text_on_screen": "text on screen", "duration_s": "duration", "cuts_per_10s": "editing pace",
          "structure": "format", "has_loop": "loop ending", "topic": "topic", "trending_audio": "trending audio",
          "post_hour": "posting hour"}


def load_model(path=HERE / "viral_model.pkl"):
    with open(path, "rb") as f:
        bundle = pickle.load(f)
    if bundle["sklearn_version"] != sklearn.__version__:
        warnings.warn(f"model saved with scikit-learn {bundle['sklearn_version']}, running {sklearn.__version__}")
    return bundle


def predict(posts, bundle, use_llm=False):
    """Mode 2: posts written as JSON (caption, transcript, visual notes...)."""
    extract = px.extract_with_llm if use_llm else px.extract_simulated
    X = pd.DataFrame([extract(p) for p in posts])[bundle["features"]]
    chances = bundle["pipeline"].predict_proba(X)[:, 1]
    return [(p.get("id", "?"), float(c), c >= bundle["threshold"]) for p, c in zip(posts, chances)]


# ---------------------------------------------------------------- mode 1: questions
def ask(prompt):
    raw = input(prompt + " ").strip()
    if not sys.stdin.isatty():
        print(raw)   # when answers come from a pipe, echo them so the output reads like a conversation
    return raw


def ask_number(prompt, low, high, integer=False):
    while True:
        raw = ask(prompt).replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            print(f"  Please type a number between {low} and {high}.")
            continue
        if not low <= value <= high:
            print(f"  Please type a number between {low} and {high}.")
        elif integer and value != int(value):
            print("  Please type a whole number.")
        else:
            return int(value) if integer else value


def ask_yes_no(prompt):
    while True:
        raw = ask(prompt + " (y/n)").lower()
        if raw in ("y", "yes", "s", "sim"):
            return 1
        if raw in ("n", "no", "nao", "não"):
            return 0
        print("  Please type y or n.")


def ask_choice(prompt, options):
    print(prompt)
    for number, (_, label) in enumerate(options, 1):
        print(f"  {number}) {label}")
    while True:
        raw = ask("  Type the number:")
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print(f"  Please type a number from 1 to {len(options)}.")


def ask_about_video():
    print("Answer a few questions about your video.\n")
    duration = ask_number("1. How long is the video, in seconds?", 3, 600)
    if not 10 <= duration <= 90:
        print("   Note: the model learned from videos of 10 to 90 s, so the result is less reliable.")
    cuts = ask_number("2. How many cuts (scene changes) does it have?", 0, 500, integer=True)
    pace = round(cuts / duration * 10, 1)
    if not 0.5 <= pace <= 8:
        print(f"   Note: that is {pace} cuts per 10 s; the model saw 0.5 to 8, so the result is less reliable.")
    hook_type = ask_choice("3. What kind of hook opens the video?", HOOK_TYPES)
    hook_seconds = 8.0 if hook_type == "none" else ask_number("4. At which second does the hook sentence start?", 0, 60)
    return {
        "hook_seconds": hook_seconds,
        "hook_type": hook_type,
        "face_first_second": ask_yes_no("5. Does a face appear in the first second?"),
        "text_on_screen": ask_yes_no("6. Is there written text on screen at the start?"),
        "duration_s": duration,
        "cuts_per_10s": pace,
        "structure": ask_choice("7. What is the format?", STRUCTURES),
        "has_loop": ask_yes_no("8. Does the ending loop back to the beginning?"),
        "topic": ask_choice("9. What is the topic?", TOPICS),
        "trending_audio": ask_yes_no("10. Does it use a trending sound?"),
        "post_hour": ask_number("11. At what hour will it be posted? (0-23)", 0, 23, integer=True),
    }


def explain(features, bundle):
    """Points each feature added or removed compared with an average training video."""
    pipeline = bundle["pipeline"]
    x = pipeline.named_steps["preprocess"].transform(pd.DataFrame([features])[bundle["features"]])
    x = x.toarray() if hasattr(x, "toarray") else np.asarray(x)
    points = pipeline.named_steps["model"].coef_[0] * (x[0] - bundle["column_means"])
    by_feature = {}
    for source, value in zip(bundle["column_source"], points):
        by_feature[source] = by_feature.get(source, 0.0) + float(value)
    return sorted(by_feature.items(), key=lambda item: item[1])


def show_result(features, bundle):
    chance = float(bundle["pipeline"].predict_proba(pd.DataFrame([features])[bundle["features"]])[0, 1])
    verdict = "VIRAL" if chance >= bundle["threshold"] else "not viral"
    print("\n" + "=" * 52)
    print(f"Chance of going viral: {chance:.1%}   {'█' * round(chance * 20):<20s}  →  {verdict}")
    print(f"(an average video in the training data has about {bundle['average_chance']:.0%})")
    print("=" * 52)
    ranking = explain(features, bundle)
    helped = [(n, p) for n, p in reversed(ranking) if p > 0.05][:3]
    hurt = [(n, p) for n, p in ranking if p < -0.05][:3]
    if helped:
        print("\nWhat helped:")
        for name, points in helped:
            print(f"  + {LABELS[name]:26s} {points:+.2f} points")
    if hurt:
        print("\nWhat hurt:")
        for name, points in hurt:
            print(f"  - {LABELS[name]:26s} {points:+.2f} points")
    print("\nTip: run it again changing one answer to see how much that single choice is worth.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bundle = load_model()
    print(f"{bundle['name']} (trained on {bundle['trained_on']} videos)\n")
    try:
        if not args:
            show_result(px.validate_features(ask_about_video()), bundle)
        else:
            posts = json.loads(Path(args[0]).read_text(encoding="utf-8"))
            for post_id, chance, viral in predict(posts, bundle, use_llm="--llm" in sys.argv):
                print(f"{post_id:10s} {chance:6.1%}  {'█' * round(chance * 20):20s}  {'VIRAL' if viral else 'not viral'}")
    except (EOFError, KeyboardInterrupt):
        print("\nStopped.")
    except ValueError as error:
        sys.exit(f"Problem with the information given: {error}")
