import pandas as pd
import numpy as np
import sys
from scipy.stats import zscore, percentileofscore
from scipy.spatial import distance
from scipy.spatial.distance import mahalanobis

#Comment to make easier for anyone who sees code after

#ioxpath = "H:\Documents\LabVIEW\\true_IOXPleth_file.xlsx"
#co2path = "H:\Documents\LabVIEW\\true_CO2Analyzer_file.csv"

##################### READING FILES FUNCTIONS ######################################


def readiox(ioxpath):
    iox = pd.read_csv(ioxpath, encoding= 'unicode_escape')                          #Read IOX excel file

    return iox

def readco2(co2path):
    co2 = pd.read_csv(co2path, encoding= 'unicode_escape')                          #Read CO2 excel file

    return co2


##################### CLEANING EXCEL FILE FUNCTIONS ######################################

def cleanit(iox):
    ############## DELETING ############################
    df = iox

    # Helps visualization
    df.columns.values[6] = "c6"
    
    # Find the row index where "parameter" is present in the specified column
    start_row = df[df["c6"].str.contains("parameter", na=False)].index[0]

    # Read the Excel file again, skipping the rows before the row with "parameter"
    df = pd.read_excel(ioxpath, skiprows = start_row + 1)
    
    # Delete last 6 rows
    df.drop(df.tail(6).index, inplace = True)
    
    # Delete rows containing the word 'analyzer' and 'period-stop'
    df.rename(columns={df.columns[5]: "c5"}, inplace=True)
    df = df[~df["c5"].astype(str).str.contains('analyzer')]
    df = df[~df["c5"].astype(str).str.contains('period-stop')]
    df.rename(columns={df.columns[6]: "c6", df.columns[8]: "c8"}, inplace=True)
    
    # Populate column 'c8' with values from 'c6' until the next non-null value is encountered
    df['c8'] = df.groupby(df['c6'].notnull().cumsum())['c6'].transform(lambda x: x.ffill())
    
    # Delete columns 0,5-8
    df = df.drop(columns = df.columns[0])
    df = df.drop(columns = df.columns[4:7])

    # Delete rows 0-5
    df = df.drop(labels = range(0,5), axis = 0)
    
    
    ################# ADDING/MOVING ##################
    df.columns.values[5] = "c5"
    df = df.dropna(subset=["c5"]) #Remove unwanted NaNs
    df.insert(0, "Sample", df["c5"])



    ################# RENAMING ########################
    df.columns.values[0] = "Sample"
    df.columns.values[1] = "CPU Date"
    df.columns.values[2] = "CPU Time"
    df.columns.values[3] = "Site Time"
    df.columns.values[4] = "Period Time"
    df.columns.values[5] = "Protocol Type"
    df.columns.values[6] = "Storage ID"
    df.columns.values[7] = "First Beat ID"
    df.columns.values[8] = "Last Beat ID"
    df.columns.values[9] = "Ti (msec)"
    df.columns.values[10] = "Te (msec)"
    df.columns.values[15] = "RT (msec)"
    df.columns.values[17] = "P (msec)"
    df.columns.values[18] = "f (bpm)"
    df.columns.values[19] = "EIP (msec)"
    df.columns.values[20] = "EEP (msec)"
    
    
    # Reset the row headers to start from 1
    df = df.reset_index(drop=True)
    
    
    pd.set_option('display.max_columns', None)  # None: Display all columns
    pd.set_option('display.max_rows', None)  # None: Display all rows

    return df



################## ADD OTHER PLETHYSMOGRAPHY VALUES #########################
def addvalues(df):
    mid_df = df.copy()  # Create a copy of the original DataFrame to avoid modifying it
    
    # Define the weights for each variable
    weights = {
        'TV': 0.4,
        'Ti (msec)': 0.2,
        'Te (msec)': 0.2,
        'PIF': 0.2
    }
    
    
    # Calculate the z-scores, percentiles, and Mahalanobis distances for each variable
    for variable in ['TV', 'Ti (msec)', 'Te (msec)', 'PIF']:
        mean = mid_df[variable].mean()
        std = mid_df[variable].std()
        mid_df[f'{variable}_ZScore'] = (mid_df[variable] - mean) / std
        mid_df[f'{variable}_Percentile'] = mid_df[variable].rank(pct=True)
        cov = np.cov(np.stack(mid_df[variable]), rowvar=False)
        mean_vector = np.array([mean])
        mid_df[f'{variable}_MahalanobisDistance'] = mid_df[variable].apply(
            lambda x: distance.mahalanobis([x], mean_vector, cov)
        )

    # Calculate the weighted composite score
    variables = ['TV', 'Ti (msec)', 'Te (msec)', 'PIF']
    composite_score = np.zeros(len(mid_df))
    for variable in variables:
        composite_score += (
            weights[variable] * mid_df[f'{variable}_ZScore'] +
            weights[variable] * mid_df[f'{variable}_Percentile'] +
            weights[variable] * mid_df[f'{variable}_MahalanobisDistance']
        )

    # Assign the composite score to a new column
    mid_df['BreathIrregularityScore'] = composite_score

    return mid_df

################## COMBINE IOX UPDATED DATAFRAME WITH CO2 DATAFRAME ##########
def combineit(mid_df,co2):
    finaldf = mid_df
    
    # Append co2 to the right of mid_df with four spaces in between
    finaldf = pd.concat([finaldf, pd.DataFrame(columns=['', '', '', '']), co2], axis=1)
    

    return finaldf


####################### SAVE FINAL DATAFRAME AS EXCEL #########################
def excel_saveit(df):

    # determining the path and name of the file
    file_path = 'H:\Documents\LabVIEW\ioxco2_testing_finaldf.xlsx'
  
    # saving the excel
    df.to_excel(file_path, index = False)
    print('IOX + CO2 DataFrame is written to Excel File successfully.')


#df = cleanit(iox)
#mid_df = addvalues(df)
#finaldf = combineit(mid_df,co2)



