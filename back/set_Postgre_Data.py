import pandas as pd
from sqlalchemy import create_engine
from get_DB_Connection import DATABASE_URI

# Initialize database connection
engine = create_engine(DATABASE_URI)

# Function to clean and expand the dataframe
def process_mismatches_file(file_path):
    # Load the Excel file, skipping the problematic empty rows and extra columns
    df = pd.read_excel(file_path)

    # Inspect the columns to understand which ones are relevant
    print(f"Columns in the file: {df.columns}")

    # Drop irrelevant columns and keep only the columns of interest
    # Assuming that the relevant columns are from column 4 onward
    df = df.iloc[:, 4:]  # Start from column 4 and beyond

    # Now rename the first four relevant columns to the names we expect
    df.columns = ['Index', 'vote_Name', 'GPT_predictions', 'RTM_predictions']

    # Define the labels (in the same order as the list predictions in the Excel file)
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Function to convert space-separated strings to proper lists
    def convert_to_list(prediction_string):
        # Convert space-separated strings into lists by inserting commas
        return [int(x) for x in prediction_string.strip("[]").split()]

    # Expand GPT_predictions (replace spaces with commas before applying eval)
    gpt_pred_df = pd.DataFrame(df['GPT_predictions'].apply(lambda x: pd.Series(convert_to_list(x))).values, columns=[f"{label}_GPT" for label in labels])

    # Expand RTM_predictions (replace spaces with commas before applying eval)
    rtm_pred_df = pd.DataFrame(df['RTM_predictions'].apply(lambda x: pd.Series(convert_to_list(x))).values, columns=[f"{label}_RTM" for label in labels])

    # Combine the original vote information with the expanded predictions
    expanded_df = pd.concat([df[['Index', 'vote_Name']], gpt_pred_df, rtm_pred_df], axis=1)

    return expanded_df

# List of Excel files and corresponding table names
excel_files = [
    ('data/Test_DataWithLabels.xlsx', 'test_data_with_labels'),
    ('data/CorpusEtiquetado_Sampled.xlsx', 'corpus_etiquetado_sampled'),
    ('data/expanded_mismatches.xlsx', 'expanded_mismatches'),
    ('data/mismatches.xlsx', 'gpt_rtm_comparison'),
    # Add other files as needed
]

for file_path, table_name in excel_files:
    # Handle the specific case for mismatches.xlsx
    if table_name == 'gpt_rtm_comparison':
        df = process_mismatches_file(file_path)
    else:
        # For other files, read and load as usual
        df = pd.read_excel(file_path)

    # Write to PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data from {file_path} has been written to the '{table_name}' table.")
