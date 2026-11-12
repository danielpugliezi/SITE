# Will It Go Viral?

Machine Learning project by **Gustavo Pugliezi** (Computer Science): a Logistic Regression model that estimates whether a short video will go viral from its **hook**, **structure** and **content**. The data is simulated (platforms do not publish features such as "seconds until the hook"), and the notebook explains why and what that means.

## Deliverable
`notebook/viral_predictor.ipynb` follows the 12-step project framework. Open it in Jupyter Lab, VS Code or Google Colab and choose **Run All**. It is self-contained and creates, next to itself:

| File | Step | What it is |
|---|---|---|
| `posts.json` | 3 | the 3,000 posts received as JSON |
| `post_extractor.py` | 4 | feature extraction (classroom rules or LLM) |
| `dataset.csv` | 5 | the dataset |
| `new_posts.json` | 10 | brand-new posts with no answer |
| `viral_model.pkl` | 11 | the trained model |
| `predict_app.py` | 12 | terminal app that loads the `.pkl` and predicts |

## Testing your own video
After the notebook has run once, anyone with Python, `pandas` and `scikit-learn` can test a video from a terminal. Only `viral_model.pkl`, `post_extractor.py` and `predict_app.py` are needed:

```bash
cd notebook
python predict_app.py                  # asks 11 questions about your video, then explains the result
python predict_app.py new_posts.json   # predicts every post in a JSON file
```

## Presentation site
`site/index.html` is an interactive page (in Portuguese) for the presentation. Open it directly in a browser.
