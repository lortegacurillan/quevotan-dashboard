import os
import pandas as pd
import numpy as np

# Define the path to the mismatches file
input_file_path = os.path.join('./data/', 'mismatches.xlsx')
output_file_path = os.path.join('./data/', 'filtered_mismatches.xlsx')

# Load the mismatches DataFrame from the Excel file
df_mismatches = pd.read_excel(input_file_path)

print(df_mismatches.columns)
filtered_mismatches = []

for i in df_mismatches[0]:
    prediction_GPT = np.array(df_mismatches[2][i])
    prediction_RTM = np.array(df_mismatches[3][i][1:22])

    if not np.array_equal(prediction_GPT, prediction_RTM):
        print(i,"differs:\n",prediction_GPT,'\n',prediction_RTM)
        mismatch_row = {
            'index': i,
            'vote_Name': df_mismatches[1][i],
            'prediction_GPT': prediction_GPT,
            'prediction_RTM': prediction_RTM,
        }
        filtered_mismatches.append(mismatch_row)
    else:
        print(i,"had equal predictions: ",prediction_GPT,"vs",prediction_RTM) 

df_filtered_mismatches = pd.DataFrame(filtered_mismatches)
df_filtered_mismatches.to_excel(output_file_path, index=False)