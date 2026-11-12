# Will It Go Viral?

Machine Learning project by **Gustavo Pugliezi** (Computer Science): a Logistic Regression model that estimates whether a short video will go viral from its **hook**, **structure** and **content**.

## Deliverable
`notebook/viral_predictor.ipynb` follows the 12-step project framework and is self-contained. Open it in Jupyter Lab, VS Code or Google Colab and choose **Run All**. It needs no other files and writes everything it produces into its own folder:

| File | Created in | What it is |
|---|---|---|
| `posts.json` | Step 3 | the 3,000 (simulated) posts received as JSON |
| `post_extractor.py` | Step 4 | feature extraction: LLM or classroom simulation |
| `dataset.csv` | Step 5 | the dataset |
| `new_posts.json` | Step 10 | brand-new posts with no answer |
| `viral_model.pkl` | Step 11 | the trained model |
| `predict_app.py` | Step 12 | a separate app that loads the `.pkl` and predicts |

```bash
pip install -r requirements.txt
jupyter lab notebook/viral_predictor.ipynb

cd notebook
python predict_app.py new_posts.json
```

## Presentation site
`site/index.html` is an interactive page (in Portuguese) for the presentation. Open it directly in a browser.
