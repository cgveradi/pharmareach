# PharmaReach: Physician HVT Segmentation & Nexus Model

<div align="left">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" height="20"/>
  <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=flat-square&logo=pandas&logoColor=white" height="20"/>
  <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=flat-square&logo=sqlite&logoColor=white" height="20"/>
  <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat-square&logo=scikit-learn&logoColor=white" height="20"/>
  <img src="https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=flat-square&logo=Matplotlib&logoColor=black" height="20"/>
</div>

---

## Project Overview

PharmaReach is a data analytics platform designed to identify **High-Value Targets (HVT)** and **Key Opinion Leaders (KOL)** within the pharmaceutical landscape. By unifying commercial and research payment data into a single **Physician Nexus**, this project enables data-driven targeting strategies across Oncology, Cardiology, and Neurology.

## Data Architecture (Medallion Pattern)

The project utilizes a tiered data strategy to ensure lineage and integrity:

- **Bronze Layer:** Raw ingestion of Open Payments General and Research datasets.
- **Silver Layer:** Standardized physician records with cleaned identities, Title Case formatting, and unified IDs.
- **Gold Layer (Physician Nexus Model):** Final model-ready dataset featuring engineered behavioral scores and log-normalized financial metrics.

## Feature Engineering & Methodology

The following behavioral features were engineered to provide high-resolution physician profiles:

- **Influence Ratio:** A calculation of $( \text{Research Spend} \div \text{Total Spend} )$ used to differentiate between scientific researchers (KOLs) and commercial speakers (HVTs).
- **Manufacturer Loyalty Index:** A concentration score identifying a physician's dependence on a single primary manufacturer.
- **Log-Normal Spend Transformation:** Application of $\log1p$ to total spend values to normalize extreme outliers—such as individuals receiving $\$17M+$—while preserving their relative significance for clustering.

## Analytical Insights

### 1. Behavioral Segmentation

The **Behavioral Segmentation Map** demonstrates natural clustering of physicians based on their influence size and scientific focus. This visualization validates the use of unsupervised learning for market segment discovery.

### 2. Feature Interdependence

A **Correlation Heatmap** confirmed that Influence and Loyalty are statistically independent ($r = -1.00$ for specific segments), ensuring that the model captures unique dimensions of behavior.

### 3. Specialty Dynamics

Statistical validation via **One-Way ANOVA** confirmed significant funding variance across therapeutic areas ($P < 0.05$), justifying the specialized targeting logic applied to each specialty.

## 📂 Repository Structure

```text
├── data
│   ├── raw                # Original CSV datasets (Open Payments)
│   └── processed          # SQLite Databases (HVT_Analysis_Final.db)
├── notebooks
│   ├── 01_data_cleaning   # Ingestion, formatting, and ANOVA validation
│   └── 02_feature_eng     # Feature creation and behavioral analysis
├── reports
│   └── figures            # Exported charts for stakeholder presentation
└── README.md              # Project documentation
```
