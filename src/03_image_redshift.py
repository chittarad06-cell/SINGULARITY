"""Estimate galaxy redshift from image-derived features.

Expected labels CSV columns:
- image: relative or absolute image path
- redshift: target z value
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

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


def image_features(path: Path, size: int = 64) -> np.ndarray:
    image = Image.open(path).convert("RGB").resize((size, size))
    arr = np.asarray(image, dtype=float) / 255.0
    features = []
    for channel in range(3):
        values = arr[:, :, channel].ravel()
        features.extend(
            [
                values.mean(),
                values.std(),
                np.percentile(values, 10),
                np.percentile(values, 50),
                np.percentile(values, 90),
            ]
        )
    gray = arr.mean(axis=2)
    y_grid, x_grid = np.indices(gray.shape)
    total = gray.sum() + 1e-12
    cx = float((x_grid * gray).sum() / total)
    cy = float((y_grid * gray).sum() / total)
    radius = np.sqrt((x_grid - cx) ** 2 + (y_grid - cy) ** 2)
    features.extend([cx / size, cy / size, float((radius * gray).sum() / total) / size])
    return np.array(features, dtype=float)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", required=True, help="CSV with image and redshift columns.")
    parser.add_argument("--image-root", default=".", help="Base folder for relative image paths.")
    parser.add_argument("--output", default="outputs/image_redshift_predictions.csv")
    args = parser.parse_args()

    labels = pd.read_csv(args.labels).dropna(subset=["image", "redshift"])
    root = Path(args.image_root)
    x = []
    kept_rows = []
    for _, row in labels.iterrows():
        image_path = Path(row["image"])
        if not image_path.is_absolute():
            image_path = root / image_path
        if image_path.exists():
            x.append(image_features(image_path))
            kept_rows.append(row)

    if not x:
        raise ValueError("No readable image files were found from the labels CSV.")

    data = pd.DataFrame(kept_rows)
    x_arr = np.vstack(x)
    y = data["redshift"].to_numpy(dtype=float)
    train_idx, test_idx = train_test_split(len(data))
    train_x, test_x = standardize(x_arr[train_idx], x_arr[test_idx])
    weights = fit_ridge(train_x, y[train_idx])
    pred = predict_ridge(test_x, weights)
    score = metrics(y[test_idx], pred)

    out = data.iloc[test_idx].copy()
    out["predicted_redshift"] = pred
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"Images used: {len(data)}")
    print(f"MAE: {score['mae']:.5f}")
    print(f"RMSE: {score['rmse']:.5f}")
    print(f"Bias: {score['bias']:.5f}")
    print(f"Saved predictions to: {args.output}")


if __name__ == "__main__":
    main()
