import pandas as pd
from sqlalchemy import create_engine
from get_DB_Connection import DATABASE_URI

# Initialize database connection
engine = create_engine(DATABASE_URI)

# Define input and output table names
input_table_name = 'expanded_mismatches'
output_table_name = 'vote_ranking_softmax'

# Load the input DataFrame from the 'corpus_etiquetado_sampled' table in PostgreSQL
df_corpus = pd.read_sql_table(input_table_name, con=engine)

# Select only the necessary columns
# Assuming the 'corpus_etiquetado_sampled' table has 'vote_name' and 'index' columns
df_softmax = df_corpus[['index', 'vote_Name']].copy()

# Rename columns to match the `vote_ranking_softmax` table schema
df_softmax.rename(columns={'index': 'vote_index', 'vote_name': 'vote_name'}, inplace=True)

# Initialize appearance_count to 0
df_softmax['appearance_count'] = 0

# Write the resulting DataFrame to the new table in the database
df_softmax.to_sql(output_table_name, con=engine, if_exists='replace', index=False)
print(f"Softmax initialization data saved to table '{output_table_name}' in the database.")
