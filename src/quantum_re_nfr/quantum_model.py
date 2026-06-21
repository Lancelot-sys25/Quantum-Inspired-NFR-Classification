from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


class QuantumInspiredNFRClassifier(BaseEstimator, ClassifierMixin):
    """A compact research prototype for semantic-state label projection."""

    def __init__(self, threshold: float = 0.5, random_state: int = 42):
        self.threshold = threshold
        self.random_state = random_state
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)

    def fit(self, texts: list[str], y: np.ndarray) -> "QuantumInspiredNFRClassifier":
        x = self.vectorizer.fit_transform(texts).toarray()
        states = self._normalize_states(x)
        self.label_basis_ = self._learn_label_basis(states, y)
        self.interference_ = self._learn_interference(y)
        return self

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        x = self.vectorizer.transform(texts).toarray()
        states = self._normalize_states(x)
        amplitude = states @ self.label_basis_.T
        score = amplitude**2
        adjusted = score @ self.interference_
        return self._minmax_rows(adjusted)

    def predict(self, texts: list[str]) -> np.ndarray:
        return (self.predict_proba(texts) >= self.threshold).astype(int)

    @staticmethod
    def _normalize_states(x: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(x, axis=1, keepdims=True)
        norm[norm == 0] = 1.0
        return x / norm

    @staticmethod
    def _learn_label_basis(states: np.ndarray, y: np.ndarray) -> np.ndarray:
        basis = []
        for label_index in range(y.shape[1]):
            positive = states[y[:, label_index] == 1]
            if len(positive) == 0:
                basis.append(np.zeros(states.shape[1]))
                continue
            centroid = positive.mean(axis=0)
            norm = np.linalg.norm(centroid)
            basis.append(centroid / norm if norm else centroid)
        return np.vstack(basis)

    @staticmethod
    def _learn_interference(y: np.ndarray) -> np.ndarray:
        co_occurrence = y.T @ y
        diagonal = np.diag(co_occurrence).copy()
        diagonal[diagonal == 0] = 1
        normalized = co_occurrence / diagonal[:, None]
        return 0.85 * np.eye(y.shape[1]) + 0.15 * normalized

    @staticmethod
    def _minmax_rows(x: np.ndarray) -> np.ndarray:
        lo = x.min(axis=1, keepdims=True)
        hi = x.max(axis=1, keepdims=True)
        scale = hi - lo
        scale[scale == 0] = 1.0
        return (x - lo) / scale


class QuantumInspiredContrastiveNFRClassifier(BaseEstimator, ClassifierMixin):
    """Contrastive semantic-state projection for multi-label NFR classification.

    This variant keeps the quantum-inspired projection idea, but learns each label
    direction from the difference between positive and negative semantic centroids.
    That makes the projection more discriminative than a positive-only centroid.
    """

    def __init__(
        self,
        threshold: float = 0.5,
        random_state: int = 42,
        score_scale: float = 12.0,
        interference_weight: float = 0.05,
    ):
        self.threshold = threshold
        self.random_state = random_state
        self.score_scale = score_scale
        self.interference_weight = interference_weight
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)

    def fit(self, texts: list[str], y: np.ndarray) -> "QuantumInspiredContrastiveNFRClassifier":
        x = self.vectorizer.fit_transform(texts).toarray()
        states = self._normalize_states(x)
        self.label_basis_ = self._learn_contrastive_label_basis(states, y)
        self.label_bias_ = self._learn_label_bias(y)
        self.interference_ = QuantumInspiredNFRClassifier._learn_interference(y)
        return self

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        x = self.vectorizer.transform(texts).toarray()
        states = self._normalize_states(x)
        amplitude = states @ self.label_basis_.T
        score = self._sigmoid(self.score_scale * amplitude + self.label_bias_)
        if self.interference_weight:
            interfered = score @ self.interference_
            score = (1 - self.interference_weight) * score + self.interference_weight * interfered
        return np.clip(score, 0.0, 1.0)

    def predict(self, texts: list[str]) -> np.ndarray:
        return (self.predict_proba(texts) >= self.threshold).astype(int)

    @staticmethod
    def _normalize_states(x: np.ndarray) -> np.ndarray:
        return QuantumInspiredNFRClassifier._normalize_states(x)

    @staticmethod
    def _learn_contrastive_label_basis(states: np.ndarray, y: np.ndarray) -> np.ndarray:
        basis = []
        global_centroid = states.mean(axis=0)
        for label_index in range(y.shape[1]):
            positive = states[y[:, label_index] == 1]
            negative = states[y[:, label_index] == 0]
            if len(positive) == 0:
                direction = np.zeros(states.shape[1])
            elif len(negative) == 0:
                direction = positive.mean(axis=0) - global_centroid
            else:
                direction = positive.mean(axis=0) - negative.mean(axis=0)
            norm = np.linalg.norm(direction)
            basis.append(direction / norm if norm else direction)
        return np.vstack(basis)

    @staticmethod
    def _learn_label_bias(y: np.ndarray) -> np.ndarray:
        eps = 1e-4
        prior = np.clip(y.mean(axis=0), eps, 1 - eps)
        return 0.15 * np.log(prior / (1 - prior))

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        x = np.clip(x, -50, 50)
        return 1 / (1 + np.exp(-x))


class HybridQuantumSVMNFRClassifier(BaseEstimator, ClassifierMixin):
    """Hybrid quantum-inspired classifier with SVM score fusion.

    The model combines two signals:
    1. contrastive quantum-inspired projection scores;
    2. one-vs-rest Linear SVM decision scores.

    The fusion keeps the quantum-inspired semantic projection as an explicit
    component while using the SVM signal as a stabilizer for small datasets.
    """

    def __init__(
        self,
        threshold: float = 0.5,
        random_state: int = 42,
        quantum_weight: float = 0.30,
    ):
        self.threshold = threshold
        self.random_state = random_state
        self.quantum_weight = quantum_weight

    def fit(self, texts: list[str], y: np.ndarray) -> "HybridQuantumSVMNFRClassifier":
        self.quantum_ = QuantumInspiredContrastiveNFRClassifier(
            threshold=self.threshold,
            random_state=self.random_state,
            interference_weight=0.03,
        )
        self.quantum_.fit(texts, y)
        self.svm_ = OneVsRestClassifier(
            Pipeline(
                [
                    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
                    ("clf", LinearSVC(class_weight="balanced", dual="auto")),
                ]
            )
        )
        self.svm_.fit(texts, y)
        return self

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        quantum_score = self.quantum_.predict_proba(texts)
        svm_decision = self.svm_.decision_function(texts)
        svm_score = QuantumInspiredContrastiveNFRClassifier._sigmoid(svm_decision)
        fused = self.quantum_weight * quantum_score + (1 - self.quantum_weight) * svm_score
        return np.clip(fused, 0.0, 1.0)

    def predict(self, texts: list[str]) -> np.ndarray:
        return (self.predict_proba(texts) >= self.threshold).astype(int)
