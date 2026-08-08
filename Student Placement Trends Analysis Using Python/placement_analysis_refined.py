import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import numpy as np

# Set up visual style
COLORS = ['#4080FF', '#57A9FB', '#37D4CF', '#23C343', '#FBE842', '#FF9A2E', '#A9AEB8']
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['grid.color'] = '#F0F0F0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['axes.edgecolor'] = '#EEEEEE'
plt.rcParams['axes.labelcolor'] = '#333333'
plt.rcParams['xtick.color'] = '#333333'
plt.rcParams['ytick.color'] = '#333333'

# Try to set CJK font (Noto Sans CJK SC is standard for clean look)
font_name = 'sans-serif'
for f in fm.findSystemFonts():
    if 'NotoSansCJK' in f or 'WenQuanYi' in f:
        font_prop = fm.FontProperties(fname=f)
        font_name = font_prop.get_name()
        plt.rcParams['font.family'] = font_name
        break

# Load cleaned data
df = pd.read_csv('cleaned_placement_data.csv')
pkg_order = ['3-6 LPA', '6-10 LPA', '10-15 LPA', '15-25 LPA', '25+ LPA']
df['package'] = pd.Categorical(df['package'], categories=pkg_order, ordered=True)

os.makedirs('final_charts', exist_ok=True)

# --- Chart 1: Placement Trends by Branch ---
plt.figure(figsize=(12, 7))
trend_data = df.groupby(['year', 'branch']).size().unstack()
ax = trend_data.plot(kind='line', marker='o', color=COLORS, linewidth=2.5, markersize=8, ax=plt.gca())
plt.title('Student Placement Trends by Branch (2020-2024)', fontsize=16, fontweight='bold', pad=25)
plt.xlabel('Academic Year', fontsize=12, labelpad=10)
plt.ylabel('Number of Students Placed', fontsize=12, labelpad=10)
plt.grid(True, which='both', axis='both', alpha=0.5)
plt.legend(title='Branch', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False)
plt.xticks(df['year'].unique())
sns.despine(offset=10, trim=True)
plt.tight_layout()
plt.savefig('final_charts/1_placement_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# --- Chart 2: Package Distribution ---
plt.figure(figsize=(10, 6))
pkg_counts = df['package'].value_counts().reindex(pkg_order)
bars = plt.bar(pkg_counts.index, pkg_counts.values, color=COLORS[:5], edgecolor='none', alpha=0.85)
plt.title('Overall Package Distribution (2020-2024)', fontsize=16, fontweight='bold', pad=25)
plt.xlabel('Package Range (LPA)', fontsize=12, labelpad=10)
plt.ylabel('Number of Placements', fontsize=12, labelpad=10)
plt.grid(axis='y', alpha=0.3)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

sns.despine(left=True, bottom=False)
plt.tight_layout()
plt.savefig('final_charts/2_package_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# --- Chart 3: Branch-wise Salary Heatmap ---
plt.figure(figsize=(12, 8))
heatmap_data = pd.crosstab(df['branch'], df['package'])
# Normalize by row to show distribution within branch
heatmap_norm = heatmap_data.div(heatmap_data.sum(axis=1), axis=0) * 100

sns.heatmap(heatmap_norm, annot=heatmap_data, fmt='d', cmap='Blues', 
            cbar_kws={'label': 'Concentration (%)'}, linewidths=.5)
plt.title('Branch vs Package Range: Placement Concentration', fontsize=16, fontweight='bold', pad=25)
plt.xlabel('Package Range (LPA)', fontsize=12, labelpad=10)
plt.ylabel('Branch', fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig('final_charts/3_branch_salary_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# --- Chart 4: Year-over-Year Growth ---
plt.figure(figsize=(10, 6))
yearly_totals = df.groupby('year').size()
growth_rate = yearly_totals.pct_change() * 100
years = yearly_totals.index[1:]
rates = growth_rate.dropna()

plt.bar(years, rates, color=COLORS[2], alpha=0.7, width=0.6)
plt.plot(years, rates, marker='D', color=COLORS[0], linewidth=2)

plt.title('Annual Placement Growth Rate (%)', fontsize=16, fontweight='bold', pad=25)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Growth Rate (%)', fontsize=12)
plt.axhline(0, color='#333333', linewidth=1)
plt.grid(axis='y', alpha=0.3)

for i, rate in enumerate(rates):
    plt.text(years[i], rate + (2 if rate > 0 else -5), f'{rate:.1f}%', 
             ha='center', fontsize=10, fontweight='bold', color=COLORS[0])

sns.despine()
plt.tight_layout()
plt.savefig('final_charts/4_growth_rate.png', dpi=300, bbox_inches='tight')
plt.close()

print("Refined charts generated in 'final_charts/'")
