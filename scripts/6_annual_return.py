import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv(
    r"E:\SP500_Analysis\data\clean\sp500_final_clean.csv",
    index_col= 'Date'
    )

df.index = pd.to_datetime(df.index, format= 'ISO8601')
df = df.sort_index()


yearly_close = df['Close'].resample('YE').last()
annual_returns = yearly_close.pct_change() * 100

first_year_return = (
    (yearly_close.iloc[0]- df['Close'].iloc[0])/
    df['Close'].iloc[0])*100

annual_returns.iloc[0] = first_year_return

annual_returns.index = annual_returns.index.year

print("=== S&P 500 Annual Returns (%) ===")
print(annual_returns.round(2))

# =============================================================================
# #chart create
# =============================================================================

fig, ax = plt.subplots(figsize=(16, 4), dpi = 300)
colors = [
    '#2E7D32'if val >=0
    else '#C62828' for val in 
    annual_returns.values ]

bars = ax.bar(
    annual_returns.index.astype(str),
    annual_returns.values,
    color= colors,
    width = 0.58,
    zorder = 3
    )

ax.axhline(0, color = '#444444', linewidth= 1.2, zorder = 4)

for bar in bars:
    yval = bar.get_height()
    offset = 1.2 if yval >=0 else -2.2
    va_align = "bottom" if yval >0 else "top"
    sign = "+" if yval > 0 else ""
    
    ax.text(
        bar.get_x() + bar.get_width()/2,
        yval + offset,
        f"{sign}{yval:.1f}%",
        ha="center",
        va= va_align,
        fontsize = 9.5,
        fontweight = 'bold',
        color = '#222222'
        )
    
# =============================================================================
# # Y-Axis clean 
# =============================================================================

ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals = 0))
ax.set_ylim(annual_returns.min() - 8, annual_returns.max() + 8)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.yaxis.grid(True, linestyle = '--', alpha = 0.4, color = '#BDBDBD',zorder = 0)


# =============================================================================
# Title and label
# =============================================================================

ax.set_title(
    "S&P 500 Annual Returns (%) - Year-over-Year Performance (2016-2026)",
    fontsize= 14, 
    fontweight = 'bold',
    loc = 'left',
    pad = 15,
    color = '#111111'
    )

ax.set_xlabel(
    "Year",
    fontsize = 11,
    fontweight = 'bold',
    color = '#333333',
    labelpad = 10
    )
ax.set_ylabel(
    'Annual Return (%)',
    fontsize = 11,
    fontweight = 'bold',
    color = '#333333',
    labelpad = 10
    )

# =============================================================================
# Save and show
# =============================================================================

plt.savefig(
    r"E:\SP500_Analysis\charts\04_anuual_returns.png",
    dpi = 300,
    bbox_inches = 'tight'
    )
plt.show()






















