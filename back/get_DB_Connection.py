from sqlalchemy import create_engine

db_username = 'test_user'
db_password = 'test_password'
db_host = 'localhost'
db_port = '5432'
db_name = 'test_db'

DATABASE_URI = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
