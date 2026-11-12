import yfinance as yf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

print("All libraries imported successfully")

ticker = "^GSPC"
sp500 = yf.Ticker(ticker)
print("Ticker", ticker)
print("Downloading s&p500 data...")

start_date = "2016-01-01"
end_date = (
    datetime.today() + timedelta(days=1)
).strftime("%Y-%m-%d")

data = yf.download(
    ticker,
    start= start_date,
    end = end_date,
    interval= "1d",
    auto_adjust = False,
    progress = True,
    multi_level_index= False
    )

# Date - From index to just general
data.reset_index(inplace=True)



print(data.head())
print(data.tail())
print("Total observations: ", len(data))

# =============================================================================
# Raw data Save
# =============================================================================


folder_name = r"E:\SP500_Analysis\data\raw"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print("successfully folder_name created", os.path.abspath(folder_name))
else:
    print("Folder already exists", os.path.abspath(folder_name))


data.to_csv(
    r"E:\SP500_Analysis\data\raw\sp500_raw_data.csv", index=False
    )


print("The file is successfully added to the folder")



# =============================================================================
# Initial data exploration
# =============================================================================

print("\nDataset shape", data.shape)
print("First 5 Rows:", data.head())
print("last 5 Rows", data.tail())
print("Dataset Information", data.info())
print("Statistical Summary", data.describe())

print("missing value:", data.isnull().sum())

print("duplicate values", data.index.duplicated().sum())

print("data types", data.dtypes)













