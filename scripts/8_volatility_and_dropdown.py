import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# ১. ডেটা লোড ও ইনডেক্স ঠিক করা
df = pd.read_csv(r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv", index_col="Date")
df.index = pd.to_datetime(df.index, format="ISO8601")
df = df.sort_index()

# ২. ডেইলি রিটার্ন, 30-Day Rolling Volatility ও Drawdown হিসাব করা
df["Daily_Return"] = df["Close"].pct_change()
# বার্ষিকীকৃত (Annualized) ৩০-দিনের রোলিং ভলাটিলিটি (%)
df["Volatility_30D"] = df["Daily_Return"].rolling(window=30).std() * np.sqrt(252) * 100

# Drawdown (%) হিসাব: সর্বোচ্চ চূড়া (Running Peak) থেকে বর্তমান প্রাইস কত নিচে আছে
rolling_peak = df["Close"].cummax()
df["Drawdown_%"] = ((df["Close"] - rolling_peak) / rolling_peak) * 100

# ৩. মূল ইনসাইটস (Insights) বের করে টার্মিনালে প্রিন্ট করা
max_dd = df["Drawdown_%"].min()
max_dd_date = df["Drawdown_%"].idxmin()

max_vol = df["Volatility_30D"].max()
max_vol_date = df["Volatility_30D"].idxmax()
avg_vol = df["Volatility_30D"].mean()

print("=== KEY RISK & DRAWDOWN INSIGHTS (FOR PRESENTATION) ===")
print(f"1. Maximum Drawdown (Worst Crash): {max_dd:.2f}% on {max_dd_date.strftime('%d %b, %Y')}")
print(f"2. Peak Volatility (Highest Risk): {max_vol:.2f}% on {max_vol_date.strftime('%d %b, %Y')}")
print(f"3. Average Annualized Volatility: {avg_vol:.2f}%")

# ৪. ২-প্যানেল প্রফেশনাল চার্ট তৈরি (ওপরে Drawdown, নিচে Volatility)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), dpi=300, sharex=True)

# --- প্যানেল ১: Maximum Drawdown (Underwater Plot) ---
ax1.plot(df.index, df["Drawdown_%"], color="#C62828", linewidth=1.3, zorder=3)
ax1.fill_between(df.index, df["Drawdown_%"], 0, color="#EF5350", alpha=0.25, zorder=2)
ax1.axhline(0, color="#444444", linewidth=1)

# সবচেয়ে বড় পতন (Max Drawdown) হাইলাইট করা
ax1.scatter(max_dd_date, max_dd, color="#B71C1C", s=50, zorder=4)
ax1.annotate(
    f"Max Drawdown: {max_dd:.1f}%\n({max_dd_date.strftime('%b %d, %Y')})",
    xy=(max_dd_date, max_dd),
    xytext=(35, 10),
    textcoords="offset points",
    fontsize=9.5,
    fontweight="bold",
    color="#B71C1C",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFEBEE", edgecolor="#EF5350"),
    arrowprops=dict(arrowstyle="->", color="#B71C1C")
)

ax1.set_title(
    "S&P 500 Risk Analysis: Historical Drawdown & 30-Day Rolling Volatility (2016–2026)",
    fontsize=14, fontweight="bold", loc="left", pad=15, color="#111111"
)
ax1.set_ylabel("Drawdown from Peak (%)", fontsize=10.5, fontweight="bold", color="#333333")
ax1.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(True, linestyle="--", alpha=0.4)

# --- প্যানেল ২: 30-Day Rolling Volatility ---
ax2.plot(df.index, df["Volatility_30D"], color="#1565C0", linewidth=1.5, label="30-Day Annualized Volatility", zorder=3)
ax2.axhline(avg_vol, color="#FF8F00", linestyle="--", linewidth=1.5, label=f"Average Volatility ({avg_vol:.1f}%)", zorder=4)

# সর্বোচ্চ ভলাটিলিটি হাইলাইট করা
ax2.scatter(max_vol_date, max_vol, color="#0D47A1", s=50, zorder=5)
ax2.annotate(
    f"Peak Volatility: {max_vol:.1f}%\n({max_vol_date.strftime('%b %d, %Y')})",
    xy=(max_vol_date, max_vol),
    xytext=(35, -15),
    textcoords="offset points",
    fontsize=9.5,
    fontweight="bold",
    color="#0D47A1",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#E3F2FD", edgecolor="#42A5F5"),
    arrowprops=dict(arrowstyle="->", color="#0D47A1")
)

ax2.set_ylabel("Annualized Volatility (%)", fontsize=10.5, fontweight="bold", color="#333333")
ax2.set_xlabel("Year", fontsize=11, fontweight="bold", color="#333333", labelpad=10)
ax2.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
ax2.xaxis.set_major_locator(mdates.YearLocator(1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(True, linestyle="--", alpha=0.4)
ax2.legend(frameon=False, loc="upper right", fontsize=10)

plt.tight_layout()
plt.savefig(r"E:\SP500_Analysis\charts\06_volatility_and_drawdown.png", dpi=300, bbox_inches="tight")
plt.show()
