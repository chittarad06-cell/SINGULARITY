"""Detect meteor events as unusual local peaks in antenna signal level."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def contiguous_regions(mask: np.ndarray) -> list[tuple[int, int]]:
    regions: list[tuple[int, int]] = []
    start = None
    for i, value in enumerate(mask):
        if value and start is None:
            start = i
        if start is not None and (not value or i == len(mask) - 1):
            end = i - 1 if not value else i
            regions.append((start, end))
            start = None
    return regions


def merge_close_regions(regions: list[tuple[int, int]], max_gap: int) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in regions:
        if merged and start - merged[-1][1] <= max_gap:
            merged[-1] = (merged[-1][0], end)
        else:
            merged.append((start, end))
    return merged


def detect_meteors(
    df: pd.DataFrame,
    level_col: str = "Level",
    window: int = 101,
    z_threshold: float = 4.0,
    min_prominence_db: float = 2.0,
    merge_gap: int = 5,
) -> pd.DataFrame:
    signal = pd.to_numeric(df[level_col], errors="coerce")
    baseline = signal.rolling(window, center=True, min_periods=max(5, window // 5)).median()
    residual = signal - baseline

    local_mad = residual.abs().rolling(window, center=True, min_periods=max(5, window // 5)).median()
    local_sigma = (1.4826 * local_mad).fillna(1.4826 * residual.abs().median())
    threshold = np.maximum(z_threshold * local_sigma, min_prominence_db)
    peak_mask = (residual > threshold).fillna(False).to_numpy()

    regions = merge_close_regions(contiguous_regions(peak_mask), merge_gap)
    events = []
    for event_id, (start, end) in enumerate(regions, start=1):
        segment = df.iloc[start : end + 1].copy()
        peak_idx = pd.to_numeric(segment[level_col], errors="coerce").idxmax()
        events.append(
            {
                "event_id": event_id,
                "start_index": start,
                "end_index": end,
                "peak_index": int(peak_idx),
                "start_time": df.loc[start, "Time"] if "Time" in df else start,
                "peak_time": df.loc[peak_idx, "Time"] if "Time" in df else int(peak_idx),
                "end_time": df.loc[end, "Time"] if "Time" in df else end,
                "peak_level": float(signal.loc[peak_idx]),
                "local_baseline": float(baseline.loc[peak_idx]),
                "prominence_db": float(residual.loc[peak_idx]),
            }
        )
    return pd.DataFrame(events)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Meteor CSV file.")
    parser.add_argument("--output", default="outputs/meteor_events.csv", help="Detected event CSV.")
    parser.add_argument("--z-threshold", type=float, default=4.0)
    parser.add_argument("--min-prominence-db", type=float, default=2.0)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    events = detect_meteors(
        df,
        z_threshold=args.z_threshold,
        min_prominence_db=args.min_prominence_db,
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.output, index=False)
    print(f"Detected meteors: {len(events)}")
    print(f"Saved events to: {args.output}")


if __name__ == "__main__":
    main()

