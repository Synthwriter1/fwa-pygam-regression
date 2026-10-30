# PyGAM Medicare FWA Analysis: The Shape of the Math

This repository contains the source code and methodology accompanying the Medium article analyzing over 802,000 CMS Medicare claims in California using Generalized Additive Models (PyGAM).

## Key Features
- **Memory-Safe Ingestion:** Chunked API streaming designed for large-scale public use files.
- **Continuous Regression:** Utilizing smoothing splines (`s()`) for service volume and factor terms (`f()`) for provider specialties.
- **Interpretable BIA:** Mathematically reversing log-transformations (`np.expm1`) to translate statistical variance into executive-level Budget Impact Analysis.

## Metrics
- **Out-of-Fold R²:** 0.6748
- **RMSE:** 1.0956
- **MAE:** 0.7714
