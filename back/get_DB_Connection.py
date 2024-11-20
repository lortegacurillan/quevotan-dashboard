from sqlalchemy import create_engine

db_username = 'test_user'
db_password = 'chistecortopalquelee'
db_host = '172.24.252.23'
db_port = '5432'
db_name = 'postgres'

DATABASE_URI = f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'