# Project Context: Impact of UPI on Spending Behaviour Among College Students

> **Academic Domain:** Artificial Intelligence & Machine Learning (AIML), Applied Statistics & Behavioral Economics  
> **Project Title:** Impact of Unified Payments Interface (UPI) on Spending Behaviour Among College Students  
> **Target Demographic:** Undergraduate and postgraduate college students (Ages 17–26) across urban and semi-urban institutions in India  
> **Primary Objective:** Quantify, analyze, and model how high-frequency, frictionless digital payment adoption (UPI) alters students' financial discipline, monthly expenditures, impulse purchases, and perceived psychological "pain of paying".

---

## 1. Executive Summary & Research Background

The rapid proliferation of digital payment infrastructure in India—specifically **Unified Payments Interface (UPI)**—has drastically transformed consumer spending habits. College students represent one of the most active digital demographic segments, using UPI apps (Google Pay, PhonePe, Paytm, CRED, BHIM) for daily micro-transactions (canteen food, tea, stationery, transport) as well as e-commerce, food delivery, and entertainment subscriptions.

### Core Behavioral & Economic Problems
1. **Diminished "Pain of Paying" (Prelec & Loewenstein Theory):**  
   Physical cash exchange requires physically parting with paper currency, which triggers immediate cognitive and emotional friction ("loss aversion"). Digital QR scans and biometric/PIN authorizations eliminate tactile feedback, making payments feel virtually frictionless and less painful.
