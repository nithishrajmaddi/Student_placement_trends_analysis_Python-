import pandas as pd
import numpy as np
import os

# Create directory for raw data
os.makedirs('raw_data', exist_ok=True)

years = [2020, 2021, 2022, 2023, 2024]
branches = ['Computer Science', 'Information Technology', 'Electronics', 'Mechanical', 'Civil']
package_ranges = ['3-6 LPA', '6-10 LPA', '10-15 LPA', '15-25 LPA', '25+ LPA']

# Generate 4 disparate datasets
# Dataset 1: CS & IT (2020-2022)
data1 = []
for year in [2020, 2021, 2022]:
    for branch in ['Computer Science', 'Information Technology']:
        count = np.random.randint(50, 150)
        for _ in range(count):
            data1.append({
                'Year': year,
                'Branch': branch,
                'Student_ID': f'STU_{year}_{np.random.randint(1000, 9999)}',
                'Package': np.random.choice(package_ranges, p=[0.3, 0.4, 0.2, 0.08, 0.02]),
                'Status': 'Placed'
            })
pd.DataFrame(data1).to_excel('raw_data/cs_it_placements_v1.xlsx', index=False)

# Dataset 2: Core Branches (2020-2022)
data2 = []
for year in [2020, 2021, 2022]:
    for branch in ['Electronics', 'Mechanical', 'Civil']:
        count = np.random.randint(30, 100)
        for _ in range(count):
            data2.append({
                'Academic_Year': f'{year}-{year+1}',
                'Department': branch,
                'ID': np.random.randint(10000, 99999),
                'Salary_Range': np.random.choice(package_ranges, p=[0.5, 0.3, 0.15, 0.04, 0.01]),
                'Placement_Status': 'Yes'
            })
pd.DataFrame(data2).to_excel('raw_data/core_branches_archive.xlsx', index=False)

# Dataset 3: All branches (2023)
data3 = []
for branch in branches:
    count = np.random.randint(60, 180)
    for _ in range(count):
        data3.append({
            'Year': 2023,
            'Branch_Name': branch,
            'Roll_No': f'23B_{np.random.randint(100, 999)}',
            'LPA': np.random.choice(package_ranges, p=[0.2, 0.4, 0.25, 0.1, 0.05]),
            'Placed': 1
        })
pd.DataFrame(data3).to_excel('raw_data/placements_2023_final.xlsx', index=False)

# Dataset 4: All branches (2024) - different format
data4 = []
for branch in branches:
    count = np.random.randint(70, 200)
    for _ in range(count):
        data4.append({
            'Year_Of_Passing': 2024,
            'Stream': branch,
            'Candidate_ID': f'C24_{np.random.randint(1000, 9999)}',
            'Package_Category': np.random.choice(package_ranges, p=[0.15, 0.35, 0.3, 0.15, 0.05]),
            'Is_Placed': 'True'
        })
pd.DataFrame(data4).to_csv('raw_data/batch_2024_report.csv', index=False)

print("Generated 4 disparate datasets in 'raw_data/'")
