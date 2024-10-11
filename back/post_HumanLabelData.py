from sqlalchemy import create_engine, Column, String, BigInteger, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from back.get_DB_Connection import DATABASE_URI

# Conexión a la base de datos
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Definir el modelo de la tabla human_labels
class HumanLabels(Base):
    __tablename__ = 'human_labels'
    
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    vote_id = Column(String, nullable=False)
    votaciones_nombre = Column("votaciones_Nombre", String)
    seguridad_y_defensa = Column("Seguridad y Defensa", BigInteger)
    relaciones_internacionales = Column("Relaciones Internacionales", BigInteger)
    energia_y_medioambiente = Column("Energía y Medioambiente", BigInteger)
    justicia_y_derechos_humanos = Column("Justicia y Derechos Humanos", BigInteger)
    educacion = Column("Educación", BigInteger)
    politicas_sociales = Column("Políticas Sociales", BigInteger)
    deporte_cultura_y_salud = Column("Deporte, Cultura y Salud", BigInteger)
    politica_economica = Column("Política Económica", BigInteger)
    politica_interna = Column("Política Interna", BigInteger)
    participacion_ciudadana = Column("Participación Ciudadana", BigInteger)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Crear las tablas si no existen
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)

def save_Data_To_Postgres(data_To_Send: dict):
    """Función para guardar los datos usando ORM"""
    session = Session()
    try:
        new_entry = HumanLabels(
            vote_id=data_To_Send['vote_index'],
            votaciones_nombre=data_To_Send['votaciones_Nombre'],
            seguridad_y_defensa=data_To_Send['Seguridad y Defensa'],
            relaciones_internacionales=data_To_Send['Relaciones Internacionales'],
            energia_y_medioambiente=data_To_Send['Energía y Medioambiente'],
            justicia_y_derechos_humanos=data_To_Send['Justicia y Derechos Humanos'],
            educacion=data_To_Send['Educación'],
            politicas_sociales=data_To_Send['Políticas Sociales'],
            deporte_cultura_y_salud=data_To_Send['Deporte, Cultura y Salud'],
            politica_economica=data_To_Send['Política Económica'],
            politica_interna=data_To_Send['Política Interna'],
            participacion_ciudadana=data_To_Send['Participación Ciudadana'],
            timestamp=datetime.now()
        )
        session.add(new_entry)
        session.commit()
    except Exception as e:
        session.rollback()  # Reset session on failure
        raise e
    finally:
        session.close()
