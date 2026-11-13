import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker  # এখানে ticker আমদানির সামান্য সংশোধন করা হয়েছে

df = pd.read_csv(
    r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv",
    index_col="Date"
)
print("connect")

df.index = pd.to_datetime(df.index, format="%d/%m/%Y")
df = df.sort_index()

yearly_avg = df['Close'].groupby(df.index.year).mean()
print('Yearly average closing price: ', yearly_avg.round(2))

fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
colors = ["#90CAF9" if year != yearly_avg.index.max() 
          else "#1565C0" for year in yearly_avg.index]

bars = ax.bar(
    yearly_avg.index.astype(str),
    yearly_avg.values,
    color=colors,
    width=0.58,
    zorder=3
)

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval + (yearly_avg.max() * 0.015),
        f"{yval:,.0f}",  # <--- এখানে স্পেসটি সরিয়ে দেওয়া হয়েছে (`,.0f`)
        ha="center",
        va='bottom',
        fontsize=9.5,
        fontweight="bold",
        color='#222222'
    )
    
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
ax.set_ylim(0, yearly_avg.max() * 1.12)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

ax.set_title(
    "S&P 500 Yearly Average Closing Price (2016-2026)",
    fontsize=15,
    fontweight="bold",
    loc="left",
    pad=15,
    color='#111111'
)

ax.set_xlabel("Year", fontsize=11, fontweight='bold', color='#333333', labelpad=10)
ax.set_ylabel("Average Index Value", fontweight='bold', color='#333333', labelpad=10) # <--- 'ylable' থেকে বানান ঠিক করে 'ylabel' করা হয়েছে

folder_name = r"E:\SP500_Analysis\charts"

# plt.savefig এর ভেতরে dpi এবং bbox_inches সঠিক নিয়মে দেওয়া হলো
plt.savefig(
    os.path.join(folder_name, "02_yearly_average_closing_price.png"), 
    dpi=300, 
    bbox_inches='tight'
)
plt.show()