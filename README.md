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

## Part 3: Galaxy Redshift From Images

Part 3 predicts galaxy redshift using image-based galaxy features. A small sample image dataset is included here:

```text
data/sample_galaxy_images/
data/sample_image_redshift_labels.csv
```

Run the sample:

```powershell
python src/03_image_redshift.py --labels data/sample_image_redshift_labels.csv --image-root data --output outputs/sample_image_redshift_predictions.csv
```

The labels CSV must contain:

- `image` - image path
- `redshift` - target redshift value

The script extracts visual features such as color, brightness spread, and galaxy center, then trains a ridge regression model. The sample run produced:

- MAE: `0.00902`
- RMSE: `0.00902`
- Bias: `-0.00902`

## Part 4

For Part 4, place the needed light curve dataset in `data/` and run the matching script with `--help` to see the required arguments.
