import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from back.get_DB_Connection import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import pandas as pd

def get_Data(table_name: str = None) -> pd.DataFrame:
    '''
    Fetch data from the PostgreSQL database.

    Parameters:
    table_name (str): The name of the table to fetch data from.

    Returns:
    pd.DataFrame: The DataFrame with data from the specified table.
    '''
    if table_name is None:
        return None

    # Initialize database connection
    engine = create_engine(
        DATABASE_URI,
        poolclass=QueuePool,
        pool_size=20,           # Base number of connections
        max_overflow=10,        # Additional connections allowed
        pool_timeout=30,        # Seconds to wait for available connection
        pool_pre_ping=True      # Check connection validity before use
    )

    # Read data from the table
    df = pd.read_sql_table(table_name, con=engine)
    return df
