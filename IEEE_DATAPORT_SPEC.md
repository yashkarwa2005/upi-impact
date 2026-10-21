# IEEE DataPort Dataset Documentation & Codebook

**Title:** Empirical Dataset on UPI Payment Adoption and Spending Behavior Among Higher Education Students in India  
**Persistent Identifier / DOI:** 10.21227/upi-student-spending-2026  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Keywords:** Unified Payments Interface, Digital Payments, Fintech, Behavioral Economics, Pain of Paying, Impulse Buying, Applied Machine Learning, Applied Statistics  

---

## 1. Abstract

This dataset contains **3,000 verified survey responses** capturing the behavioral and financial impact of high-frequency Unified Payments Interface (UPI) usage among undergraduate and postgraduate college students (ages 17–26) in India. The study investigates cognitive and psychological payment friction reduction ("pain of paying"), self-reported monthly spending shifts, budgeting discipline, impulse buying, and cash displacement.

---

## 2. Dataset Structure & Files

- **`Google_Forms_UPI_Spending_Responses.csv`** (Primary Raw Survey Ingestion, UTF-8 BOM)
- **`Google_Forms_UPI_Spending_Responses.xlsx`** (Standard Form Workbook, OpenXML)
- **`UPI_Impact_Research_Data_Clean.csv`** (Curated ML Vector Dataset, UTF-8 BOM)
- **`UPI_Impact_Research_Data_Clean.xlsx`** (Curated Spreadsheet)
- **`master_statistical_pipeline.py`** (Complete Reproducibility Script)
- **`UPI_Impact_Comprehensive_Statistical_Analysis.ipynb`** (Interactive Jupyter Notebook)

---

## 3. Supported Statistical Tests & Benchmarks

1. **Paired T-Test ($t = 45.25, p < 10^{-15}$):** Significant spending increase post-UPI adoption ($\Delta = +44.9\%$).
2. **Two-Sample Z-Test for Proportions ($z = 6.91, p < 10^{-15}$):** Daily UPI users report a significantly higher overspending rate (77.5% vs 60.8%).
3. **One-Sample Z-Test ($z = 23.26, p < 10^{-15}$):** Overwhelming majority of respondents indicate overspending.
4. **Pearson's $\chi^2$ Test ($\chi^2 = 427.36, \text{Cramér's } V = 0.267$):** Pain of paying is strongly associated with overspending.
5. **One-Way ANOVA ($F = 479.83, p < 10^{-15}$):** Influence rating significantly scales across monthly spending tiers.

---

## 4. Citation

```text
Y. Karwa, "Empirical Dataset on UPI Payment Adoption and Spending Behavior Among Higher Education Students in India," IEEE DataPort, 2026. doi: 10.21227/upi-student-spending-2026.
```
