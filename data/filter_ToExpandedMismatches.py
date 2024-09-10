import os
import pandas as pd

# Define the path to the mismatches file
input_file_path = os.path.join('./data/', 'filtered_mismatches.xlsx')
output_file_path = os.path.join('./data/', 'expanded_mismatches.xlsx')

# Load the mismatches DataFrame from the Excel file
df_mismatches = pd.read_excel(input_file_path)
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
        # Remove spaces and brackets, then split by space
        value = value.replace("[", "").replace("]", "").split()
        return [int(x) for x in value]  # Convert the cleaned-up string into a list of integers
    return value  # If it's already a list, return as is

# Apply the cleaning and conversion function to each prediction
df_mismatches['prediction_GPT'] = df_mismatches['prediction_GPT'].apply(clean_and_convert)
df_mismatches['prediction_RTM'] = df_mismatches['prediction_RTM'].apply(clean_and_convert)

# Expand the 'prediction_GPT' and 'prediction_RTM' into separate columns
gpt_df = pd.DataFrame(df_mismatches['prediction_GPT'].to_list(), columns=gpt_columns)
rtm_df = pd.DataFrame(df_mismatches['prediction_RTM'].to_list(), columns=rtm_columns)

# Concatenate the 'Index', 'vote_name', GPT predictions, and RTM predictions into a single DataFrame
final_df = pd.concat([df_mismatches[['index', 'vote_Name']], gpt_df, rtm_df], axis=1)

# Save the resulting DataFrame to an Excel file
final_df.to_excel(output_file_path, index=False)

print(f"Transformed data saved to '{output_file_path}'")
