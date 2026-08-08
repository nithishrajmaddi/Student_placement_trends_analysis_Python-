Student Placement Trends Analysis (Python)
This project analyzes 5 years of college placement data (2020-2024) to identify hiring trends across different academic branches and package ranges. It demonstrates data cleaning, merging disparate datasets, and high-quality data visualization using Python.

Key Features
Data Integration: Cleaned and merged 4 disparate Excel/CSV datasets into a single structured dataset.
Trend Analysis: Identified year-over-year hiring patterns by branch.
Salary Insights: Analyzed package distribution and branch-wise salary concentrations.
Growth Metrics: Calculated annual placement growth rates.
Visualizations
The project generates several high-quality charts:

Placement Trends by Branch: Line chart showing YoY growth for each department.
Package Distribution: Bar chart showing the overall spread of salary packages.
Branch-wise Salary Heatmap: Matrix visualization of salary concentrations per branch.
Annual Growth Rate: Combined bar and line chart for YoY percentage changes.
Project Structure
StudentPlacementAnalysis/
├── data/
│   ├── raw/             # Original disparate datasets
│   └── processed/       # Cleaned and merged dataset
├── src/
│   └── analysis.py      # Main analysis and visualization script
├── visualizations/      # Generated high-quality charts
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
How to Run
Clone the repository.
Install dependencies:
pip install -r requirements.txt
Run the analysis:
python src/analysis.py
Requirements
pandas
matplotlib
seaborn
openpyxl (for Excel files)
