"""Detect transit-like dips in light curves and flag likely tidal locking."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def detect_transits(time: np.ndarray, flux: np.ndarray, sigma: float = 4.0) -> pd.DataFrame:
    finite = np.isfinite(time) & np.isfinite(flux)
    time = time[finite]
    flux = flux[finite]
    normalized = flux / np.nanmedian(flux)
    residual = normalized - 1.0
    mad = np.nanmedian(np.abs(residual - np.nanmedian(residual)))
    robust_sigma = 1.4826 * mad if mad > 0 else np.nanstd(residual)
    dip_mask = residual < -sigma * robust_sigma

    events = []
    start = None
    for i, value in enumerate(dip_mask):
        if value and start is None:
            start = i
        if start is not None and (not value or i == len(dip_mask) - 1):
            end = i - 1 if not value else i
            segment = residual[start : end + 1]
            min_i = start + int(np.argmin(segment))
            events.append(
                {
                    "event_id": len(events) + 1,
                    "start_time": float(time[start]),
                    "mid_time": float(time[min_i]),
                    "end_time": float(time[end]),
                    "depth": float(-residual[min_i]),
                    "duration": float(time[end] - time[start]),
                }
            )
            start = None
    return pd.DataFrame(events)


def likely_tidally_locked(period_days: float, semi_major_axis_au: float | None = None) -> bool:
    if period_days <= 10:
        return True
    if semi_major_axis_au is not None and semi_major_axis_au <= 0.1:
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lightcurve", required=True, help="CSV with time and flux columns.")
    parser.add_argument("--time-col", default="time")
    parser.add_argument("--flux-col", default="flux")
    parser.add_argument("--period-days", type=float, default=None, help="Known orbital period for tidal-locking check.")
    parser.add_argument("--semi-major-axis-au", type=float, default=None)
    parser.add_argument("--output", default="outputs/transit_events.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.lightcurve)
    events = detect_transits(
        pd.to_numeric(df[args.time_col], errors="coerce").to_numpy(float),
        pd.to_numeric(df[args.flux_col], errors="coerce").to_numpy(float),
    )
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.output, index=False)
    print(f"Transit-like dips detected: {len(events)}")
    print(f"Saved events to: {args.output}")
    if args.period_days is not None:
        locked = likely_tidally_locked(args.period_days, args.semi_major_axis_au)
        print(f"Likely tidally locked: {'yes' if locked else 'not enough evidence / less likely'}")


if __name__ == "__main__":
    main()

