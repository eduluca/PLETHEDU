import pandas as pd
#from IPython.display import display

ioxpath = "H:\Documents\LabVIEW\\true_IOXPleth_file.xlsx"
co2path = "H:\Documents\LabVIEW\\true_CO2Analyzer_file.csv"


iox = pd.read_excel(ioxpath)                                                    #Read IOX excel file
co2 = pd.read_csv(co2path, encoding= 'unicode_escape')                          #Read CO2 excel file

print(iox.columns)
iox.columns.values[6] = "c6"

# Find the row index where "parameter" is present in the specified column
start_row = iox[iox["c6"].str.contains("parameter", na=False)].index[0]

# Read the Excel file again, skipping the rows before the identified row index
df = pd.read_excel(ioxpath, skiprows = start_row + 1)

df.columns.values[5] = "c5"


# Delete rows containing the word 'analyzer'
df = df[~df['c5'].astype(str).str.contains('analyzer')]

#pd.set_option('display.max_columns', None)  # None: Display all columns
#pd.set_option('display.max_rows', None)  # None: Display all rows

df


print("brrrrrr")