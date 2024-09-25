from sqlalchemy import create_engine

# Replace with your actual credentials
db_username = 'test_user'
db_password = 'test_password'
db_host = 'localhost'  # or your DB host
db_port = '5432'       # default PostgreSQL port
db_name = 'test_db'

DATABASE_URI = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
