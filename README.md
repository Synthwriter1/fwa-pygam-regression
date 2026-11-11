# FWA PyGAM Regression: Real-World Medicare Forensic Audit

## Executive Summary
This repository houses the production environment for a multi-phase forensic audit of 802,000 real-world 2024 California CMS Medicare claims. Building upon the synthetic machine learning baseline established in Phases 1 and 2 (housed in a separate sandbox repository), this project applies advanced continuous regression modeling and strict deterministic auditing to uncover both probabilistic upcoding anomalies and structural administrative failures within the federal healthcare payment architecture.

By combining predictive data science with forensic investigative journalism (cross-referencing Department of Justice indictments and statutory laws), this pipeline maps not just statistical outliers, but the actual vulnerability windows of the government's fraud prevention systems.

## Repository Architecture & Modular Documentation

```text
fwa-pygam-regression/
├── data_engineering/                  # ETL & API Ingestion
│   └── API_chunked_ingestion.py       # Script for chunking massive federal payloads
├── data/
│   └── .keep                          # Raw 802k CMS and LEIE CSVs (Gitignored)
├── phase_3_pygam/                     
│   ├── README.md                      
│   ├── Billing_variance_curve.py
│   ├── pygam_acceleration_threshold_50k.png
│   └── pygam_global_variance_curve.png
├── phase_4_leie_audit/                
│   ├── README.md                      
│   ├── phase_4_leie_audit.py
│   └── results/
│       └── phase_4_leie_hits_anonymized.csv
└── README.md
```
To maintain strict data governance and prevent leakage, this repository is strictly segregated from synthetic test data. It is structured chronologically, from initial API ingestion through advanced mathematical modeling and deterministic auditing.

*Note: For detailed technical breakdowns, mathematical methodologies, and script instructions, please refer to the nested `README.md` files located inside each phase's respective folder.*

### Data Engineering: API Chunked Ingestion
Before advanced analytics can begin, massive federal datasets must be acquired without triggering memory faults or API timeouts. 
* **The Process:** Engineered a custom Python ETL script (`API_chunked_ingestion.py`) to systematically pull down Medicare claims data in manageable chunks.
* **The Value:** Demonstrates enterprise-level memory management, pagination looping, and API rate-limit handling necessary for production-scale data engineering.
* **Location:** `data_engineering/API_chunked_ingestion.py`

### Phase 3: PyGAM & Non-Linear Upcoding
While most fraud detection relies on linear thresholds or opaque black-box models, Phase 3 utilizes **Generalized Additive Models (PyGAM)** to map the hidden, non-linear curves of Medicare upcoding. 
* **The Process:** Engineered a Python data pipeline with chunked ingestion to process 802,000 claims, training a PyGAM model to track billing acceleration thresholds.
* **The Result:** Generated interpretable partial dependence plots that expose the exact mathematical inflection points where aggressive billing deviates from standard clinical practice.
* **Documentation:** `phase_3_pygam/README.md`

### Phase 4: Deterministic Audit & The "Temporal Fog"
Moving from probabilistic algorithms to binary forensics, Phase 4 executes a strict chronological inner merge between the 2024 CMS ledger and the **HHS OIG List of Excluded Individuals/Entities (LEIE)**.
* **The Process:** A Pandas pipeline designed to catch "ghosts in the ledger"—federally excluded providers who successfully routed claims through the system.
* **The Findings:** Identified 69 anomalous claims tied to actively excluded providers, including individuals convicted of fentanyl manufacturing, pill-mill operations, and fake surgical implant schemes (Stivax). 
* **The Forensic Discovery:** Cross-referencing these hits with DOJ indictments exposed massive **administrative latency** (up to 24 months between federal conviction and LEIE exclusion). Furthermore, the audit highlights how the CMS Public Use File's yearly data aggregation creates a **"Temporal Fog"** that acts as an accountability shield, making independent chronological auditing mathematically impossible without subpoenaed data.
* **Documentation:** `phase_4_leie_audit/README.md`

## Tech Stack & Core Competencies
* **Languages & Libraries:** Python, Pandas, NumPy, PyGAM, Matplotlib
* **Forensic Techniques:** Deterministic Data Auditing, Cross-jurisdictional record linking (PACER, DOJ, State Medical Boards), Survivorship Bias Analysis.
* **Data Engineering:** Chunked API ingestion, ETL pipelines, Datetime bounding, Safe Harbor compliance handling.

## Companion Articles & Portfolio
The narrative breakdowns of these forensic audits can be found on my Medium and Substack publications:
* **Phase 3:** *The Shape of the Math: How PyGAM Exposed the Hidden Curve Inside 802,000 Medicare Claims*
* **Phase 4:** *Ghosts in the Ledger: Fentanyl, Pill Mills, and the Medicare Penalty Box*

For the complete architectural overview, including the synthetic glass-box machine learning and IQR sandbox phases, visit the master portfolio: **[gregdamico.github.io](https://gregdamico.github.io)**
