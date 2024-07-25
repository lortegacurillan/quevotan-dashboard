import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='¿Que Votan? dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

# @st.cache_data
# def get_gdp_data():
#     """Grab GDP data from a CSV file.

#     This uses caching to avoid having to read the file every time. If we were
#     reading from an HTTP endpoint instead of a file, it's a good idea to set
#     a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
#     """
#     return gdp_df

# gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page
# Backend simulado
def backend_obtener_datos_etiquetas():
    """
    Simula la obtención de datos de etiquetas desde el backend.
    
    Returns:
        tuple: Una tupla con una lista de etiquetas (list) y una lista de cantidades (list).
    """
    etiquetas = ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3']
    cantidades = [50, 30, 20]
    return etiquetas, cantidades

def backend_obtener_dataframe():
    """
    Simula la obtención de un dataframe desde el backend.
    
    Returns:
        pd.DataFrame: Un dataframe con datos de texto y sus etiquetas.
    """
    data = pd.DataFrame({
        'Texto': ['Texto 1', 'Texto 2', 'Texto 3', 'Texto 4', 'Texto 5', 'Texto 6', 'Texto 7', 'Texto 8', 'Texto 9', 'Texto 10','Texto 11', 'Texto 12', 'Texto 13', 'Texto 14', 'Texto 15', 'Texto 16', 'Texto 17', 'Texto 18', 'Texto 19', 'Texto 20'],
        'Etiqueta': ['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3', 'Etiqueta 1', 'Etiqueta 2']
    })
    return data

def backend_etiquetar_texto(texto):
    """
    Simula el envío de un texto al backend para ser etiquetado y recibir una respuesta.
    
    Args:
        texto (str): El texto que se desea etiquetar.
    
    Returns:
        str: La respuesta del backend con el texto etiquetado.
    """
    respuesta = f"Texto etiquetado recibido: {texto}"
    return respuesta

# Funciones de interacción con el backend
@st.cache_data(ttl=600)
def obtener_datos_etiquetas():
    """
    Función que interactúa con el backend para obtener datos de etiquetas.
    
    Returns:
        tuple: Una tupla con una lista de etiquetas (list) y una lista de cantidades (list).
    """
    try:
        return backend_obtener_datos_etiquetas()
    except Exception as e:
        st.error(f"Error al obtener datos de etiquetas: {e}")
        return [], []

@st.cache_data(ttl=600)
def obtener_dataframe():
    """
    Función que interactúa con el backend para obtener un dataframe.
    
    Returns:
        pd.DataFrame: Un dataframe con datos de texto y sus etiquetas.
    """
    try:
        return backend_obtener_dataframe()
    except Exception as e:
        st.error(f"Error al obtener el dataframe: {e}")
        return pd.DataFrame()

def enviar_texto_al_backend(texto):
    """
    Función que interactúa con el backend para enviar un texto y recibir una etiqueta.
    
    Args:
        texto (str): El texto que se desea etiquetar.
    
    Returns:
        str: La respuesta del backend con el texto etiquetado.
    """
    try:
        return backend_etiquetar_texto(texto)
    except Exception as e:
        st.error(f"Error al enviar el texto al backend: {e}")
        return "Error en el etiquetado"

# Definir el menú vertical
st.sidebar.title("Menú")
opcion = st.sidebar.radio("Selecciona una vista:", ["Etiquetas", "Consulta"])

# Función para actualizar datos de etiquetas
def actualizar_datos_etiquetas():
    st.cache_data.clear()
    etiquetas, cantidades = obtener_datos_etiquetas()
    return etiquetas, cantidades

# Función para actualizar dataframe
def actualizar_dataframe():
    st.cache_data.clear()
    data = obtener_dataframe()
    return data

# Vista "Etiquetas"
if opcion == "Etiquetas":
    st.title("Distribución de Etiquetas")
    
    if st.button("Actualizar datos de etiquetas"):
        etiquetas, cantidades = actualizar_datos_etiquetas()
    else:
        etiquetas, cantidades = obtener_datos_etiquetas()
    
    if etiquetas and cantidades:
        # Crear gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(cantidades, labels=etiquetas, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Asegura que el gráfico de torta sea circular
        
        # Mostrar gráfico de torta
        st.pyplot(fig)
    else:
        st.warning("No se pudieron obtener los datos de etiquetas.")

# Vista "Consulta"
elif opcion == "Consulta":
    st.title("Consulta de Etiquetas")
    
    if st.button("Actualizar datos del dataframe"):
        data = actualizar_dataframe()
    else:
        data = obtener_dataframe()
    
    if not data.empty:
        # Campo de entrada de número de filas a mostrar
        num_filas = st.slider("Número de filas a mostrar:", 1, len(data), 10)
        # Mostrar dataframe con el número de filas seleccionado
        st.write("Datos del dataframe:", data.head(num_filas))
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
                    respuesta = enviar_texto_al_backend(texto_a_etiquetar)
                    # Mostrar respuesta
                    st.write("Respuesta del backend:", respuesta)
            else:
                st.write("Por favor, ingresa un texto.")