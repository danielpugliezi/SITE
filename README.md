# Will It Go Viral?

Machine Learning project by **Gustavo Pugliezi** (Computer Science): a Logistic Regression model, trained on **real YouTube Shorts**, that estimates whether a short video will go viral from its **hook**, **structure** and **content**.

## How to run
Both notebooks live in `notebook/` and must stay in the same folder.

1. **`collect_real_videos.ipynb`**: run it on your own computer (YouTube blocks most cloud servers). It searches YouTube Shorts in 6 topics, saves public data and automatic captions, analyses each video's frames (face in the first second, cuts, loop) and writes `posts.json` and `new_posts.json`. It takes about 30–60 minutes and resumes where it stopped.
2. **`viral_predictor.ipynb`**: the deliverable. It follows the 12-step project framework, each step explained with the "intern" analogy, and produces:

| File | Step | What it is |
|---|---|---|
| `post_extractor.py` | 4 | feature extraction (classroom rules or LLM) |
| `dataset.csv` | 5 | the dataset |
| `viral_model.pkl` | 11 | the trained model |
| `predict_app.py` | 12 | a separate app that loads the `.pkl` and predicts |

```bash
pip install -r requirements.txt
jupyter lab notebook/
```

## Presentation site
`site/index.html` is an interactive page (in Portuguese) for the presentation. It still uses the earlier simulated-data model.
