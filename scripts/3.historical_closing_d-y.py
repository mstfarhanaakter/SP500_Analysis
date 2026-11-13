import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

df = pd.read_csv(
    r"E:\SP500_Analysis\data\clean\sp500_cleaned_data.csv")
print("connected")

#Date column to index


s = df["Date"].astype(str).str.strip()
df["Date"] = pd.to_datetime(s.where(s.str.contains("/")), format="%d/%m/%Y").fillna(
    pd.to_datetime(s.where(s.str.contains("-")), format="%Y-%m-%d")
)
df = df.set_index("Date").sort_index()
print("Max Date:", df.index.max())

df.to_csv(r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv", index=True)
print("Clean CSV saved successfully!")


# %% Folder Check and Create

folder_name =r"E:\SP500_Analysis\charts"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print("Folder name successfully created")
else:
    print("Folder is already exists")
    
# Historical Closing Price

fig,ax = plt.subplots(figsize=(14,6),dpi=300)

#Main line Plot
line_color = "#1E88E5"
ax.plot(
        df.index,
        df["Close"],
        color=line_color,
        linewidth= 1.8,
        label = "S&P 500 Closing Price",
        zorder =3
        )

#for professional look
ax.fill_between(
    df.index,
    df["Close"],
    df["Close"].min()* 0.95,
    color=line_color,
    alpha= 0.10,
    zorder = 2
    )

# X-Axis

ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# Y-Axis (,)

ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

#Up and down border cut

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

ax.grid(True, linestyle= "--", alpha=0.4, color= "#BDBDBD", zorder =  0)

# Tite, label, legend

ax.set_title(
    "S&P 500 Historical Closing Price(2016-2026)",
    fontsize = 15, 
    fontweight = 'bold',
    loc = 'left',
    pad = 15, 
    color= '#111111'
    )

ax.set_xlabel("Year", fontsize = 11, fontweight='bold', color= '#333333', labelpad = 10)
ax.set_ylabel("Index Value", fontsize = 11, fontweight='bold', color= '#333333', labelpad = 10)
ax.legend(frameon = False, loc='upper left', fontsize=11)

# save and show the files

plt.savefig(
    os.path.join(folder_name, "01_historical_closing_price.png"),
    dpi = 300,
    bbox_inches= "tight"
    )

print("succfully created in the folder path")
plt.show()