import pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarSearch:
    def __init__(self, csv_path="data/past_tickets.csv"):
        self.df = pd.read_csv(csv_path)
        texts = (self.df["title"].fillna("") + " " + self.df["body"].fillna("")).tolist()
        self.vec = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.mat = self.vec.fit_transform(texts)

    def topk(self, query: str, k: int = 5):
        q = self.vec.transform([query])
        sims = cosine_similarity(self.mat, q).ravel()
        idx = sims.argsort()[-k:][::-1]
        return self.df.iloc[idx][["ticket_id","title","body","area","tags"]].to_dict("records")
