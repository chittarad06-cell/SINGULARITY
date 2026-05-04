# SINGULARITY

## Space Data Analysis

This folder contains a complete starting solution for the four tasks in `Space Data Analysis.pdf`.

## Files

- `data/meteor_data.csv` - downloaded meteor antenna dataset.
- `src/01_meteor_detection.py` - detects and counts meteor peaks.
- `src/02_tabular_redshift.py` - trains a redshift model from CSV photometry.
- `src/03_image_redshift.py` - trains a redshift model from galaxy images plus labels.
- `src/04_exoplanet_transit_tidal_locking.py` - finds transit-like dips and flags likely tidally locked planets.
- `REPORT.md` - plain-English methods and answers you can adapt for submission.

## Run

```powershell
python src/01_meteor_detection.py --input data/meteor_data.csv --output outputs/meteor_events.csv
```

For the other tasks, place your datasets in `data/` and run the matching script with `--help` to see the required arguments.
