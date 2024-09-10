import sys
import os
import streamlit as st
import pandas as pd
from back.get_Data import get_Data, get_Mismatches
from utils.theme import set_color_scheme
# from back.get_LabelCount import get_LabelCount
# from back.get_Query import get_QueryResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar vistas
from views.view_About import show_About
from views.view_LabelsMetrics import show_Labels
from views.view_UniqueQuery import get_UniqueQuery
from views.view_TestData import show_TestData
from views.unicos import show_mismatches

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

data = get_Data('sampled')
mismatch_Data = get_Mismatches()

# Definir el menú vertical
st.sidebar.image("src/quevotan.jpg", use_column_width=True)
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una vista:", ["About", "Etiquetas", "Consulta","Pruebas","Mismatches"])

# Mostrar la vista seleccionada
if opcion == "About":
    show_About()
elif opcion == "Etiquetas":
    show_Labels(data)
elif opcion == "Consulta":
    get_UniqueQuery(data,get_Data)
elif opcion == "Pruebas":
    show_TestData(get_Data)
elif opcion == "Mismatches":
    show_mismatches(data,mismatch_Data)


