import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# Data load and index
df = pd.read_csv(
    r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv",
    index_col='Date'
)
df.index = pd.to_datetime(df.index, format='ISO8601')
df = df.sort_index()

# 50-Day ও 200-Day Moving Average
df["SMA_50"] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# create Chart
fig, ax = plt.subplots(figsize=(14, 6), dpi=300)

ax.plot(
    df.index, 
    df['Close'], 
    color="#B0B5C5", 
    linewidth=1.2,
    alpha=0.8,
    label="Daily Close"
)

ax.plot(
    df.index,
    df['SMA_50'],
    color='#1E88E5',
    linewidth=1.6,
    label='50-Day SMA (Short-Term Trend)'
)
ax.plot(
    df.index,
    df['SMA_200'],
    color='#E53935',
    linewidth=2.0,
    label='200-Day SMA (Long-Term Trend)'
)

# Format and border clean
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Y-axis এর জন্য কমা ফরম্যাট (এখানে ঠিক করে দেওয়া হয়েছে)
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, linestyle='--', alpha=0.4)

ax.set_title(
    "S&P 500 Trend Analysis: 50-Day vs 200-Day Moving Average",
    fontsize=14, 
    fontweight='bold',
    loc='left',
    pad=15
)

ax.set_ylabel("Index Value", fontsize=11, fontweight='bold')
ax.legend(frameon=False, loc='upper left', fontsize=10.5)

folder_name = r"E:\SP500_Analysis\charts"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print("folder name created successfully")
else:
    print("Folder already exists")

plt.savefig(os.path.join(folder_name, '03_moving_average.png'), dpi=300, bbox_inches='tight')

print("Successfully created in the designated folder")
plt.show()