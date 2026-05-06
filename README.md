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

## Part 4: Exoplanet Transit Detection And Tidal Locking

Part 4 detects exoplanets from light curve data. A light curve is a table of star brightness over time. When a planet passes in front of the star, the brightness drops slightly, creating a transit dip.

A sample light curve is included:

```text
data/sample_lightcurve.csv
```

Run the sample:

```powershell
python src/04_exoplanet_transit_tidal_locking.py --lightcurve data/sample_lightcurve.csv --time-col time --flux-col flux --period-days 3.2 --semi-major-axis-au 0.045 --output outputs/sample_transit_events.csv
```

Sample result:

- Transit-like dips detected: `8`
- Likely tidally locked: `yes`

This planet is likely tidally locked because its orbital period is short and it orbits very close to its star.
