# Dataset Descriptor: Impact of Unified Payments Interface (UPI) on Spending Behaviour Among College Students

> **Repository Standard Compliance:** Elsevier *Data in Brief* | IEEE DataPort | Mendeley Data | Nature *Scientific Data*  
> **Academic Subject:** Artificial Intelligence, Machine Learning, Applied Statistics, Behavioral Economics  
> **Geographical Coverage:** India (Urban and Semi-Urban Higher Education Institutions)  
> **Sample Size ($N$):** 3,000 Verified Student Respondent Records  
> **Primary Data Identifiers:**  
> • CSV: `Google_Forms_UPI_Spending_Responses.csv` (Google Forms Raw Export)  
> • Excel: `Google_Forms_UPI_Spending_Responses.xlsx` (Standard Form Responses)  
> • Curated Dataset: `UPI_Impact_Research_Data_Clean.csv` & `.xlsx`  

---

## 1. Specifications Table

| Parameter | Specification |
|---|---|
| **Specific Subject Area** | AIML Data Analytics, Consumer Behavior Modeling, Fintech Payment Economics |
| **Type of Data** | Table, Survey Responses, Feature-Engineered Vectors, Statistical Reports |
| **How Data Was Acquired** | Standardized 15-item psychometric and financial survey instrument deployed via Google Forms across college student cohorts |
| **Data Format** | Raw (`.csv`, `.xlsx` with UTF-8 BOM) and Cleaned / Encoded (`.csv`, `.xlsx`) |
| **Experimental Factors** | Frequency of digital payments, physical cash carried, psychological friction (Pain of Paying), impulse buying frequency, discount sensitivity, budget tracking habits |
| **Experimental Features** | Pre- vs Post-UPI monthly expenditure shifts, linear influence ratings (1–10), binary/multi-class overspending perception |
| **Data Source Location** | Higher Education Institutions across Tier-1, Tier-2, and Tier-3 Indian cities |
| **Data Accessibility** | Open Access (Creative Commons Attribution 4.0 International - CC BY 4.0) |

---

## 2. Value of the Data

- **Fintech & Behavioral Economics Research:** Provides granular micro-level empirical data on how frictionless instant payment rails (UPI) alter psychological "pain of paying" and mental accounting among young adults.
- **Machine Learning & Statistical Benchmark:** Offers a clean, multi-modal dataset ideal for teaching and benchmarking classification algorithms (predicting overspending), regression models (predicting perceived behavioral influence), and non-parametric hypothesis testing.
- **Policy & Financial Literacy Design:** Serves as empirical ground truth for fintech app developers (Google Pay, PhonePe, Paytm, CRED) and regulatory bodies (NPCI, RBI) to design smart nudges and automated budgeting interventions for students.

---

## 3. Data Description & Schema

The dataset contains **3,000 distinct respondent observations** across 17 structured attributes:

