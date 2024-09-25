import pandas as pd
from sqlalchemy import create_engine
from back.get_DB_Connection import DATABASE_URI
# Initialize database connection
engine = create_engine(DATABASE_URI)

# List of your Excel files and corresponding table names
excel_files = [
    ('data/Test_DataWithLabels.xlsx', 'test_data_with_labels'),
    ('data/CorpusEtiquetado_Sampled.xlsx', 'corpus_etiquetado_sampled'),
    ('data/expanded_mismatches.xlsx', 'expanded_mismatches'),
    # Add other files as needed
]

for file_path, table_name in excel_files:
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Write to PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data from {file_path} has been written to the '{table_name}' table.")
