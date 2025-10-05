import pandas as pd

# Make sure you have openpyxl installed:
# pip install openpyxl

df = pd.read_excel('/workspaces/DFIG/Agri.xlsx')   # Updated path
print(df.shape)                   # prints (rows, columns)
print(df.head())                  # prints first 5 rows
