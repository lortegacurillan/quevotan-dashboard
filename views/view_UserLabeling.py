import pandas as pd
import streamlit as st
import random
from back.post_Pg_Data import save_Data_To_Postgres

# Función para obtener una votación aleatoria
def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

# Vista principal
def show_UserLabeling(data: pd.DataFrame):
    st.title("Etiquetado de Votaciones del Congreso")

    # Mostrar votación aleatoria
    vote =  data.iloc[get_Random_Vote(data)] #pd.series Series object <- []
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
    selected_Labels = {}
    with st.form(key='labeling_form'):
        st.write("Selecciona las etiquetas que correspondan:")
        for label in labels:
            selected_Labels[label] = st.checkbox(label)
        submitted = st.form_submit_button("Enviar")

    # Al enviar el formulario
    if submitted:
        if any(selected_Labels.values()):
            data_to_send = {
                'vote_index': vote['_id'],
                'votaciones_Nombre': vote['votaciones_Nombre'],
                'Seguridad y Defensa': int(selected_Labels["Seguridad y Defensa"]),
                'Relaciones Internacionales': int(selected_Labels["Relaciones Internacionales"]),
                'Energía y Medioambiente': int(selected_Labels["Energía y Medioambiente"]),
                'Justicia y Derechos Humanos': int(selected_Labels["Justicia y Derechos Humanos"]),
                'Educación': int(selected_Labels["Educación"]),
                'Políticas Sociales': int(selected_Labels["Políticas Sociales"]),
                'Deporte, Cultura y Salud': int(selected_Labels["Deporte, Cultura y Salud"]),
                'Política Económica': int(selected_Labels["Política Económica"]),
                'Política Interna': int(selected_Labels["Política Interna"]),
                'Participación Ciudadana': int(selected_Labels["Participación Ciudadana"]),
            }

            # Guardar datos en PostgreSQL
            save_Data_To_Postgres(data_to_send)

            st.success("¡Gracias por tu colaboración!")
        else:
            st.warning("Por favor, selecciona al menos una etiqueta.")

