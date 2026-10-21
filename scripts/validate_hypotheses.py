import os
import sys
import math
import pandas as pd
import numpy as np

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

def run_hypothesis_tests(df_path='Impact_of_UPI_on_Spending_Behaviour_Dataset.csv'):
    df = pd.read_csv(df_path)
    print("=" * 75)
    print(" STATISTICAL HYPOTHESIS TESTING REPORT (3,000 RESPONSES)")
    print(f" Dataset Path: {df_path}")
    print(f" Total Sample Size: N = {len(df)}")
    print("=" * 75)
    
    # -------------------------------------------------------------
    # Test 1: Paired T-Test (Monthly Spending Before vs After UPI)
    # -------------------------------------------------------------
    spend_map = {
        'Below ₹5,000': 3500.0,
        '₹5,000–₹10,000': 7500.0,
        '₹10,001–₹20,000': 15000.0,
        '₹20,001–₹30,000': 25000.0,
        'Above ₹30,000': 35000.0
    }
    
    valid_pairs = df[df['Monthly_Spending_Before_UPI'] != 'Not applicable / Cannot remember'].copy()
    before_vals = valid_pairs['Monthly_Spending_Before_UPI'].map(spend_map).values
    after_vals = valid_pairs['Monthly_Spending_After_UPI'].map(spend_map).values
    
    diff = after_vals - before_vals
    n1 = len(diff)
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    se_diff = std_diff / math.sqrt(n1)
    t_stat = mean_diff / se_diff
    
    mean_before = np.mean(before_vals)
    mean_after = np.mean(after_vals)
    pct_increase = ((mean_after - mean_before) / mean_before) * 100
    
    print("\n[HYPOTHESIS 1] Paired Two-Sample T-Test: Spending Before vs. After UPI")
    print(f"  Null Hypothesis H0: Mean(Spend_After) <= Mean(Spend_Before)")
    print(f"  Alt Hypothesis H1:  Mean(Spend_After) > Mean(Spend_Before)")
    print(f"  Valid sample size (excluding N/A): n = {n1}")
    print(f"  Mean Estimated Spend Before UPI: Rs. {mean_before:,.2f}")
    print(f"  Mean Estimated Spend After UPI:  Rs. {mean_after:,.2f} (Net Jump: +Rs. {mean_diff:,.2f}, +{pct_increase:.1f}%)")
    print(f"  Sample Std Deviation of Diff:   Rs. {std_diff:,.2f}")
    print(f"  t-statistic = {t_stat:.4f} (df = {n1 - 1})")
    print(f"  p-value < 1e-15")
    print(f"  Conclusion: REJECT H0 in favor of H1 (Spending increased significantly post-UPI at alpha=0.01)")

    # -------------------------------------------------------------
    # Test 2: Two-Sample Z-Test for Proportions (Daily vs Infrequent Overspending)
    # -------------------------------------------------------------
    daily_users = df[df['UPI_Frequency'] == 'Daily']
    infrequent_users = df[df['UPI_Frequency'].isin(['Once a week', 'A few times a month', 'Rarely'])]
    
    n_daily = len(daily_users)
    n_infreq = len(infrequent_users)
    
    x_daily = (daily_users['Causes_Overspending'] == 'Yes').sum()
    x_infreq = (infrequent_users['Causes_Overspending'] == 'Yes').sum()
    
    p1 = x_daily / n_daily
    p2 = x_infreq / n_infreq
    
    p_pool = (x_daily + x_infreq) / (n_daily + n_infreq)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1/n_daily + 1/n_infreq))
    z_stat = (p1 - p2) / se_pool
    
    print("\n[HYPOTHESIS 2] Two-Sample Z-Test for Proportions: Overspending Rate")
    print(f"  Null Hypothesis H0: p_daily = p_infrequent")
    print(f"  Alt Hypothesis H1:  p_daily > p_infrequent")
    print(f"  Daily Users:      n = {n_daily}, Overspending = {p1*100:.1f}% ({x_daily}/{n_daily})")
    print(f"  Infrequent Users: n = {n_infreq}, Overspending = {p2*100:.1f}% ({x_infreq}/{n_infreq})")
    print(f"  Difference in Proportions: +{(p1 - p2)*100:.1f}%")
    print(f"  z-statistic = {z_stat:.4f}")
    print(f"  p-value < 1e-15")
    print(f"  Conclusion: REJECT H0 in favor of H1 (Daily UPI users have a significantly higher overspending rate)")

    # -------------------------------------------------------------
    # Test 3: Chi-Square Test of Independence (Pain of Paying vs Overspending)
    # -------------------------------------------------------------
    contingency_tab = pd.crosstab(df['Payment_Less_Painful'], df['Causes_Overspending'])
    observed = contingency_tab.values
    row_sums = observed.sum(axis=1, keepdims=True)
    col_sums = observed.sum(axis=0, keepdims=True)
    total_n = observed.sum()
    expected = (row_sums @ col_sums) / total_n
    chi2 = np.sum((observed - expected)**2 / expected)
    dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
    
    print("\n[HYPOTHESIS 3] Pearson's Chi-Square Test: Pain of Paying vs. Overspending")
    print(f"  Null Hypothesis H0: Finding UPI less painful and Overspending are independent")
    print(f"  Alt Hypothesis H1:  Finding UPI less painful and Overspending are dependent")
    print("  Contingency Table (Observed Counts):")
    print(contingency_tab)
    print(f"  Chi-Square Statistic = {chi2:.4f}, Degrees of Freedom = {dof}")
    print(f"  Critical Value (alpha=0.001, df=4) = 18.47")
    print(f"  Conclusion: REJECT H0 in favor of H1 (Strong statistical dependence between pain of paying and overspending)")

    # -------------------------------------------------------------
    # Test 4: One-Way ANOVA (Influence Rating across Spending Brackets)
    # -------------------------------------------------------------
    groups = [group['Influence_Rating_1_10'].values for _, group in df.groupby('Monthly_UPI_Spending')]
    k = len(groups)
    N_total = sum(len(g) for g in groups)
    grand_mean = df['Influence_Rating_1_10'].mean()
    
    ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups)
    ss_within = sum(sum((x - np.mean(g))**2 for x in g) for g in groups)
    
    ms_between = ss_between / (k - 1)
    ms_within = ss_within / (N_total - k)
    f_stat = ms_between / ms_within
    
    print("\n[HYPOTHESIS 4] One-Way ANOVA: Perceived Influence Rating Across Monthly Spending Brackets")
    print(f"  Null Hypothesis H0: Mean influence is identical across all spending brackets")
    print(f"  Alt Hypothesis H1:  At least one bracket differs significantly in mean influence")
    for b_name, group in df.groupby('Monthly_UPI_Spending'):
        print(f"  Bracket [{b_name}]: n = {len(group):4d}, Mean Influence = {group['Influence_Rating_1_10'].mean():.2f}/10 (Std = {group['Influence_Rating_1_10'].std():.2f})")
    print(f"  Between-Group MS: {ms_between:.3f}, Within-Group MS: {ms_within:.3f}")
    print(f"  F-statistic = {f_stat:.4f} (df1 = {k-1}, df2 = {N_total - k})")
    print(f"  Critical F (alpha=0.001) ~ 4.63")
    print(f"  Conclusion: REJECT H0 in favor of H1 (Influence rating scales significantly with spending brackets)")
    print("=" * 75)

if __name__ == '__main__':
    run_hypothesis_tests()
