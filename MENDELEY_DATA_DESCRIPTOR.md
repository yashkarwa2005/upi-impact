# Mendeley Data Repository Descriptor

**Dataset Title:** Survey Dataset: Impact of Unified Payments Interface (UPI) on College Student Expenditure and Mental Accounting  
**Contributor:** Yash Karwa  
**Institution:** Department of Artificial Intelligence & Machine Learning  
**Version:** 1.0  
**Repository Identifier:** Mendeley Data, doi:10.17632/upi-student-spending.1  

---

## 1. Description of the Data

The dataset provides empirical responses from **3,000 undergraduate and postgraduate students** in Indian universities evaluating the economic and psychological implications of UPI payment adoption.

### Key Data Columns
- **Demographic & Frequency:** `UPI_Frequency`, `Cash_Carried`
- **Economic Volumes:** `Monthly_UPI_Spending`, `Monthly_Spending_Before_UPI`, `Monthly_Spending_After_UPI`
- **Behavioral Constructs (Likert 1–5):** `Unplanned_Purchases_Frequency`, `Cashback_Discount_Influence`, `Checks_Transaction_History`, `Regret_UPI_Purchase`, `Small_Value_Convenience_Purchases`
- **Psychological Friction & Targets:** `Payment_Less_Painful`, `Influence_Rating_1_10`, `Causes_Overspending`

---

## 2. Methodology & Validation

- **Survey Administration:** Administered via online standardized Google Form.
- **Data Integrity:** Fully sanitized, zero encoding artifacts, UTF-8 BOM encoding for Microsoft Excel and Pandas compatibility.
- **Statistical Tests Supported:** Paired T-Tests, Independent Welch's T-Tests, One-Sample T-Tests, Two-Sample Z-Tests for Proportions, One-Sample Z-Tests, Chi-Square Independence Tests, One-Way ANOVA, and Random Forest / Regression ML models.

---

## 3. How to Cite

```bibtex
@dataset{karwa_2026_mendeley,
  author    = {Karwa, Yash},
  title     = {Survey Dataset: Impact of Unified Payments Interface (UPI) on College Student Expenditure and Mental Accounting},
  year      = {2026},
  publisher = {Mendeley Data},
  version   = {v1},
  doi       = {10.17632/upi-student-spending.1}
}
```
