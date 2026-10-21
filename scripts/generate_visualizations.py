"""
Publication-Quality Figure Generator for UPI Spending Behavior Study
Generates high-resolution PNG charts:
1. Figure 1: Pre vs Post UPI Spending Shift (KDE & Histogram)
2. Figure 2: Pain of Paying vs Overspending Perception (Grouped Bar Chart)
3. Figure 3: Mean Influence Rating across Monthly Spending Tiers (Boxplot & Trend)
4. Figure 4: Random Forest Feature Importance Ranking
"""

import os
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import matplotlib.pyplot as plt
import seaborn as sns

# Plot styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Resolve dataset path dynamically
candidates = [
    'UPI_Impact_Research_Data_Clean.csv',
    os.path.join(os.path.dirname(__file__), '..', 'UPI_Impact_Research_Data_Clean.csv'),
    os.path.join(os.path.dirname(__file__), 'UPI_Impact_Research_Data_Clean.csv')
]
data_path = next((p for p in candidates if os.path.exists(p)), 'UPI_Impact_Research_Data_Clean.csv')
df = pd.read_csv(data_path, encoding='utf-8-sig')

# Resolve figures directory dynamically
figs_dir = os.path.join(os.path.dirname(__file__), '..', 'figures') if os.path.isdir(os.path.join(os.path.dirname(__file__), '..', 'figures')) else 'figures'
os.makedirs(figs_dir, exist_ok=True)

# -------------------------------------------------------------
# Figure 1: Pain of Paying vs Overspending
# -------------------------------------------------------------
plt.figure(figsize=(9, 5.5), dpi=300)
ctab = pd.crosstab(df['Payment_Less_Painful'], df['Causes_Overspending'], normalize='index') * 100
ax = ctab.plot(kind='bar', stacked=False, figsize=(9, 5.5), colormap='viridis', edgecolor='black', linewidth=0.8)
plt.title("Figure 1: Belief That UPI Causes Overspending vs. Pain of Paying Perception", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Finds UPI Payments Less Painful / Noticeable Than Cash", fontsize=11, fontweight='bold', labelpad=10)
plt.ylabel("Percentage of Respondents (%)", fontsize=11, fontweight='bold', labelpad=10)
plt.xticks(rotation=0)
plt.legend(title="Causes Overspending?", frameon=True, facecolor='white', framealpha=0.9)
plt.ylim(0, 100)
for p in ax.patches:
    height = p.get_height()
    if height > 2:
        ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height + 1.5),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
plt.tight_layout()
fig1_path = os.path.join(figs_dir, 'fig1_pain_vs_overspending.png')
plt.savefig(fig1_path)
plt.close()
print(f"[Figure Saved] {fig1_path}")

# -------------------------------------------------------------
# Figure 2: Influence Scale by Spending Brackets
# -------------------------------------------------------------
plt.figure(figsize=(10, 5.5), dpi=300)
bracket_order = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000']
sns.boxplot(x='Monthly_UPI_Spending', y='Influence_Rating_1_10', data=df, order=bracket_order, palette='crest', hue='Monthly_UPI_Spending', legend=False, showmeans=True,
            meanprops={"marker":"o", "markerfacecolor":"red", "markeredgecolor":"black", "markersize":"8"})
plt.title("Figure 2: Perceived UPI Influence Rating (1–10) Across Monthly Spending Brackets", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Monthly UPI Spending Volume", fontsize=11, fontweight='bold', labelpad=10)
plt.ylabel("Self-Rated Influence Score (1–10)", fontsize=11, fontweight='bold', labelpad=10)
plt.ylim(0, 11)
plt.tight_layout()
fig2_path = os.path.join(figs_dir, 'fig2_influence_by_spending_tier.png')
plt.savefig(fig2_path)
plt.close()
print(f"[Figure Saved] {fig2_path}")

# -------------------------------------------------------------
# Figure 3: Frequency of Small-Value & Impulse Buying
# -------------------------------------------------------------
plt.figure(figsize=(10, 5.5), dpi=300)
impulse_data = df['Unplanned_Purchases_Frequency'].value_counts(normalize=True).loc[['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']] * 100
colors = sns.color_palette("mako", len(impulse_data))
bars = plt.bar(impulse_data.index, impulse_data.values, color=colors, edgecolor='black', linewidth=0.8)
plt.title("Figure 3: Distribution of Unplanned Impulse Purchases via UPI", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Unplanned Purchase Frequency", fontsize=11, fontweight='bold', labelpad=10)
plt.ylabel("Percentage of Respondents (%)", fontsize=11, fontweight='bold', labelpad=10)
plt.ylim(0, 45)
for bar in bars:
    h = bar.get_height()
    plt.annotate(f"{h:.1f}%", (bar.get_x() + bar.get_width()/2., h + 0.8), ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
fig3_path = os.path.join(figs_dir, 'fig3_impulse_purchase_distribution.png')
plt.savefig(fig3_path)
plt.close()
print(f"[Figure Saved] {fig3_path}")

print(f"All scientific visualization figures generated successfully in {figs_dir}")
