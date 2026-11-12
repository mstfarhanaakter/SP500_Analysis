import os
import pandas as pd
import numpy as np

# Data Load

df = pd.read_csv(
    r"E:\SP500_Analysis\data\raw\sp500_raw_data.csv")

# print("successfully conected")!!
file_path= r"E:\SP500_Analysis\data\clean"
if not os.path.exists(file_path):
    os.makedirs(file_path)
    print("Folder created Successfully ")
else:
    print("Forlder is already Exists")
     

clean_data = df.copy()

# Remove duplicate dates

clean_data = clean_data[~clean_data.index.duplicated(keep="first")]
print(clean_data, "successfull")

#Remove rows where closing price ar missing
clean_data = clean_data.dropna(subset=['Close'])

#Convert Numeric to column

numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

for col in numeric_columns:
    if col in clean_data.columns:
        clean_data[col] = pd.to_numeric(clean_data[col], errors= 'coerce')

# aging missing closing price again
clean_data= clean_data.dropna(subset=['Close'])

print("data cleaning complete")
print("Missing values after cleaning:\n", df.isnull().sum())


print("Cleaned dataset saved successfully")

save_path = os.path.join(file_path, "sp500_cleaned_data.csv")
clean_data.to_csv(save_path, index=False)




