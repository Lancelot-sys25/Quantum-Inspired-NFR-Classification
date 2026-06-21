from __future__ import annotations

import importlib.util

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier


def sentence_transformers_available() -> bool:
    return importlib.util.find_spec("sentence_transformers") is not None


class SentenceBertLogisticRegressionClassifier(BaseEstimator, ClassifierMixin):
    """Sentence-BERT embeddings followed by one-vs-rest Logistic Regression."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        max_iter: int = 3000,
        random_state: int = 42,
    ):
        self.model_name = model_name
        self.max_iter = max_iter
        self.random_state = random_state

    def fit(self, texts: list[str], y: np.ndarray) -> "SentenceBertLogisticRegressionClassifier":
        from sentence_transformers import SentenceTransformer

        self.encoder_ = SentenceTransformer(self.model_name)
        embeddings = self.encoder_.encode(list(texts), show_progress_bar=False)
        self.classifier_ = OneVsRestClassifier(
            LogisticRegression(
                max_iter=self.max_iter,
                class_weight="balanced",
                random_state=self.random_state,
            )
        )
        self.classifier_.fit(embeddings, y)
        return self

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        embeddings = self.encoder_.encode(list(texts), show_progress_bar=False)
        if hasattr(self.classifier_, "predict_proba"):
            return self.classifier_.predict_proba(embeddings)
        decision = self.classifier_.decision_function(embeddings)
        return 1 / (1 + np.exp(-decision))

    def predict(self, texts: list[str]) -> np.ndarray:
        return self.classifier_.predict(self.encoder_.encode(list(texts), show_progress_bar=False))