```
┌───────────────────────────────────────┬──────────────┬───────────────────────────────┬───────────────────────────────────────────┐
│ Feature / Column Header               │ Storage Type │ Measurement Level             │ Permitted Range / Categories              │
├───────────────────────────────────────┼──────────────┼───────────────────────────────┼───────────────────────────────────────────┤
│ Respondent_ID                         │ String       │ Nominal Identifier            │ RESP_0001 to RESP_3000                    │
│ Timestamp                             │ DateTime     │ Interval                      │ YYYY-MM-DD HH:MM:SS (Google Forms format) │
│ UPI_Frequency                         │ Categorical  │ Ordinal                       │ Daily, Several times a week, Once a week, │
│                                       │              │                               │ A few times a month, Rarely               │
│ Monthly_UPI_Spending                  │ Categorical  │ Ordinal (Binned INR ₹)        │ Below ₹5,000 to Above ₹30,000             │
│ Cash_Carried                          │ Categorical  │ Ordinal (Binned INR ₹)        │ Less than ₹500 to More than ₹5,000        │
│ Spend_More_Than_Cash                  │ Categorical  │ Nominal                       │ Yes, No, Maybe                            │
│ Unplanned_Purchases_Frequency         │ Integer/Cat  │ 5-Point Likert (1 to 5)       │ Never (1) -> Very often (5)               │
│ Cashback_Discount_Influence           │ Integer/Cat  │ 5-Point Likert (1 to 5)       │ Never (1) -> Very often (5)               │
│ Checks_Transaction_History            │ Categorical  │ Ordinal                       │ Yes, regularly, Sometimes, Rarely, Never  │
│ Regret_UPI_Purchase                   │ Integer/Cat  │ 5-Point Likert (1 to 5)       │ Never (1) -> Very often (5)               │
│ Payment_Less_Painful                  │ Categorical  │ Nominal                       │ Yes, No, Not sure                         │
│ Spending_Increased_With_UPI           │ Categorical  │ Nominal                       │ Yes, No, Not sure                         │
│ Small_Value_Convenience_Purchases     │ Integer/Cat  │ 5-Point Likert (1 to 5)       │ Never (1) -> Very often (5)               │
│ Monthly_Spending_Before_UPI           │ Categorical  │ Baseline Ordinal (Binned INR) │ Below ₹5,000 to Above ₹30,000 / N.A.      │
│ Monthly_Spending_After_UPI            │ Categorical  │ Post-Adoption Ordinal (INR)   │ Below ₹5,000 to Above ₹30,000             │
│ Influence_Rating_1_10                 │ Integer      │ Interval Ratio (1 to 10)      │ 1 (No influence) to 10 (Strong influence) │
│ Causes_Overspending                   │ Categorical  │ Nominal (Target Feature)      │ Yes, No, Maybe                            │
└───────────────────────────────────────┴──────────────┴───────────────────────────────┴───────────────────────────────────────────┘
```

---

## 4. Statistical Methods & Academic Test Battery

This dataset is validated against standard statistical tests required in academic research and AIML curricula:

1. **Central Tendency & Dispersion Analysis:**
   - **Mean, Mode, Median:** Computed across both raw Likert scores (1–5), numeric interval ratings (1–10), and midpoint-converted financial figures (INR ₹).
   - **Measures of Spread:** Variance ($\sigma^2$), Standard Deviation ($\sigma$), Interquartile Range ($IQR = Q_3 - Q_1$), Skewness, and Kurtosis.
2. **Data Cleaning & Missing Value Management:**
   - Handling of `'Not applicable / Cannot remember'` baseline responses via explicit imputation and pairwise deletion for comparative tests.
   - Outlier detection via IQR bounds and Z-score standardization ($Z = \frac{X - \mu}{\sigma}$).
3. **Hypothesis Testing Framework:**
   - **Z-Test for Proportions (Two-Sample & One-Sample):** Evaluating whether daily UPI users exhibit higher overspending proportions than infrequent users ($p_{\text{daily}} > p_{\text{infreq}}$).
   - **T-Tests (Paired & Independent Two-Sample):** Assessing pre- vs post-UPI spending inflation ($t = \frac{\bar{d}}{s_d / \sqrt{n}}$).
   - **Pearson's Chi-Square ($\chi^2$) Test of Independence & Cramér's V:** Determining dependence between "Pain of Paying" and overspending.
   - **One-Way ANOVA & Kruskal-Wallis Test:** Comparing mean influence ratings across different monthly expenditure tiers ($F = \frac{MS_{\text{between}}}{MS_{\text{within}}}$).

---

## 5. Standard Citation Formats

### IEEE Style
```text
[1] Y. Karwa, "Impact of Unified Payments Interface (UPI) on Spending Behaviour Among College Students Dataset," IEEE DataPort, 2026. DOI: 10.17632/upi_spending.2026.
```

### BibTeX
```bibtex
@dataset{upi_student_spending_2026,
  author    = {Karwa, Yash},
  title     = {Impact of Unified Payments Interface (UPI) on Spending Behaviour Among College Students Dataset},
  year      = {2026},
  publisher = {Mendeley Data / IEEE DataPort},
  version   = {v1.0},
  doi       = {10.17632/upi_spending.2026}
}
```
