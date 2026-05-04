# Space Data Analysis Report

## 1. Meteor Detection

The meteor antenna data contains signal `Level` values over time. A meteor event is treated as an unusual upward peak: the signal becomes much stronger than the nearby background.

Method used:

1. Compute a rolling median baseline around each point.
2. Subtract the baseline from the signal to get local prominence.
3. Estimate local noise using median absolute deviation.
4. Mark points as meteor candidates when their prominence is at least 4 local sigma and at least 2 dB above the local baseline.
5. Merge nearby candidate points into one event.

This is better than using one fixed global threshold because the background signal changes over time.

Run:

```powershell
python src/01_meteor_detection.py --input data/meteor_data.csv --output outputs/meteor_events.csv
```

Result with the default settings: **52 meteor events detected**. The event list is saved in `outputs/meteor_events.csv`.

## 2. Galaxy Redshift From Tabular Data

For tabular galaxy data, the input features should be photometric measurements such as brightness or magnitude in different filters. The target is redshift `z`.

Proposed model:

- Clean the CSV and keep numeric columns.
- Use photometric columns as features.
- Split the data into training and test sets.
- Train a ridge regression model.
- Evaluate with MAE, RMSE, and bias.

MAE tells the average redshift error. RMSE penalizes large mistakes more strongly. Bias shows whether the model tends to over-predict or under-predict redshift.

Example CSV format:

```csv
u,g,r,i,z,redshift
19.12,18.44,18.01,17.82,17.70,0.082
21.03,20.12,19.58,19.21,19.04,0.214
```

Run after placing the real galaxy CSV in `data/`:

```powershell
python src/02_tabular_redshift.py --input data/galaxy_redshift.csv --target redshift --output outputs/tabular_redshift_predictions.csv
```

If the redshift column is named `z` instead of `redshift`, use:

```powershell
python src/02_tabular_redshift.py --input data/galaxy_redshift.csv --target z --output outputs/tabular_redshift_predictions.csv
```

Expected final answer for this part: the model learns a relationship between galaxy photometric bands and redshift. Its performance should be reported using MAE, RMSE, and bias on a held-out test set.

## 3. Galaxy Redshift From Images

For image-based redshift prediction, each galaxy image is converted into numerical visual features. The included script extracts simple color and structure features from each image, then trains a ridge regression model.

Useful image information includes:

- Galaxy color across bands.
- Brightness concentration.
- Approximate size and spread.
- Symmetry and structure.

A stronger final solution could use a convolutional neural network, but the provided feature-based approach is easier to explain and run on a normal laptop.

## 4. Exoplanet Transits And Tidal Locking

Tidal locking happens when a planet's rotation period becomes equal to its orbital period, so the same side always faces its star. It is important for exoplanets because it can strongly affect temperature, atmosphere, habitability, and climate.

Exoplanets can be detected from light curves using the transit method. When a planet passes in front of its star, the measured brightness drops slightly. Repeated dips with similar depth, duration, and spacing are evidence for an orbiting planet.

Planets most likely to be tidally locked are close to their stars. A practical rule is:

- orbital period less than or equal to about 10 days: likely tidally locked
- very small orbital distance, for example less than about 0.1 AU: likely tidally locked
- long-period planets farther away: less likely or require more detailed calculation

The included script detects transit-like dips from light curve CSV data and can flag likely tidal locking when orbital period or orbital distance is provided.
