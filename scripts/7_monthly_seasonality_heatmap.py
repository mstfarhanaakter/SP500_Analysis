import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(
    r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv",
    index_col = "Date"
    )
print("connect")

df.index = pd.to_datetime(df.index, format='ISO8601')
df = df.sort_index()

monthly_close = df['Close'].resample('ME').last()
monthly_returns = monthly_close.pct_change() * 100

first_month_return = (
    (monthly_close.iloc[0] - df['Close'].iloc[0])/
    df['Close'].iloc[0]) * 100

monthly_returns.iloc[0] = first_month_return

heatmap_df = pd.DataFrame({
    "Year": monthly_returns.index.year,
    "Month": monthly_returns.index.month,
    "Return": monthly_returns.values
    })

pivot_table = heatmap_df.pivot(
    index = "Year", columns="Month", values="Return"
    )

month_names = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

pivot_table.columns = [month_names[m-1] for m in pivot_table.columns]

fig,ax = plt.subplots(figsize= (14, 7), dpi = 300)

sns.heatmap(
    pivot_table,
    annot= True,
    fmt='.1f',
    cmap = 'RdYlGn',
    center = 0,
    linewidths = 1.5,
    linecolor = 'white',
    cbar_kws={'label': "Monthly Return (%)", 'shrink': 0.82},
    annot_kws= {'size': 10, 'weight': 'bold'},
    ax = ax
    )

ax.set_title(
    "S&P 500 Monthly Seasonlity Heatmap - Monthly Returns (%) (2016-2026)",
    fontsize = 15, 
    fontweight = 'bold',
    loc = 'left',
    pad = 20,
    color = "#111111"
    )

ax.set_xlabel(
    "Month", 
    fontsize = 11, 
    fontweight = 'bold',
    color = '#333333', 
    labelpad = 12
    )

ax.set_ylabel(
    "Year", 
    fontsize = 11, 
    fontweight = 'bold',
    color = '#333333', 
    labelpad = 12
    )

# y - axis letter not rotate stay straight
ax.tick_params(axis = 'y', rotation = 0, labelsize = 10.5)
ax.tick_params(axis = 'x', labelsize = 10.5)

plt.savefig(
    r"E:\SP500_Analysis\charts\05_monthly_seasonality_heatmap.png",
    dpi = 300,
    bbox_inches = 'tight'
    )
print("charts created to the destinated folder")
plt.show()











































