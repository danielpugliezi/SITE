"""Tests one YouTube Short with the trained model (viral_model.pkl).

Usage:
    python test_video.py <shorts link> <topic> [--cookies chrome]

    topic: humor, education, beauty, gaming, cooking or sports

Example:
    python test_video.py https://www.youtube.com/shorts/abc123XYZ cooking

Needs viral_model.pkl and post_extractor.py in this folder (both are created by viral_predictor.ipynb).
Author: Gustavo Pugliezi
"""
import json
import os
import pickle
import sys
import tempfile
from datetime import date

import cv2
import pandas as pd
import yt_dlp

import post_extractor as px

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS = sorted(px.ALLOWED["topic"])
FACE_MODEL = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def read_transcript(info):
    subs = info.get("requested_subtitles") or {}
    for lang in ("pt-orig", "pt", "en-orig", "en"):
        path = (subs.get(lang) or {}).get("filepath")
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                events = json.load(f).get("events", [])
            lines = []
            for e in events:
                text = "".join(s.get("utf8", "") for s in e.get("segs", []) or []).replace("\n", " ").strip()
                if text:
                    t = e.get("tStartMs", 0) / 1000
                    lines.append(f"[{int(t // 60):02d}:{t % 60:04.1f}] {text}")
            return "\n".join(lines)
    return ""


def analyse_video(path):
    """Same measurements as collect_real_videos.ipynb: face in the first second, cuts, loop."""
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    previous_hist, first_small, last_small = None, None, None
    cuts, faces, index = 0, 0, 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, (96, 160))
        hist = cv2.calcHist([cv2.cvtColor(small, cv2.COLOR_BGR2HSV)], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        if previous_hist is not None and cv2.compareHist(previous_hist, hist, cv2.HISTCMP_CORREL) < 0.55:
            cuts += 1
        previous_hist = hist
        first_small = small if first_small is None else first_small
        last_small = small
        if index < fps and index % max(1, int(fps // 4)) == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found = FACE_MODEL.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                                minSize=(gray.shape[1] // 8, gray.shape[1] // 8))
            faces += len(found) > 0
        index += 1
    cap.release()
    if first_small is None:
        raise ValueError("the video could not be read")
    a = cv2.calcHist([cv2.cvtColor(first_small, cv2.COLOR_BGR2HSV)], [0, 1], None, [16, 16], [0, 180, 0, 256])
    b = cv2.calcHist([cv2.cvtColor(last_small, cv2.COLOR_BGR2HSV)], [0, 1], None, [16, 16], [0, 180, 0, 256])
    similarity = float(cv2.compareHist(cv2.normalize(a, a), cv2.normalize(b, b), cv2.HISTCMP_CORREL))
    return {"face_first_second": int(faces >= 2), "cuts": cuts, "has_loop": int(similarity >= 0.9)}


def fetch_post(url, topic, cookies=None):
    work = tempfile.mkdtemp(prefix="short_")
    options = {
        "quiet": True, "no_warnings": True, "noprogress": True,
        "format": "bv*[height<=480][ext=mp4]/bv*[height<=480]/b[height<=480]/wv*/w",
        "outtmpl": os.path.join(work, "%(id)s.%(ext)s"),
        "writeautomaticsub": True, "subtitleslangs": ["pt-orig", "pt", "en-orig", "en"], "subtitlesformat": "json3",
    }
    if cookies:
        options["cookiesfrombrowser"] = (cookies,)
    with yt_dlp.YoutubeDL(options) as y:
        info = y.extract_info(url, download=True)
    video = next(os.path.join(work, f) for f in os.listdir(work) if f.endswith((".mp4", ".webm", ".mkv")))
    post = {
        "id": info["id"], "title": info.get("title") or "", "description": (info.get("description") or "")[:500],
        "transcript": read_transcript(info), "duration_s": info.get("duration"),
        "posted_date": info.get("upload_date") or date.today().strftime("%Y%m%d"), "topic": topic,
        "video_analysis": analyse_video(video),
    }
    for f in os.listdir(work):
        os.remove(os.path.join(work, f))
    os.rmdir(work)
    return post


if __name__ == "__main__":
    args, cookies = sys.argv[1:], None
    if "--cookies" in args:
        position = args.index("--cookies")
        cookies = args[position + 1] if position + 1 < len(args) else None
        args = args[:position] + args[position + 2:]
    if len(args) != 2 or args[1] not in TOPICS or ("--cookies" in sys.argv and not cookies):
        sys.exit(__doc__)
    url, topic = args

    with open(os.path.join(HERE, "viral_model.pkl"), "rb") as f:
        bundle = pickle.load(f)

    print("Downloading and analysing the video...")
    try:
        post = fetch_post(url, topic, cookies)
    except yt_dlp.utils.DownloadError as error:
        hint = "\nTip: add --cookies chrome (or edge/firefox) to use your browser's YouTube login." if "bot" in str(error) else ""
        sys.exit(f"Could not download the video: {error}{hint}")
    features = px.extract(post)
    chance = bundle["pipeline"].predict_proba(pd.DataFrame([features])[bundle["features"]])[0, 1]

    print(f"\n{post['title']}\n")
    for name, value in features.items():
        print(f"  {name:18s} {value}")
    print(f"\nChance of going viral: {chance:.1%}  →  {'VIRAL' if chance >= bundle['threshold'] else 'not viral'}")
