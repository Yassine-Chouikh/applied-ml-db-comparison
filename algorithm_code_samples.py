"""
UCLA Extension (COM SCI-X 450.1) Final Project — Code Samples
Title: Random Forest (Supervised) vs K-Means (Unsupervised)

Author: Yassine Chouikh

What this file is:
- A clean, runnable demo of the two algorithms I compared in my final report.
- Uses synthetic datasets (so anyone can run it without private data).
- Prints simple metrics + timing, and also shows the "reported" benchmark
  numbers I used in my project visuals (so everything stays consistent).

TL;DR:
- Random Forest: slower to train, but strong predictive accuracy (supervised)
- K-Means: fast + interpretable clusters, but not a predictor (unsupervised)
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# These are the benchmark numbers used in my VISUALS / write-up.
# (They’re meant to be illustrative, since timing varies by laptop.)
REPORTED_RF_TRAIN_MS = 450
REPORTED_KMEANS_TRAIN_MS = 80


@dataclass
class TimingResult:
    seconds: float

    @property
    def ms(self) -> float:
        return self.seconds * 1000.0


def _timer_start() -> float:
    return time.perf_counter()


def _timer_end(t0: float) -> TimingResult:
    return TimingResult(time.perf_counter() - t0)


def demo_random_forest(seed: int = 42) -> dict:
    print("\n" + "=" * 72)
    print("Random Forest (Supervised) — quick demo")
    print("=" * 72)

    # Synthetic classification dataset (reproducible)
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=3,
        random_state=seed,
    )

    print(f"Dataset: {X.shape[0]} rows × {X.shape[1]} features | classes={len(np.unique(y))}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )

    # Reasonable defaults for a student project.
    # (Not trying to hyper-optimize—just demonstrating the idea.)
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        random_state=seed,
        n_jobs=-1,
    )

    t0 = _timer_start()
    model.fit(X_train, y_train)
    fit_time = _timer_end(t0)

    t0 = _timer_start()
    y_pred = model.predict(X_test)
    pred_time = _timer_end(t0)

    acc = accuracy_score(y_test, y_pred)

    print("\nResults (measured locally):")
    print(f"- Train time: {fit_time.ms:.1f} ms")
    print(f"- Predict time: {pred_time.ms:.1f} ms ({pred_time.ms / len(X_test):.3f} ms/sample)")
    print(f"- Accuracy: {acc:.3f}")

    print("\nClassification report (quick sanity check):")
    print(classification_report(y_test, y_pred, digits=3))

    # Feature importance = one of the nicest “interpretability-ish” things
    # you can show with Random Forest.
    importances = pd.DataFrame(
        {
            "feature": [f"feature_{i}" for i in range(X.shape[1])],
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    print("Top 8 feature importances:")
    print(importances.head(8).to_string(index=False))

    # Keep the project consistent with your visuals:
    print("\nNumbers used in my project visuals (for consistency):")
    print(f"- Reported RF training time: {REPORTED_RF_TRAIN_MS} ms (illustrative benchmark)")

    return {
        "accuracy": acc,
        "train_ms_measured": fit_time.ms,
        "train_ms_reported": REPORTED_RF_TRAIN_MS,
    }


def demo_kmeans(seed: int = 42) -> dict:
    print("\n" + "=" * 72)
    print("K-Means (Unsupervised) — quick demo")
    print("=" * 72)

    # Synthetic clustering dataset (reproducible)
    X, _true_labels = make_blobs(
        n_samples=1000,
        n_features=10,
        centers=4,
        cluster_std=1.5,
        random_state=seed,
    )
    print(f"Dataset: {X.shape[0]} rows × {X.shape[1]} features | target clusters ≈ 4")

    # K-Means uses distance → scaling matters
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    km = KMeans(
        n_clusters=4,
        init="k-means++",
        n_init=10,
        max_iter=300,
        random_state=seed,
    )

    t0 = _timer_start()
    labels = km.fit_predict(X_scaled)
    fit_time = _timer_end(t0)

    sil = silhouette_score(X_scaled, labels)
    inertia = km.inertia_

    unique, counts = np.unique(labels, return_counts=True)

    print("\nResults (measured locally):")
    print(f"- Train time: {fit_time.ms:.1f} ms")
    print(f"- Iterations until convergence: {km.n_iter_}")
    print(f"- Silhouette score: {sil:.3f}  (closer to 1 = nicer clusters)")
    print(f"- Inertia: {inertia:.1f} (lower = tighter clusters)")

    print("\nCluster sizes:")
    for c, n in zip(unique, counts):
        print(f"- cluster {c}: {n} points ({(n / len(labels)) * 100:.1f}%)")

    print("\nNumbers used in my project visuals (for consistency):")
    print(f"- Reported K-Means training time: {REPORTED_KMEANS_TRAIN_MS} ms (illustrative benchmark)")

    return {
        "silhouette": sil,
        "train_ms_measured": fit_time.ms,
        "train_ms_reported": REPORTED_KMEANS_TRAIN_MS,
    }


def quick_takeaways() -> None:
    print("\n" + "=" * 72)
    print("So… when would I use which one?")
    print("=" * 72)

    print("\nRandom Forest (supervised) is great when:")
    print("- you have labels/outcomes (diagnosis yes/no, readmitted yes/no, etc.)")
    print("- you want strong accuracy with minimal tuning")
    print("- you want feature importance as a starting point for interpretability")

    print("\nK-Means (unsupervised) is great when:")
    print("- you DON'T have labels and you’re exploring patterns")
    print("- you want fast segmentation (patient groups, behavior groups, etc.)")
    print("- you need results you can explain easily (centroids / cluster profiles)")

    print("\nBonus: a realistic workflow is often:")
    print("1) cluster first (explore groups), then")
    print("2) train a supervised model (predict outcomes), then")
    print("3) validate the heck out of it.")


def main() -> None:
    print("=" * 72)
    print("ML Algorithm Comparison — portfolio demo")
    print("Author: Yassine Chouikh")
    print("=" * 72)

    rf_out = demo_random_forest()
    km_out = demo_kmeans()

    print("\n" + "=" * 72)
    print("Tiny timing recap (measured vs reported-for-visuals)")
    print("=" * 72)
    print(f"Random Forest train: measured ~{rf_out['train_ms_measured']:.1f} ms | reported {rf_out['train_ms_reported']} ms")
    print(f"K-Means train:       measured ~{km_out['train_ms_measured']:.1f} ms | reported {km_out['train_ms_reported']} ms")

    quick_takeaways()

    print("\nDone. If you’re reading this on GitHub: hiii :D")


if __name__ == "__main__":
    main()

