import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# Set up visual style
COLORS = ['#4080FF', '#57A9FB', '#37D4CF', '#23C343', '#FBE842', '#FF9A2E', '#A9AEB8']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['grid.color'] = '#E0E0E0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['axes.edgecolor'] = '#333333'

# Try to set CJK font
# Common paths for CJK fonts on Ubuntu
cjk_font_paths = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'
]
font_prop = None
for path in cjk_font_paths:
    if os.path.exists(path):
        font_prop = fm.FontProperties(fname=path)
        plt.rcParams['font.family'] = font_prop.get_name()
        break

# --- 1. Data Cleaning & Merging ---

# Load Dataset 1
df1 = pd.read_excel('raw_data/cs_it_placements_v1.xlsx')
df1 = df1.rename(columns={'Year': 'year', 'Branch': 'branch', 'Package': 'package'})
df1 = df1[['year', 'branch', 'package']]

# Load Dataset 2
df2 = pd.read_excel('raw_data/core_branches_archive.xlsx')
df2['year'] = df2['Academic_Year'].str.split('-').str[0].astype(int)
df2 = df2.rename(columns={'Department': 'branch', 'Salary_Range': 'package'})
df2 = df2[['year', 'branch', 'package']]

# Load Dataset 3
df3 = pd.read_excel('raw_data/placements_2023_final.xlsx')
df3 = df3.rename(columns={'Year': 'year', 'Branch_Name': 'branch', 'LPA': 'package'})
df3 = df3[['year', 'branch', 'package']]

# Load Dataset 4
df4 = pd.read_csv('raw_data/batch_2024_report.csv')
df4 = df4.rename(columns={'Year_Of_Passing': 'year', 'Stream': 'branch', 'Package_Category': 'package'})
df4 = df4[['year', 'branch', 'package']]

# Merge all
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Order package ranges
pkg_order = ['3-6 LPA', '6-10 LPA', '10-15 LPA', '15-25 LPA', '25+ LPA']
df['package'] = pd.Categorical(df['package'], categories=pkg_order, ordered=True)

# --- 2. Visualizations ---

os.makedirs('output_charts', exist_ok=True)

# Chart 1: Placement Trends by Branch (Year over Year)
plt.figure(figsize=(12, 7))
trend_data = df.groupby(['year', 'branch']).size().unstack()
trend_data.plot(kind='line', marker='o', color=COLORS, linewidth=2, ax=plt.gca())
plt.title('Student Placement Trends by Branch (2020-2024)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Placements', fontsize=12)
plt.grid(True)
plt.legend(title='Branch', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('output_charts/1_placement_trends_by_branch.png', dpi=300)
plt.close()

# Chart 2: Package Distribution (Overall)
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='package', palette=COLORS)
plt.title('Overall Package Distribution (2020-2024)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Package Range (LPA)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('output_charts/2_package_distribution.png', dpi=300)
plt.close()

# Chart 3: Branch-wise Package Range Analysis (Heatmap)
plt.figure(figsize=(12, 8))
heatmap_data = pd.crosstab(df['branch'], df['package'])
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'})
plt.title('Branch vs Package Range Heatmap', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Package Range (LPA)', fontsize=12)
plt.ylabel('Branch', fontsize=12)
plt.tight_layout()
plt.savefig('output_charts/3_branch_package_heatmap.png', dpi=300)
plt.close()

# Chart 4: Hiring Growth Rate (Percentage Change)
plt.figure(figsize=(10, 6))
growth = df.groupby('year').size().pct_change() * 100
growth.plot(kind='bar', color=COLORS[0], edgecolor='black', ax=plt.gca())
plt.title('Annual Placement Growth Rate (%)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Growth Rate (%)', fontsize=12)
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('output_charts/4_annual_growth_rate.png', dpi=300)
plt.close()

print("Charts generated successfully in 'output_charts/'")
df.to_csv('cleaned_placement_data.csv', index=False)
print("Cleaned data saved to 'cleaned_placement_data.csv'")