2. **Mental Accounting Distortions (Thaler's Theory):**  
   Small micro-transactions (₹10–₹100) are often dismissed as negligible, leading to cumulative budget overruns that students fail to notice until their monthly bank balance is depleted.
3. **Impulse & Unplanned Purchases:**  
   Instantaneous transaction speed combined with promotional nudges (cashback, scratch cards, discounts) accelerates unplanned impulse spending.
4. **Lack of Active Budget Tracking:**  
   Despite digital transaction histories being readily accessible, students frequently avoid reviewing daily logs, leading to post-purchase regret.

---

## 2. Research Questions & Statistical Hypotheses

| # | Research Question | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Statistical Test |
|---|-------------------|-------------------------|--------------------------------|------------------|
| **1** | Has average monthly spending increased significantly after adopting UPI? | $\mu_{\text{after}} \le \mu_{\text{before}}$ (No increase in monthly spending) | $\mu_{\text{after}} > \mu_{\text{before}}$ (Monthly spending is significantly higher post-UPI) | **Paired Two-Sample T-Test** / **Wilcoxon Signed-Rank Test** |
| **2** | Do frequent UPI users (Daily) report a higher proportion of overspending compared to infrequent users? | $p_{\text{daily}} = p_{\text{infrequent}}$ (Proportions are identical) | $p_{\text{daily}} > p_{\text{infrequent}}$ (Daily users have higher overspending rate) | **Two-Sample Z-Test for Proportions** |
| **3** | Is finding UPI "less painful than cash" statistically dependent on reporting overspending? | Variable $A$ and $B$ are independent | Variable $A$ and $B$ are significantly dependent | **Pearson's Chi-Square ($\chi^2$) Test of Independence** |
| **4** | Does the perceived influence rating (1–10) differ across different monthly UPI spending brackets? | $\mu_1 = \mu_2 = \mu_3 = \mu_4 = \mu_5$ (Mean influence is equal across brackets) | At least one spending bracket has a significantly different mean influence rating | **One-Way ANOVA** / **Kruskal-Wallis H-Test** |

---

## 3. Comprehensive Survey Instrument & Question Mapping

The survey consists of **15 core questions** designed to capture demographics, transaction frequencies, spending brackets before/after UPI, psychological factors, and perceived influence.

### Question Inventory

```
[Q1]  Frequency of UPI Usage (q1_freq)
      • Options: 'Daily', 'Several times a week', 'Once a week', 'A few times a month', 'Rarely'
      • Type: Categorical / Ordinal

[Q2]  Average Monthly Spending via UPI (q2_monthly_spend)
      • Options: 'Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000'
      • Type: Categorical / Ordinal Bins (Midpoints: ₹2,500, ₹7,500, ₹15,000, ₹25,000, ₹35,000)

[Q3]  Cash Normally Carried (q3_cash_carry)
      • Options: 'Less than ₹500', '₹500–₹1,000', '₹1,001–₹2,000', '₹2,001–₹5,000', 'More than ₹5,000'
      • Type: Categorical / Ordinal Bins (Midpoints: ₹250, ₹750, ₹1,500, ₹3,500, ₹6,000)

[Q4]  Spend More When Paying via UPI than Cash (q4_spend_more_upi)
      • Options: 'Yes', 'No', 'Maybe'
      • Type: Categorical (Binary/Trinary Target)

[Q5]  Unplanned Purchases Frequency (q5_unplanned_purchases)
      • Options: 'Never', 'Rarely', 'Sometimes', 'Often', 'Very often'
      • Type: 5-Point Likert Scale (1 = Never, 5 = Very often)

[Q6]  Influence of Cashbacks/Discounts on Purchasing (q6_cashback_discounts)
      • Options: 'Never', 'Rarely', 'Sometimes', 'Often', 'Very often'
      • Type: 5-Point Likert Scale (1 = Never, 5 = Very often)

[Q7]  Checking UPI Transaction History Regularly (q7_check_history)
      • Options: 'Yes, regularly', 'Sometimes', 'Rarely', 'Never'
      • Type: Categorical / Ordinal

[Q8]  Regret Over UPI Purchases (q8_regret_purchase)
      • Options: 'Never', 'Rarely', 'Sometimes', 'Often', 'Very often'
      • Type: 5-Point Likert Scale (1 = Never, 5 = Very often)

[Q9]  UPI Payments Feel Less Painful / Noticeable than Cash (q9_less_painful)
      • Options: 'Yes', 'No', 'Not sure'
      • Type: Categorical (Behavioral indicator for Pain of Paying)

[Q10] Spending Has Increased Since Regular UPI Usage (q10_spending_increased)
      • Options: 'Yes', 'No', 'Not sure'
      • Type: Categorical (Subjective spending inflation indicator)

[Q11] Small-Value Convenience Purchases Frequency (q11_small_value_convenience)
      • Options: 'Never', 'Rarely', 'Sometimes', 'Often', 'Very often'
      • Type: 5-Point Likert Scale (1 = Never, 5 = Very often)

[Q12] Approximate Monthly Spending BEFORE Using UPI (q12_spend_before_upi)
      • Options: 'Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000', 'Not applicable / Cannot remember'
      • Type: Categorical / Baseline spending bracket

[Q13] Approximate Monthly Spending AFTER Regularly Using UPI (q13_spend_after_upi)
      • Options: 'Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000'
      • Type: Categorical / Post-adoption spending bracket

[Q14] Rate UPI Influence on Spending Behaviour (q14_influence_scale)
      • Range: 1 to 10 Linear Scale (1 = 'Does not influence', 10 = 'Strongly influences')
      • Type: Continuous / Interval

[Q15] Belief that UPI Causes Overspending (q15_causes_overspend)
      • Options: 'Yes', 'No', 'Maybe'
      • Type: Primary Target Label for Machine Learning
```

---

## 4. Dataset Schema & Standard Column Specifications

All datasets generated or exported from the survey follow this exact standard schema:

| Column Header | Data Type | Permitted Values / Range | Description |
|---|---|---|---|
| `Respondent_ID` | String | `RESP_0001` – `RESP_9999` | Unique identifier for survey respondent |
| `Timestamp` | DateTime | `YYYY-MM-DD HH:MM:SS` | Date and time of response logging |
| `UPI_Frequency` | String | `Daily`, `Several times a week`, `Once a week`, `A few times a month`, `Rarely` | Frequency of UPI payments |
| `Monthly_UPI_Spending` | String | `Below ₹5,000`, `₹5,000–₹10,000`, `₹10,001–₹20,000`, `₹20,001–₹30,000`, `Above ₹30,000` | Current monthly volume on UPI |
| `Cash_Carried` | String | `Less than ₹500`, `₹500–₹1,000`, `₹1,001–₹2,000`, `₹2,001–₹5,000`, `More than ₹5,000` | Physical cash in wallet |
| `Spend_More_Than_Cash` | String | `Yes`, `No`, `Maybe` | Perception of spending more vs cash |
| `Unplanned_Purchases_Frequency` | String | `Never`, `Rarely`, `Sometimes`, `Often`, `Very often` | Impulse purchase frequency |
| `Cashback_Discount_Influence` | String | `Never`, `Rarely`, `Sometimes`, `Often`, `Very often` | Marketing inducement sensitivity |
| `Checks_Transaction_History` | String | `Yes, regularly`, `Sometimes`, `Rarely`, `Never` | Monitoring / accounting behavior |
| `Regret_UPI_Purchase` | String | `Never`, `Rarely`, `Sometimes`, `Often`, `Very often` | Buyer's remorse frequency |
| `Payment_Less_Painful` | String | `Yes`, `No`, `Not sure` | Psychological pain of paying indicator |
| `Spending_Increased_With_UPI` | String | `Yes`, `No`, `Not sure` | Self-reported expenditure increase |
| `Small_Value_Convenience_Purchases` | String | `Never`, `Rarely`, `Sometimes`, `Often`, `Very often` | Micro-transaction frequency |
| `Monthly_Spending_Before_UPI` | String | `Below ₹5,000`, `₹5,000–₹10,000`, `₹10,001–₹20,000`, `₹20,001–₹30,000`, `Above ₹30,000`, `Not applicable / Cannot remember` | Pre-UPI monthly spend |
| `Monthly_Spending_After_UPI` | String | `Below ₹5,000`, `₹5,000–₹10,000`, `₹10,001–₹20,000`, `₹20,001–₹30,000`, `Above ₹30,000` | Post-UPI monthly spend |
| `Influence_Rating_1_10` | Integer | `1` to `10` | Overall self-rated influence score |
| `Causes_Overspending` | String | `Yes`, `No`, `Maybe` | Target feature: Perceived overspending |

---

## 5. Feature Engineering & Numerical Encodings for AIML Pipelines

When processing the dataset for statistical modeling and Machine Learning classification:

### 1. Likert Scale Integer Encodings (1 to 5)
```python
LIKERT_MAP = {
    'Never': 1,
    'Rarely': 2,
    'Sometimes': 3,
    'Often': 4,
    'Very often': 5
}
```

### 2. Spending Bracket Midpoint Conversions (INR ₹)
```python
SPEND_BRACKET_MIDPOINTS = {
    'Below ₹5,000': 3500.0,
    '₹5,000–₹10,000': 7500.0,
    '₹10,001–₹20,000': 15000.0,
    '₹20,001–₹30,000': 25000.0,
    'Above ₹30,000': 35000.0,
    'Not applicable / Cannot remember': None
}

CASH_CARRIED_MIDPOINTS = {
    'Less than ₹500': 250.0,
    '₹500–₹1,000': 750.0,
    '₹1,001–₹2,000': 1500.0,
    '₹2,001–₹5,000': 3500.0,
    'More than ₹5,000': 6000.0
}
```

### 3. Derived Analytical Features
- **`Monthly_Spend_Inflation_INR`**: `Spend_After_Midpoint - Spend_Before_Midpoint` (Positive values indicate expenditure growth post-UPI).
- **`Spend_Inflation_Percentage`**: `(Spend_After - Spend_Before) / Spend_Before * 100`.
- **`Impulse_Index`**: Weighted composite score of `Unplanned_Purchases`, `Cashback_Influence`, and `Small_Value_Convenience`.
- **`Financial_Awareness_Score`**: Inverted `Checks_Transaction_History` combined with `Regret_UPI_Purchase`.
- **`Cash_Independence_Ratio`**: `Monthly_UPI_Spending_Midpoint / (Cash_Carried_Midpoint * 4 + 1)`.

---

## 6. Machine Learning Model Formulations

### Task 1: Binary / Multi-Class Classification of Overspending (`Causes_Overspending`)
- **Target Variable ($y$):** `Causes_Overspending` (Class 0 = No/Maybe, Class 1 = Yes; or Multi-class 0=No, 1=Maybe, 2=Yes).
- **Input Features ($X$):**
  - UPI Frequency (Ordinal)
  - Estimated Monthly UPI Spending (Continuous)
  - Estimated Cash Carried (Continuous)
  - Unplanned Purchases Score (1–5)
  - Pain of Paying indicator (`Payment_Less_Painful` = 1 if Yes, 0 otherwise)
  - Convenience Micro-purchases Score (1–5)
  - Transaction History Monitoring (Ordinal)
  - Influence Scale Rating (1–10)
- **Baseline Models:** Logistic Regression, Random Forest Classifier, XGBoost / LightGBM, Support Vector Machines (SVM).
- **Evaluation Metrics:** Classification Accuracy, Balanced Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix.

### Task 2: Linear / Ridge Regression on Influence Rating (`Influence_Rating_1_10`)
- **Target Variable ($y$):** Continuous rating from 1 to 10.
- **Goal:** Identify which behavioral factors most heavily predict self-reported susceptibility to UPI payment friction reduction.
- **Key Metrics:** $R^2$ Score, Mean Absolute Error (MAE), Root Mean Squared Error (RMSE).

---

## 7. Cross-File & Infrastructure Architecture

```mermaid
graph TD
    A["Web App Suite (index.html, app.js, style.css)"] -->|Interactive Form & Respondent Mode| B["Local Storage / Responses"]
    A -->|Simulate Student Records (100–3,000)| B
    B -->|Export CSV| C["Impact_of_UPI_on_Spending_Behaviour_Dataset.csv"]
    A -->|Apps Script Generator| D["Google Apps Script (Google Drive / Sheets)"]
    C -->|Input Data| E["Python EDA & Hypothesis Testing Pipeline"]
    E -->|Welch's T-Test, Z-Test, Chi-Square, ML Baseline| F["Statistical Test Report & Insights"]
```

---

## 8. Summary of Known Empirical Findings (From UPI Survey Analytics)

1. **High Daily Penetration:** >75% of college students use UPI on a daily or near-daily basis.
2. **Cash Displacement:** Over 68% of students carry less than ₹500 in physical cash, relying almost entirely on QR-code payments.
3. **Loss of Spending Salience:** ~65% of students report finding UPI significantly less painful to spend compared to physical currency notes.
4. **Post-UPI Spending Jump:** Average self-reported monthly spending shifts upward by approximately 25%–45% after adopting UPI, primarily concentrated in small snacks, beverages, quick-commerce, and digital entertainment.
5. **Impulse Multiplier:** Over 55% of respondents indicate making unplanned impulse purchases "Often" or "Very Often" due to UPI availability.
