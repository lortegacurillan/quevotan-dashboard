import pandas as pd
import streamlit as st
from back.get_Query import get_QueryResponse, search_votacion
from .view_UniqueQuery import get_ResponsiveDataframe
from .view_About import label_selection_form

def show_TestData(update_Dataframe):
    st.title("Consulta de Etiquetas")

    if st.button("Actualizar datos del dataframe"):
        data = update_Dataframe('test_data_with_labels')
    else:
        data = update_Dataframe('test_data_with_labels')

    if not data.empty:
        inicio_filas, fin_filas = st.slider("Número de filas a mostrar:", 1, len(data), (1, 10))

        with st.form(key='multiselect_form'):
            columnas = list(data.columns)
            columnas_seleccionadas = st.multiselect("Selecciona las columnas a mostrar:", columnas, default=columnas)
            submit_button = st.form_submit_button(label='Actualizar filtro')

        if submit_button or inicio_filas:
            st.write(f"Datos del dataframe (de la fila {inicio_filas} a la fila {fin_filas}):")
            st.write(data[columnas_seleccionadas].iloc[inicio_filas-1:fin_filas])

    else:
        st.warning("No se pudo obtener el dataframe.")

    etiquetas = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Call the refactored function for label selection using multiselect
    vote = {"_id": "dummy_id", "votaciones_Nombre": "Dummy Vote Name"}  # Replace with actual vote data
    data_to_send = label_selection_form(etiquetas, vote, form_key="test_data_form")

    if data_to_send:
        st.write("Etiquetas seleccionadas y enviadas:")
        st.json(data_to_send)
