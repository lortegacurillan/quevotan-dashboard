import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, Column, String, BigInteger, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
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
session = Session()

# Función para obtener una votación aleatoria
def get_random_vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

# Función para guardar los datos usando ORM
def save_data_to_postgres(data_to_send: dict):
    try:
        new_entry = HumanLabels(
            vote_id=data_to_send['vote_index'],
            votaciones_nombre=data_to_send['votaciones_Nombre'],
            seguridad_y_defensa=data_to_send['Seguridad y Defensa'],
            relaciones_internacionales=data_to_send['Relaciones Internacionales'],
            energia_y_medioambiente=data_to_send['Energía y Medioambiente'],
            justicia_y_derechos_humanos=data_to_send['Justicia y Derechos Humanos'],
            educacion=data_to_send['Educación'],
            politicas_sociales=data_to_send['Políticas Sociales'],
            deporte_cultura_y_salud=data_to_send['Deporte, Cultura y Salud'],
            politica_economica=data_to_send['Política Económica'],
            politica_interna=data_to_send['Política Interna'],
            participacion_ciudadana=data_to_send['Participación Ciudadana'],
            timestamp=datetime.now()
        )
        session.add(new_entry)
        session.commit()
    except Exception as e:
        session.rollback()  # Reset session on failure
        raise e  # Raise the exception again for debugging/logging



# Función para cargar datos desde la base de datos
def get_Data(table_name: str = None) -> pd.DataFrame:
    if table_name is None:
        return None
    df = pd.read_sql_table(table_name, con=engine)
    return df

# Vista principal
def show_UserLabeling(data: pd.DataFrame):
    st.title("Etiquetado de Votaciones del Congreso")

    # Mostrar votación aleatoria
    vote =  data.iloc[get_random_vote(data)] #pd.series Series object <- []
    st.write("Lee el siguiente tema de votación y selecciona las etiquetas correspondientes.")
    st.markdown(f"## {vote['votaciones_Nombre']}")
    st.markdown(f"##### {vote['_id']}")
    # Definir etiquetas
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Formulario para selección de etiquetas
    selected_labels = {}
    with st.form(key='labeling_form'):
        st.write("Selecciona las etiquetas que correspondan:")
        for label in labels:
            selected_labels[label] = st.checkbox(label)
        submitted = st.form_submit_button("Enviar")

    # Al enviar el formulario
    if submitted:
        if any(selected_labels.values()):
            data_to_send = {
                'vote_index': vote['_id'],
                'votaciones_Nombre': vote['votaciones_Nombre'],
                'Seguridad y Defensa': int(selected_labels["Seguridad y Defensa"]),
                'Relaciones Internacionales': int(selected_labels["Relaciones Internacionales"]),
                'Energía y Medioambiente': int(selected_labels["Energía y Medioambiente"]),
                'Justicia y Derechos Humanos': int(selected_labels["Justicia y Derechos Humanos"]),
                'Educación': int(selected_labels["Educación"]),
                'Políticas Sociales': int(selected_labels["Políticas Sociales"]),
                'Deporte, Cultura y Salud': int(selected_labels["Deporte, Cultura y Salud"]),
                'Política Económica': int(selected_labels["Política Económica"]),
                'Política Interna': int(selected_labels["Política Interna"]),
                'Participación Ciudadana': int(selected_labels["Participación Ciudadana"]),
            }

            # Guardar datos en PostgreSQL
            save_data_to_postgres(data_to_send)

            st.success("¡Gracias por tu colaboración!")
        else:
            st.warning("Por favor, selecciona al menos una etiqueta.")

