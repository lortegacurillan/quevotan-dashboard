
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from back.get_Data import get_Data
from back.get_Graph import get_CombinationGraph, get_CountGraph, get_LabelCountGraph
from back.get_LabelCount import get_LabelCount
from back.get_Query import get_QueryResponse


st.set_page_config(
    page_title='¿Que Votan? dashboard',
    page_icon=':earth_americas:', 
)

def backend_obtener_dataframe():
    try:
        data= get_Data()
    except Exception as e:
        st.error(f"Error al obtener el dataframe: {e}")
    return data


data = backend_obtener_dataframe()

# Definir el menú vertical
st.sidebar.title("Menú")
opcion = st.sidebar.radio("Selecciona una vista:", ["Etiquetas", "Consulta"])

# Función para actualizar datos de etiquetas
def actualizar_datos_etiquetas():
    st.cache_data.clear()
    etiquetas, cantidades = get_LabelCount(data)
    return etiquetas, cantidades

# Función para actualizar dataframe
def actualizar_dataframe():
    st.cache_data.clear()
    data = backend_obtener_dataframe()
    return data

# Vista "Etiquetas"
if opcion == "Etiquetas":
    st.title("Distribución de Etiquetas y Relaciones")
    
    # Actualizar datos de etiquetas
    if st.button("Actualizar datos de etiquetas"):
        etiquetas, cantidades = actualizar_datos_etiquetas()
    else:
        etiquetas, cantidades = get_LabelCount(data)
    

    # Crear gráfico de barras
    st.subheader("Distribución de Etiquetas")
        
     #Grafico de barra  del arreglo etiqueta y cantidades 

    fig = get_LabelCountGraph(etiquetas, cantidades)
    
    st.subheader("Combinaciones de Etiquetas")
    
    fig2 = get_CombinationGraph(data.iloc[:, 13:23])

    st.subheader("Número de Etiquetas por Texto")

    fig3 = get_CountGraph(data.iloc[:, 13:23])

# Vista "Consulta"
elif opcion == "Consulta":
    st.title("Consulta de Etiquetas")
    
    if st.button("Actualizar datos del dataframe"):
        data = actualizar_dataframe()
    else:
        data = backend_obtener_dataframe()
    
    if not data.empty:
        # Campo de entrada de número de filas a mostrar
        num_filas = st.slider("Número de filas a mostrar:", 1, len(data), 10)
        
        # Obtener nombres de columnas y seleccionar columnas a mostrar
        columnas = list(data.columns)
        columnas_seleccionadas = st.multiselect("Selecciona las columnas a mostrar:", columnas, default=columnas[:4])
        
        # Mostrar dataframe con las columnas y el número de filas seleccionados
        st.write("Datos del dataframe:", data[columnas_seleccionadas].head(num_filas))
    else:
        st.warning("No se pudo obtener el dataframe.")
    
    # Campo de entrada de texto
    with st.form(key='etiquetado_form'):
        texto_a_etiquetar = st.text_input("Ingresa el texto a etiquetar:")
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            if texto_a_etiquetar:
                with st.spinner("Enviando texto al backend..."):
                    # Enviar texto al backend y recibir respuesta
                    respuesta = get_QueryResponse(texto_a_etiquetar)
                    st.write(texto_a_etiquetar)
                    # Convertir ndarray a DataFrame
                    #respuesta_df = pd.DataFrame(respuesta, columns=data.iloc[:, 13:23].columns)
                    
                    # Mostrar respuesta como tabla
                    st.write("Respuesta del backend:")
                    st.dataframe(respuesta)
            else:
                st.write("Por favor, ingresa un texto.")
