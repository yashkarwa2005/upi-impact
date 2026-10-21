# UPI Spending Behaviour — Advanced Visual Analytics Suite

This directory contains the production-grade visualization scripts and generated figures for the research study:  
**"Impact of Unified Payments Interface (UPI) on Spending Behaviour Among College Students"** ($N = 3,000$ verified respondent records).

---

## 📊 Summary of Visualizations

| # | Figure File | Visualization Type | Academic & Behavioral Purpose |
|---|---|---|---|
| **1** | [`fig1_upi_frequency_vs_spending.png`](./fig1_upi_frequency_vs_spending.png) | **Bar Chart + SEM Error Bars** | Analyzes whether frequent UPI users spend more on average and highlights aggregate expenditure share across cohorts. |
| **2** | [`fig2_transactions_vs_monthly_spending.png`](./fig2_transactions_vs_monthly_spending.png) | **Scatter Plot + OLS Trendline** | Quantifies the correlation and regression slope between monthly UPI transaction frequency and spending volume. |
| **3** | [`fig3_spending_category_distribution.png`](./fig3_spending_category_distribution.png) | **Stacked Bar Chart** | Decomposes student budgets across 6 primary spending categories across different monthly spending tiers. |
| **4** | [`fig4_upi_usage_vs_impulse_purchasing.png`](./fig4_upi_usage_vs_impulse_purchasing.png) | **Grouped Bar Chart** | Evaluates the surge in unplanned impulse purchasing propensity as UPI usage frequency escalates from *Rarely* to *Daily*. |
| **5** | [`fig5_kmeans_student_spending_clusters.png`](./fig5_kmeans_student_spending_clusters.png) | **K-Means ML Scatter Plot (PCA 2D)** | Unsupervised Machine Learning segmentation ($k=4$) identifying distinct student spending personas. |

---

## 🔍 Detailed Empirical Findings

### Figure 1: UPI Usage Frequency vs. Average Monthly Spending
- **Mean Spending per Cohort:**
  - *Rarely*: ₹14,846 $\pm$ ₹1,162 ($N = 78$, 3.0% of total volume)
  - *A few times a month*: ₹13,765 $\pm$ ₹899 ($N = 119$, 4.2% of total volume)
  - *Once a week*: ₹12,711 $\pm$ ₹619 ($N = 201$, 6.5% of total volume)
  - *Several times a week*: ₹13,126 $\pm$ ₹329 ($N = 802$, 27.0% of total volume)
  - *Daily*: ₹12,855 $\pm$ ₹212 ($N = 1,800$, 59.3% of total volume)
- **Key Insight:** Infrequent users display higher single-ticket averages due to lumpy payments (tuition fees, travel tickets, electronics), whereas Daily users dominate aggregate spending volume (₹2.31 Crore/month), driven by high-velocity convenience micro-transactions.

### Figure 2: UPI Transaction Frequency vs. Monthly Spending Volume
- **Regression Equation:** $\text{Monthly Spend (₹)} = -12.9 \times \text{Transactions} + 13,733$
- **Scatter Insights:** Points are color-coded by perceived overspending (`Causes_Overspending`: *Yes*, *Maybe*, *No*).
- **Behavioral Economic Takeaway:** Overspending perception is heavily concentrated among high-frequency transactors (>40 transactions/month), as cumulative micro-purchases deplete monthly balances without tactile feedback.

### Figure 3: Spending Category Distribution Across Monthly Budget Tiers
- **Category Proportions:**
  - *Below ₹5,000 Tier:* Dominated by **Food & Canteen (44%)**, **Daily Snacks & Chai (21%)**, and **Commute & Travel (15%)**.
  - *Above ₹30,000 Tier:* Characterized by **E-Commerce & Fashion/Gadgets (36%)**, **Dining & Entertainment (26%)**, and **Quick-Commerce (15%)**.
- **Takeaway:** As student budgets scale, essential food spending gives way to discretionary retail, digital subscriptions, and dining experiences.

