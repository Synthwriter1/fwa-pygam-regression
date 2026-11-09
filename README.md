# FWA Claims Pipeline: PyGAM & The Shape of the Math

**Companion Essay:** [The Shape of the Math: How PyGAM Exposed the Hidden Curve Inside 802,000 Medicare Claims](link-to-medium-article)

## Project Overview
In healthcare fraud, waste, and abuse (FWA) auditing, intuition is a liability. Traditional linear models assume that financial exposure grows at a constant rate as provider volume increases, creating massive blind spots when analyzing extreme-volume billing entities. 

The `fwa-claims-pipeline` is an open-source analytics architecture designed to detect complex claims variance and unpredictable billing behaviors that evade traditional linear audits. Built on a dataset of over 802,000 California CMS Medicare claims, this pipeline leverages transparent, "glass-box" statistical models—specifically Generalized Additive Models (PyGAM).

By mapping the exact volume thresholds where financial exposure accelerates and confidence intervals explode, this architecture translates abstract statistical uncertainty into precise, legally defensible risk-exposure intelligence.

## Key Technical Features
- **Memory-Safe Ingestion:** Utilizes chunked API streaming designed specifically for processing large-scale public use files without memory bottlenecking.
- **Continuous Regression:** Leverages PyGAM smoothing splines (`s()`) for nonlinear service volume mapping and factor terms (`f()`) for categorical provider specialties.
- **Interpretable BIA:** Mathematically reverses log-transformations (`np.expm1`) to translate raw statistical variance into highly interpretable, executive-level Budget Impact Analysis (BIA) dollar amounts.

## Architecture Flow

### 1. Data Ingestion & Preprocessing
* Cleans and structures raw Medicare provider utilization data, handling null values, standardizing National Provider Identifiers (NPIs), and aggregating service volumes.

### 2. Glass-Box Detection (The Core Engine)
* **PyGAM Non-Linear Mapping:** Isolates aggressive financial exposure acceleration in mid-volume tiers (approx. 50,000 services) and quantifies exploding unpredictability at extreme high-volume tiers (100,000+ services).

### 3. Executive Output & Visualization
* Processes anomaly flags and PyGAM expected values into optimized dimensional tables, ready for integration into interactive FWA dashboards (e.g., Tableau).

## Model Performance Metrics
- **Out-of-Fold R²:** 0.6748
- **RMSE:** 1.0956
- **MAE:** 0.7714

## Repository Structure
```text
fwa-claims-pipeline/
├── data/                  # (Gitignored) Raw and processed Medicare datasets
├── src/                   # Core Python execution scripts (e.g., Billing_variance_curve.py)
├── images/                # Screenshots (PyGAM plots)
├── requirements.txt       # Python dependencies (pygam, pandas, numpy)
└── README.md              # Documentation and pipeline architecture
