from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from back.get_DB_Connection import DATABASE_URI

# Conexión a la base de datos
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Definir el modelo de la tabla user_model_ranking
class UserModelRanking(Base):
    __tablename__ = 'user_model_ranking'
    
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    vote_index = Column(Integer, nullable=False)  # New column for vote index
    vote_name = Column(String, nullable=False)
    chosen_model = Column(Integer, nullable=False)  # Now stores 0 (GPT) or 1 (RTM)
    user_comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)

def save_UserModelRanking_To_Postgres(data_To_Send: dict):
    """Función para guardar los datos del UserModelRanking usando ORM"""
    session = Session()
    try:
        # Creating a new entry
        new_entry = UserModelRanking(
            vote_index=data_To_Send['vote_index'],  # Include vote index
            vote_name=data_To_Send['vote_name'],
            chosen_model=data_To_Send['chosen_model'],  # Store 0 for Model 1 (GPT) and 1 for Model 2 (RTM)
            user_comment=data_To_Send['user_comment'],
            timestamp=datetime.now()
        )
        session.add(new_entry)
        session.commit()
    except Exception as e:
        session.rollback()  # Reset session on failure
        raise e
    finally:
        session.close()