### Figure 4: UPI Usage Frequency vs. Impulse Purchasing Propensity
- **Empirical Contrast:**
  - **Daily UPI Users:** **59.1%** report making unplanned impulse purchases *"Often"* (34.7%) or *"Very often"* (24.4%).
  - **Rare UPI Users:** Only **29.5%** report frequent impulse buying (*"Often"* 20.5%, *"Very often"* 9.0%).
  - **Statistical Significance:** Pearson Chi-Square test confirms high dependency ($p < 0.0001$). Daily UPI accessibility acts as a 2.0x multiplier on impulse spending propensity.

### Figure 5: K-Means Student Spending Personas (PCA 2D Projection)
Unsupervised clustering using 6 standardized features (`Spend_Num`, `Impulse_Num`, `Convenience_Num`, `Influence_Rating_1_10`, `Cash_Num`, `Freq_Scale`):
1. **Cluster 1 (Blue) — Daily Micro-Spenders (Campus & Canteen):**
   - $N = 1,476$ (49.2%) | Mean Monthly Spend: ₹7,338 | Cash Carried: ₹483 | Freq: 4.74 (Daily)
   - *Profile:* Heavy daily micro-transactions for food, tea, printing, and auto-rickshaws.
2. **Cluster 2 (Orange) — High-Volume Digital Consumers:**
   - $N = 889$ (29.6%) | Mean Monthly Spend: ₹22,871 | Influence Rating: 8.98 / 10 | Overspending: 80.4%
   - *Profile:* High-velocity shoppers with extreme reliance on UPI apps for fashion, dining, and gadgets.
3. **Cluster 3 (Green) — Disciplined / Selective Planners:**
   - $N = 488$ (16.3%) | Mean Monthly Spend: ₹12,245 | Impulse Score: 2.59 (Lowest) | Freq: 2.80 (Weekly)
   - *Profile:* Intentional spenders who restrict UPI to planned purchases with high financial awareness.
4. **Cluster 4 (Purple) — Cash-Anchored Traditionalists:**
   - $N = 147$ (4.9%) | Mean Monthly Spend: ₹12,779 | Cash Carried: ₹4,231 (10x average)
   - *Profile:* Retains physical cash in wallet as psychological friction buffer against digital overspending.

---

## 🧪 Inferential Statistical Testing Suites (Hypothesis Testing)

Separate standalone diagnostic scripts are provided for parametric and non-parametric hypothesis testing with publication-grade distribution graphs:

| Script | Output Diagnostic Graph | Primary Statistical Test | Key Finding & Decision |
|---|---|---|---|
| [`run_t_test.py`](./run_t_test.py) | [`t_test_analysis.png`](./t_test_analysis.png) | **Paired Two-Sample Student's T-Test** ($N=2,622$) | **$t = 44.22, p < 10^{-15}$ (REJECT $H_0$)**.<br>Monthly expenditure increased by **+₹3,975.02 (+43.8%)** post-UPI adoption ($d = 0.864$, large effect). |
| [`run_z_test.py`](./run_z_test.py) | [`z_test_analysis.png`](./z_test_analysis.png) | **Two-Sample Z-Test for Proportions** ($N_1=1,800, N_2=398$) | **$Z = 7.40, p = 1.32 \times 10^{-13}$ (REJECT $H_0$)**.<br>Daily users have **+17.8% higher overspending rate** (77.9% vs. 60.1%; Odds Ratio = 2.34x). |

---

## 🚀 How to Run the Scripts

### 1. Generate All 5 Core Visualizations:
```bash
python visualization/generate_charts.py
```

### 2. Run the Student's T-Test Suite (Code + Graph):
```bash
python visualization/run_t_test.py
```
*Outputs: Complete academic hypothesis report in terminal + generates `visualization/t_test_analysis.png` (300 DPI).*

### 3. Run the Z-Test for Proportions Suite (Code + Graph):
```bash
python visualization/run_z_test.py
```
*Outputs: Comprehensive proportion z-test metrics + generates `visualization/z_test_analysis.png` (300 DPI).*
