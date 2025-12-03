#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # Analysing Crashes

# In[2]:


df = pd.read_csv(r"C:\Users\harsh\Desktop\sensex.csv")  #To read CSV data. 
print(df.head())


# In[3]:


date_column = df.columns[0]  
print(f"Using column: {date_column}")

df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
df = df.sort_values(date_column)                        #convert the ‘Date’ column to datetime, sort the data by date.
df.set_index(date_column, inplace=True)                 #set it as the DataFrame index

print("\nDataFrame after processing:")
print(df.head())
print(f"Index type: {type(df.index)}")

df['Daily_Return'] = df['Close'].pct_change() * 100
crash_threshold_daily = -5                             #calculate the daily percentage change and identify crash days.
df['Crash_Daily'] = df['Daily_Return'] <= crash_threshold_daily

import plotly.graph_objects as go                      
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Closing Price'))

crash_days = df.index[df['Crash_Daily']]
crash_closes = df['Close'][df['Crash_Daily']]          #This shows the Sensex closing prices and highlight daily crashes.

fig.add_trace(go.Scatter(x=crash_days, y=crash_closes, mode='markers',
                          marker=dict(color='red'),
                          name=f'Daily Crash (<= {crash_threshold_daily}%)'))

fig.update_layout(
    title='Sensex Closing Price with Daily Crashes Highlighted',
    xaxis_title='Date',
    yaxis_title='Sensex Close',
    xaxis_rangeslider_visible=True,  
    template="plotly_white"
)

fig.show()


# # Analyzing Drawdowns

# In[5]:


df['Cumulative_Max'] = df['Close'].cummax()  # Calculate cumulative max and drawdown (% drop from the cumulative max)
df['Drawdown'] = (df['Close'] - df['Cumulative_Max']) / df['Cumulative_Max'] * 100


# In[6]:


drawdown_threshold = -20
fig = go.Figure()        #This shows the market drawdown over time and highlight a specific drawdown threshold

fig.add_trace(go.Scatter(x=df.index, y=df['Drawdown'], mode='lines', name='Drawdown (%)'))

fig.add_hline(y=drawdown_threshold, line_dash='dash', line_color='red',
              annotation_text=f'Drawdown Threshold ({drawdown_threshold}%)',
              annotation_position='bottom right')

fig.update_layout(
    title='Market Drawdown Over Time',
    xaxis_title='Date',
    yaxis_title='Drawdown (%)',
    xaxis_rangeslider_visible=True,  
    template="plotly_white"
)

fig.show()


# In[7]:


crash_drawdowns = df[df['Drawdown'] <= drawdown_threshold]
print("Dates where drawdown exceeded threshold:")   #identify the dates where the market drawdown exceeded the -20% threshold
print(crash_drawdowns[['Close', 'Cumulative_Max', 'Drawdown']].dropna().head(10))


# # Analyzing Periods of Crashes

# In[8]:


crash_dates = df.index[df['Drawdown'] <= drawdown_threshold]
clusters = []
current_cluster = []       #identify contiguous periods (clusters) where the drawdown is below the threshold

for date in crash_dates:
    if not current_cluster:
        current_cluster.append(date)
    else:
        if (date - current_cluster[-1]).days <= 3:
            current_cluster.append(date)
        else:
            clusters.append(current_cluster)
            current_cluster = [date]
if current_cluster:
    clusters.append(current_cluster)

print("Identified crash clusters based on drawdown threshold:")
for idx, cluster in enumerate(clusters):
    print(f"Cluster {idx+1}: {cluster[0].date()} to {cluster[-1].date()} (Total days: {len(cluster)})")


# In[11]:


#The first crash cluster and visualize the closing price, daily returns, and drawdown  
#within a 30-day window before and after the cluster
if clusters:
    cluster_start = clusters[0][0]
    cluster_end = clusters[0][-1]
    print(f"\nZooming into crash cluster from {cluster_start.date()} to {cluster_end.date()}")
    
    zoom_start = cluster_start - pd.Timedelta(days=30)
    zoom_end = cluster_end + pd.Timedelta(days=30)
    
    # Use searchsorted to find nearest valid dates
    zoom_df = df[(df.index >= zoom_start) & (df.index <= zoom_end)]
    
    fig_close = go.Figure()
    fig_close.add_trace(go.Scatter(x=zoom_df.index, y=zoom_df['Close'], mode='lines', name='Closing Price'))
    fig_close.add_vrect(x0=cluster_start, x1=cluster_end, fillcolor='red', opacity=0.3, layer='below', line_width=0, name='Crash Period')
    fig_close.update_layout(
        title=f'Sensex Closing Price from {zoom_start.date()} to {zoom_end.date()}',
        xaxis_title='Date',
        yaxis_title='Sensex Close',
        xaxis_rangeslider_visible=True,
        template="plotly_white"
    )
    fig_close.show()
    
    fig_returns = go.Figure()
    fig_returns.add_trace(go.Scatter(x=zoom_df.index, y=zoom_df['Daily_Return'], mode='lines', name='Daily Return (%)'))
    fig_returns.add_hline(y=0, line_color='black', line_width=0.8)
    fig_returns.add_vrect(x0=cluster_start, x1=cluster_end, fillcolor='red', opacity=0.3, layer='below', line_width=0, name='Crash Period')
    fig_returns.update_layout(
        title=f'Sensex Daily Returns from {zoom_start.date()} to {zoom_end.date()}',
        xaxis_title='Date',
        yaxis_title='Daily Return (%)',
        xaxis_rangeslider_visible=True,
        template="plotly_white"
    )
    fig_returns.show()
    
    fig_drawdown = go.Figure()
    fig_drawdown.add_trace(go.Scatter(x=zoom_df.index, y=zoom_df['Drawdown'], mode='lines', name='Drawdown (%)'))
    fig_drawdown.add_hline(y=drawdown_threshold, line_dash='dash', line_color='red',
                          annotation_text=f'Drawdown Threshold ({drawdown_threshold}%)',
                          annotation_position='bottom right')
    fig_drawdown.add_vrect(x0=cluster_start, x1=cluster_end, fillcolor='red', opacity=0.3, layer='below', line_width=0, name='Crash Period')
    fig_drawdown.update_layout(
        title=f'Sensex Drawdown from {zoom_start.date()} to {zoom_end.date()}',
        xaxis_title='Date',
        yaxis_title='Drawdown (%)',
        xaxis_rangeslider_visible=True,
        template="plotly_white"
    )
    fig_drawdown.show()
