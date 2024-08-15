import sys
import os
import streamlit as st
import pandas as pd
from back.get_Data import get_Data
from utils.theme import set_color_scheme
# from back.get_LabelCount import get_LabelCount
# from back.get_Query import get_QueryResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar vistas
from views.about import show_about
from views.etiquetas import show_etiquetas
from views.consulta import show_consulta
from views.Pruebas import show_pruebas


st.set_page_config(
    page_title='¿Que Votan? dashboard',
    page_icon=':earth_americas:', 
    layout="wide",
)

# CSS para ajustar el ancho de los elementos y mejorar la responsividad
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding: 1rem 2rem;
        }
        .css-1lcbmhc {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

def backend_obtener_dataframe(what)-> pd.DataFrame:
    try:
        data = get_Data(what)
    except Exception as e:
        st.error(f"Error al obtener el dataframe: {e}")
    return data

data = backend_obtener_dataframe('sampled')

# Definir el menú vertical
st.sidebar.image("src/quevotan.jpg", use_column_width=True)
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una vista:", ["About", "Etiquetas", "Consulta","Pruebas"])

# Mostrar la vista seleccionada
if opcion == "About":
    show_about()
elif opcion == "Etiquetas":
    show_etiquetas(data)
elif opcion == "Consulta":
    show_consulta(data,backend_obtener_dataframe)
elif opcion == "Pruebas":
    show_pruebas(backend_obtener_dataframe)

# Selección del esquema de colores
color_scheme = st.sidebar.selectbox("Selecciona el esquema de colores:", ["dark", "white", "lightgrey", "lightblue", "lightgreen"])
set_color_scheme(color_scheme)