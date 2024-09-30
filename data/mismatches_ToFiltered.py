import pandas as pd
import numpy as np
from sqlalchemy import create_engine, sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER
from back.get_DB_Connection import DATABASE_URI

# Initialize database connection
engine = create_engine(DATABASE_URI)

# Define the table names
input_table_name = 'mismatches'
output_table_name = 'filtered_mismatches'

# Load the mismatches DataFrame from the database table
df_mismatches = pd.read_sql_table(input_table_name, con=engine)

print(df_mismatches.columns)
filtered_mismatches = []

# Function to clean and convert string representations to lists of integers
def clean_and_convert(value):
    if isinstance(value, str):
        # Remove brackets and split by commas or spaces
        value = value.strip('[]')
        value = value.replace(',', ' ').split()
        return [int(x) for x in value]
    elif isinstance(value, list):
        return value
    elif isinstance(value, np.ndarray):
        return value.tolist()
    elif value is None:
        return []
    else:
        # Handle other types if necessary
        return []

# Iterate over the DataFrame rows
for idx, row in df_mismatches.iterrows():
    # Clean and convert the predictions
    prediction_GPT = np.array(clean_and_convert(row['GPT_Predictions']))
    prediction_RTM = np.array(clean_and_convert(row['RTM_Predictions']))

    # Slice prediction_RTM if necessary (adjust indices as needed)
    # prediction_RTM = prediction_RTM[1:22]

    if not np.array_equal(prediction_GPT, prediction_RTM):
        print(idx, "differs:\n", prediction_GPT, '\n', prediction_RTM)
        mismatch_row = {
            'index': row['Index'],
            'vote_Name': row['vote_name'],
            'prediction_GPT': prediction_GPT.tolist(),
            'prediction_RTM': prediction_RTM.tolist(),
        }
        filtered_mismatches.append(mismatch_row)
    else:
        print(idx, "had equal predictions: ", prediction_GPT, "vs", prediction_RTM)

# Create a DataFrame from the filtered mismatches
df_filtered_mismatches = pd.DataFrame(filtered_mismatches)

# Write the DataFrame to a new table in the database
df_filtered_mismatches.to_sql(
    output_table_name,
    con=engine,
    if_exists='replace',
    index=False,
    dtype={
        'index': INTEGER,
        'vote_Name': sqlalchemy.types.Text(),
        'prediction_GPT': ARRAY(INTEGER),
        'prediction_RTM': ARRAY(INTEGER),
    }
)

print(f"Filtered mismatches saved to table '{output_table_name}' in the database.")
