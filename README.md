# 📉 SENSEX Stock Market Crash Analysis (1997–2025)

![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-charts-3F4F75?logo=plotly&logoColor=white)

An analysis of daily **SENSEX** prices from July 1997 to March 2025 that finds, measures and
charts major market crashes using **drawdowns** (the fall from the previous peak), and tests a
simple **early-warning rule** on the real history.

## Key results

| Crash | Drawdown first crossed −20 % | Bottom | Deepest drawdown | Warning rule fired |
|---|---|---|---|---|
| 1997–98 Asian crisis | 12 Nov 1997 | 20 Oct 1998 | −39.2 % | 13 May 1998 |
| 2008–09 Global financial crisis | 11 Feb 2008 | 9 Mar 2009 | −60.9 % | 21 Jan 2008 (before the −20 % breach) |
| 2020 COVID-19 crash | 12 Mar 2020 | 23 Mar 2020 | −38.1 % | 12 Mar 2020 |

The warning rule fired on 255 of 6,835 trading days. It flagged the 2008 crash early and the
2020 crash on its first day, but only came late for 1997–98, when the fall was slower.

## Method

1. **Load and clean** the daily data (`Data/sensex.csv`): parse dates, sort, skip the extra
   header row the download tool adds.
2. **Daily crashes:** days with a fall of 5 % or more.
3. **Drawdowns:** each day's close compared with the highest close so far.
4. **Crash clusters:** runs of days with drawdown below −20 %.
5. **Crash periods:** for each of the three crashes, from the first −20 % day to the bottom,
   found from the data rather than hard-coded.
6. **Early-warning rule:** warn when the 10-day average daily return is below −0.5 % **and**
   10-day volatility is above 2 %. Shown first on a simulated year, then tested on the real data.

## Repository structure

| File / folder | Purpose |
|---|---|
| `Stock Market Crash Analysis.ipynb` | Main notebook with the full analysis and charts (charts are visible on GitHub) |
| `Stock Market Crash Analysis.py` | Same analysis as a script; charts open in your browser |
| `Data/sensex.csv` | SENSEX daily prices (Date, Close, High, Low, Open, Volume) |
| `Getting Started with Stock Market Crash Analysis with Python.docx` | Write-up of the approach |

## Run it

```bash
git clone https://github.com/Harsh24102/Stock-Market-Crash-Analysis.git
cd Stock-Market-Crash-Analysis
pip install pandas numpy plotly jupyter
jupyter notebook "Stock Market Crash Analysis.ipynb"
```

Optional: `pip install kaleido` to also save static PNG copies of the charts.

**Tech:** Python · pandas · NumPy · Plotly · Jupyter
