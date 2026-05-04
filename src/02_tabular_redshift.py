"""Estimate galaxy redshift from tabular photometric CSV data using ridge regression."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def train_test_split(n: int, test_fraction: float = 0.2, seed: int = 7) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    indices = rng.permutation(n)
    test_size = max(1, int(n * test_fraction))
    return indices[test_size:], indices[:test_size]


def standardize(train_x: np.ndarray, test_x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std[std == 0] = 1
    return (train_x - mean) / std, (test_x - mean) / std


def fit_ridge(x: np.ndarray, y: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    x_aug = np.c_[np.ones(len(x)), x]
    penalty = alpha * np.eye(x_aug.shape[1])
    penalty[0, 0] = 0
    return np.linalg.solve(x_aug.T @ x_aug + penalty, x_aug.T @ y)


def predict_ridge(x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return np.c_[np.ones(len(x)), x] @ weights


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    err = y_pred - y_true
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "bias": float(np.mean(err)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV containing photometric features and redshift label.")
    parser.add_argument("--target", default="redshift", help="Target column name, for example redshift or z.")
    parser.add_argument("--output", default="outputs/tabular_redshift_predictions.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if args.target not in df.columns:
        raise ValueError(f"Target column '{args.target}' was not found. Available columns: {list(df.columns)}")

    numeric = df.select_dtypes(include=[np.number]).dropna()
    y = numeric[args.target].to_numpy(dtype=float)
    x = numeric.drop(columns=[args.target]).to_numpy(dtype=float)
    feature_names = list(numeric.drop(columns=[args.target]).columns)

    train_idx, test_idx = train_test_split(len(numeric))
    train_x, test_x = standardize(x[train_idx], x[test_idx])
    weights = fit_ridge(train_x, y[train_idx])
    pred = predict_ridge(test_x, weights)
    score = metrics(y[test_idx], pred)

    out = numeric.iloc[test_idx].copy()
    out["predicted_redshift"] = pred
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)

    print(f"Features used: {', '.join(feature_names)}")
    print(f"MAE: {score['mae']:.5f}")
    print(f"RMSE: {score['rmse']:.5f}")
    print(f"Bias: {score['bias']:.5f}")
    print(f"Saved predictions to: {args.output}")


if __name__ == "__main__":
    main()

