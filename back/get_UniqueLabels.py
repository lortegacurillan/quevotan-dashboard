import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
from back.get_Data import get_Data
import streamlit as st
from back.get_Query import get_QueryResponse

df = get_Data('sampled')
df_mismatches = pd.DataFrame(columns=['Index', 'vote_name', 'GPT_Predictions', 'RTM_Predictions'])

# Function to check if GPT and RTM predictions are the same
def check_UniqueLabels(df: pd.DataFrame, row, vote_Name):
    '''
    This function checks if the GPT and RTM predictions are the same for a given row in the DataFrame

    Parameters:
    df (pd.DataFrame): The DataFrame with the labels
    row (pd.Series): The row to check
    vote_Name (str): The name of the vote

    Returns:
    Tuple: A tuple with the row index, vote name, GPT predictions, and RTM predictions if they are different, otherwise None
    '''
    prediction_GPT = row.iloc[13:23].values
    prediction_RTM = get_QueryResponse(vote_Name)
    
    if not np.array_equal(prediction_GPT, prediction_RTM):
        return row.name, vote_Name, prediction_GPT, prediction_RTM
    else:
        return None

def add_ToDataFrame(mismatch_data, df_mismatches):
    '''
    This function adds mismatch data to the DataFrame

    Parameters:
    mismatch_data (Tuple): A tuple with the row index, vote name, GPT predictions, and RTM predictions
    df_mismatches (pd.DataFrame): The DataFrame to add the mismatch data to

    Returns:
    pd.DataFrame: The updated DataFrame with the mismatch data
    '''
    
    row_index, vote_name, prediction_GPT, prediction_RTM = mismatch_data

    new_row = {
        'Index': row_index,
        'vote_name': vote_name,
        'GPT_Predictions': prediction_GPT,
        'RTM_Predictions': prediction_RTM
    }

    new_row = pd.DataFrame([mismatch_data])  # Assuming mismatch_data is a dict or a row of data
    df_mismatches = pd.concat([df_mismatches, new_row], ignore_index=True)
    return df_mismatches

# Loop through the dataframe and compare predictions, adding mismatches to the DataFrame
for index, row in df.iterrows():
    vote_Name = row['votaciones_Nombre']
    mismatch_data = check_UniqueLabels(df, row, vote_Name)
    if mismatch_data:
        df_mismatches = add_ToDataFrame(mismatch_data, df_mismatches)

# Save the mismatches DataFrame to an Excel file in the 'data' folder
output_file_path = os.path.join('./data/', 'mismatches.xlsx')
df_mismatches.to_excel(output_file_path, index=False)

print(f"Mismatch data has been saved to {output_file_path}")