else:
    print("No crash clusters identified based on the drawdown threshold.")


# In[13]:


cluster1_start = pd.to_datetime("1997-11-12")
cluster1_end = pd.to_datetime("1997-12-26")
cluster49_start = pd.to_datetime("2008-08-18")
cluster49_end = pd.to_datetime("2009-01-23")
cluster79_start = pd.to_datetime("2020-03-16")
cluster79_end = pd.to_datetime("2020-04-03")

def plot_crash_period(cluster_start, cluster_end, title_suffix=""):
    zoom_start = cluster_start - pd.Timedelta(days=30)
    zoom_end = cluster_end + pd.Timedelta(days=30)
    zoom_df = df[(df.index >= zoom_start) & (df.index <= zoom_end)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=zoom_df.index, y=zoom_df['Close'], mode='lines', name='Closing Price'))
    fig.add_vrect(x0=cluster_start, x1=cluster_end, fillcolor='red', opacity=0.3, layer='below', line_width=0, name='Crash Period')
    fig.update_layout(
        title=f'Sensex Closing Price {title_suffix}<br>({zoom_start.date()} to {zoom_end.date()})',
        xaxis_title='Date',
        yaxis_title='Sensex Close',
        xaxis_rangeslider_visible=True,
        template="plotly_white"
    )
    fig.show()

def plot_daily_returns(cluster_start, cluster_end, title_suffix=""):
    zoom_start = cluster_start - pd.Timedelta(days=30)
    zoom_end = cluster_end + pd.Timedelta(days=30)
    zoom_df = df[(df.index >= zoom_start) & (df.index <= zoom_end)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=zoom_df.index, y=zoom_df['Daily_Return'], mode='lines', name='Daily Return (%)'))
    fig.add_hline(y=0, line_color='black', line_width=0.8)
    fig.add_vrect(x0=cluster_start, x1=cluster_end, fillcolor='red', opacity=0.3, layer='below', line_width=0, name='Crash Period')
    fig.update_layout(
        title=f'Sensex Daily Returns {title_suffix}<br>({zoom_start.date()} to {zoom_end.date()})',
        xaxis_title='Date',
        yaxis_title='Daily Return (%)',
        xaxis_rangeslider_visible=True,
        template="plotly_white"
    )
    fig.show()

# Plot for each crash period
plot_crash_period(cluster1_start, cluster1_end, "1997 Crash")
plot_crash_period(cluster49_start, cluster49_end, "2008-2009 Crash")
plot_crash_period(cluster79_start, cluster79_end, "2020 Crash")

# Plot daily returns for each crash period
plot_daily_returns(cluster1_start, cluster1_end, "1997 Crash")
plot_daily_returns(cluster49_start, cluster49_end, "2008-2009 Crash")
plot_daily_returns(cluster79_start, cluster79_end, "2020 Crash")


# # Developing Early Warning Signals

# In[14]:


np.random.seed(42)

dates_2025 = pd.bdate_range(start="2025-01-01", periods=250)

daily_returns = np.zeros(250)
daily_returns[:150] = np.random.normal(loc=0.0005, scale=0.01, size=150)
daily_returns[150:200] = np.random.normal(loc=-0.008, scale=0.025, size=50)
daily_returns[200:] = np.random.normal(loc=0.0005, scale=0.01, size=50)

prices = [30000]
for ret in daily_returns:
    prices.append(prices[-1]*(1+ret))
prices = prices[1:]

df_2025 = pd.DataFrame({
    'Date': dates_2025,
    'Close': prices,
    'Daily_Return': daily_returns * 100 
})
df_2025.set_index('Date', inplace=True)


# In[15]:


df_2025['Rolling_Mean_Return'] = df_2025['Daily_Return'].rolling(window=10).mean()
df_2025['Rolling_Volatility'] = df_2025['Daily_Return'].rolling(window=10).std()

warning_condition = (df_2025['Rolling_Mean_Return'] < -0.5) & (df_2025['Rolling_Volatility'] > 2)
df_2025['Warning'] = warning_condition

warnings_df = df_2025[df_2025['Warning']]
print("Early Warning Signals for 2025:")
print(warnings_df[['Close', 'Daily_Return', 'Rolling_Mean_Return', 'Rolling_Volatility']].head(15))


# In[16]:


fig = go.Figure()

fig.add_trace(go.Scatter(x=df_2025.index, y=df_2025['Close'], mode='lines', name='Closing Price'))

warning_dates = df_2025.index[df_2025['Warning']]
warning_closes = df_2025['Close'][df_2025['Warning']]

fig.add_trace(go.Scatter(x=warning_dates, y=warning_closes, mode='markers',
                          marker=dict(color='red'),
                          name='Early Warning Signal'))

fig.update_layout(
    title='Synthetic 2025 Sensex Closing Price with Early Warning Signals',
    xaxis_title='Date',
    yaxis_title='Sensex Close',
    xaxis_rangeslider_visible=True, 
    template="plotly_white"
)

fig.show()

