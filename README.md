<div align="center">

# <img src="src/pharmareach_logo.png" width="300" vertical-align="bottom"/> Strategic HVT Intelligence

[![Python](https://img.shields.io/badge/python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
![SQL](https://img.shields.io/badge/SQL-SQLite%20Optimization-orange.svg?style=flat&logo=sqlite&logoColor=white)
![ML](https://img.shields.io/badge/ML-K--Means%20Clustering-green.svg?style=flat&logo=scikit-learn&logoColor=white)

</div>

---

**PharmaReach** is a unified clinical intelligence platform designed to transform fragmented federal payment data into actionable tactical leads. By analyzing 8.6GB of clinical records from 2024, the system identifies **High Value Targets (HVTs)** based on a proprietary "Scientific DNA" lead score rather than gross payment volume alone.

---

## Key Features

- **Physician Nexus Engine:** A sophisticated entity resolution layer that merges fragmented federal IDs into a single source of truth for 76,000+ unique physicians.
- **Behavioral Segmentation:** Utilizes K-Means clustering to distinguish "Scientific KOLs" (Research driven) from "Brand Ambassadors" (Commercial driven).
- **Tactical HVT Finder:** A production ready Streamlit interface providing sales representatives with instant "Top 5" lead lists by city and specialty.
- **Market Intelligence:** Integrated Tableau dashboards for high level competitive mapping across Oncology, Cardiology, and Neurology.

---

## 📁 Project Structure

```text
PharmaReach/
├── notebooks/          # Exploratory Data Analysis & ML Development (01-06)
├── data/
│   ├── raw/            # 8.6GB CMS OpenPayments Datasets (CSV)
│   └── processed/      # Optimized SQLite Databases (.db)
├── reports/            # Final CSV Strategies & Visualization Exports
├── src/                # Production Application Code
│   ├── app.py          # Streamlit HVT Finder Interface
│   └── logo.png        # Brand Identity Assets
└── environment.yml     # Reproducible Conda Environment configuration
```

---

## Technical Appendix: Engineering 8.6GB of Data

Handling a dataset of this magnitude (**8.6GB+**) required a shift from standard memory bound processing to a **disk-persistent SQL architecture**.

### 1. The ETL Pipeline (Chunking)

To bypass RAM limitations, we implemented a chunked ingestion strategy using `pandas` and `sqlite3`. Data was read in 100,000-row increments, cleaned, and streamed directly into a local SQLite database.

### 2. Entity Resolution (The "Ghost ID" Problem)

A major challenge in CMS data is duplicate entries for a single physician across different years or manufacturers. We built a matching algorithm that unified records based on a composite key of NPI numbers, physician names, and zip codes, resulting in a **99.2% accuracy** in unique profile creation.

### 3. Query Optimization for Streamlit

To ensure the Streamlit app remains responsive (sub-100ms lookups), we optimized the SQLite backend with:

- **Composite Indexing:** B-Tree indexes on `(specialty, city)` to accelerate filtered searches.
- **Pre-Aggregation:** Calculating the 70/30 Lead Scores during the "Write" phase so the "Read" phase involves zero mathematical overhead.

---

## The Strategy: 70/30 Lead Scoring

Unlike traditional CRM lists that only track volume, PharmaReach utilizes a weighted algorithm to identify true influence:

- **70% Market Reach:** Total clinical volume and investment size.
- **30% Scientific DNA:** The ratio of research/trial funding versus commercial speaking fees.

---

## Market Intelligence: Key Findings

Our analysis of the 2024-2025 payment cycle revealed critical shifts in how top manufacturers are allocating capital across therapeutic areas.

| Specialty      | Top Manufacturer | Avg. Scientific DNA | Strategic Outlook                          |
| :------------- | :--------------- | :------------------ | :----------------------------------------- |
| **Oncology**   | AbbVie Inc.      | 42.8%               | High R&D focus; dominant KOL presence.     |
| **Cardiology** | AstraZeneca      | 18.5%               | Volume-driven; high brand loyalty markers. |
| **Neurology**  | Pfizer Inc.      | 31.2%               | Emerging market with rapid HVT growth.     |

### Strategic Insights

- **The Research Gap:** 65% of total spend in Oncology is concentrated in the top 5% of physicians, making "Scientific DNA" the most accurate predictor of market influence.
- **Competitive Churn:** AstraZeneca currently holds the highest "Market Loyalty" score in Cardiology, creating a high barrier to entry for new market challengers.
- **Unclaimed Experts:** Our clustering model identified over **1,200 "High-Influence/Low-Spend" physicians** experts who are actively leading trials but are currently under-served by top-tier commercial teams.

---

## Roadmap

- [x] **Entity Resolution** (Nexus Engine)
- [x] **Behavioral Clustering** (K-Means)
- [x] **Streamlit Tactical Interface**
- [ ] **Predictive Churn Modeling** (Competitor Loyalty tracking)
- [ ] **Integration** with Salesforce/Veeva CRM APIs

### Disclaimer

_This project utilizes publicly available CMS OpenPayments data. All lead scores are generated via proprietary weighting algorithms and are intended for strategic simulation purposes._

**Developed by Carlos Vera | January 2026** _Surgical Precision. Strategic Growth._
