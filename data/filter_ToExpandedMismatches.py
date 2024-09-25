import os
import pandas as pd
from sqlalchemy import create_engine
from back.get_DB_Connection import DATABASE_URI

# Initialize database connection
engine = create_engine(DATABASE_URI)

# Define the input and output table names
input_table_name = 'filtered_mismatches'
output_table_name = 'expanded_mismatches'

# Load the mismatches DataFrame from the database table
df_mismatches = pd.read_sql_table(input_table_name, con=engine)
print(df_mismatches.columns)

# List of labels
labels = ["Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
          "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
          "Deporte, Cultura y Salud", "Política Económica", "Política Interna",
          "Participación Ciudadana"]

# Create columns for GPT and RTM predictions
gpt_columns = [f"GPT_{label}" for label in labels]
rtm_columns = [f"RTM_{label}" for label in labels]

# Function to clean and convert string lists into actual lists of integers
def clean_and_convert(value):
    if isinstance(value, str):
        # Remove brackets and split by commas or spaces
        value = value.strip('[]')
        value = value.replace(',', ' ').split()
        return [int(x) for x in value]
    elif isinstance(value, list):
        return value
    return []

# Apply the cleaning and conversion function to each prediction
df_mismatches['prediction_GPT'] = df_mismatches['prediction_GPT'].apply(clean_and_convert)
df_mismatches['prediction_RTM'] = df_mismatches['prediction_RTM'].apply(clean_and_convert)

# Expand the 'prediction_GPT' and 'prediction_RTM' into separate columns
gpt_df = pd.DataFrame(df_mismatches['prediction_GPT'].to_list(), columns=gpt_columns)
rtm_df = pd.DataFrame(df_mismatches['prediction_RTM'].to_list(), columns=rtm_columns)

# Concatenate the 'index', 'vote_Name', GPT predictions, and RTM predictions into a single DataFrame
final_df = pd.concat([df_mismatches[['index', 'vote_Name']], gpt_df, rtm_df], axis=1)

# Write the resulting DataFrame to a new table in the database
final_df.to_sql(output_table_name, con=engine, if_exists='replace', index=False)
print(f"Transformed data saved to table '{output_table_name}' in the database.")
