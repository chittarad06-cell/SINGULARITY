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

## Part 1: Meteor Detection

```powershell
python src/01_meteor_detection.py --input data/meteor_data.csv --output outputs/meteor_events.csv
```

Result: **52 meteor events detected**. The detected events are saved in `outputs/meteor_events.csv`.

## Part 2: Galaxy Redshift From CSV Data

Part 2 predicts galaxy redshift using tabular photometric data. A sample CSV is included here:

```text
data/sample_tabular_redshift.csv
```

Run the sample:

```powershell
python src/02_tabular_redshift.py --input data/sample_tabular_redshift.csv --target redshift --output outputs/sample_tabular_redshift_predictions.csv
```

For the real Part 2 dataset, replace the sample file with the actual galaxy CSV. The CSV should contain brightness columns such as `u`, `g`, `r`, `i`, `z`, plus a target column named `redshift` or `z`.

The script reports:

- MAE
- RMSE
- Bias

## Remaining Parts

For Parts 3 and 4, place the needed datasets in `data/` and run the matching script with `--help` to see the required arguments.
