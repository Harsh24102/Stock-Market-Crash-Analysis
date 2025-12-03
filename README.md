# 📉 SENSEX Stock Market Crash Analysis (1997-2024)

![Status: Complete](https://img.shields.io/badge/Status-Complete-green.svg)
[![Tech Stack](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Tech Stack](https://img.shields.io/badge/Pandas-Data_Analysis-orange.svg)](https://pandas.pydata.org/)
[![Tech Stack](https://img.shields.io/badge/Visualization-Matplotlib_Seaborn-red.svg)](https://matplotlib.org/)

## 1. Project Goal

The primary objective of this project is to analyze historical SENSEX data from 1997 to the present to **identify, visualize, and quantify major stock market crashes** and periods of high volatility. The analysis focuses on calculating key metrics like drawdowns and recovery periods to understand market behavior.

## 2. Methodology and Key Analysis Steps

The analysis is performed within the **`Stock Market Crash Analysis.ipynb`** Jupyter Notebook and follows these steps:

1.  **Data Loading and Cleaning:** Load the `sensex.csv` data and perform initial cleaning, focusing on converting the date column and handling the data types for price and volume columns.
2.  **Drawdown Calculation:** Calculate the **maximum drawdown** (the peak-to-trough decline during a specific period) to quantitatively define a crash.
3.  **Crash Identification:** Identify specific historical market crashes (e.g., dot-com bubble, 2008 financial crisis, COVID-19 drop) based on severe drawdown metrics.
4.  **Visualization:** Generate time-series plots to visualize the SENSEX index price and overlay the identified crash periods for clear communication of results.

## 3. Technology Stack

* **Core Language:** Python 3.x
* **Data Manipulation:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn (Inferred from standard practice for this type of analysis)

## 4. Data Source

The project uses historical daily price data for the SENSEX index.
* **File:** `data/sensex.csv`
* **Columns Include:** `Date`, `Close`, `High`, `Low`, `Open`, `Volume`.

## 5. How to Run This Project

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Harsh24102/Stock-Market-Crash-Analysis.git](https://github.com/Harsh24102/Stock-Market-Crash-Analysis.git)
    ```
2.  **Install Dependencies:**
    ```bash
    pip install pandas numpy matplotlib seaborn # Ensure all necessary libraries are installed
    ```
3.  **Run the Notebook:** Open the `Stock Market Crash Analysis.ipynb` file in Jupyter Lab or VS Code to step through the analysis and generate the visualizations.

---
