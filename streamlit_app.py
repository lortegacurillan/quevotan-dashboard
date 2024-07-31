
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
    layout="wide",
    
)

# # CSS para ajustar el ancho de los elementos y mejorar la responsividad
# st.markdown("""
#     <style>
#         .main .block-container {
#             max-width: 100%;
#             padding: 1rem 2rem;
#         }
#         .css-1lcbmhc {
#             flex: 1;
#             display: flex;
#             flex-direction: column;
#             justify-content: center;
#             align-items: center;
#         }
#     </style>
# """, unsafe_allow_html=True)

def backend_obtener_dataframe():
    try:
        data= get_Data()
    except Exception as e:
        st.error(f"Error al obtener el dataframe: {e}")
    return data


data = backend_obtener_dataframe()

# Definir el menú vertical
st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Selecciona una vista:", ["About","Etiquetas", "Consulta"])

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

def mostrar_dataframe_responsivo(df, num_filas):
    max_columns = 5  # Número máximo de columnas para mostrar en una fila
    num_columns = len(df.columns)
    
    if num_columns > max_columns:
        for i in range(0, num_columns, max_columns):
            subset_df = df.iloc[:, i:i + max_columns]
            st.dataframe(subset_df.head(num_filas))
    else:
        st.dataframe(df.head(num_filas))

# Vista "Etiquetas"
# Vista "About"
if opcion == "About":
    st.title("Sobre Nosotros")

    # Introducción
    st.subheader("Introducción")
    st.write(
        """
        Bienvenido a la sección "About" de nuestro proyecto. Aquí te proporcionamos una visión general sobre nuestra 
        iniciativa, el equipo detrás del proyecto, y el objetivo de nuestra solución.
        """
    )

    # El Proyecto
    st.subheader("El Proyecto")

    st.write(
        """
        ### Descripción General
        Nuestro proyecto se centra en el desarrollo y entrenamiento de un modelo de aprendizaje automático utilizando Random Forest 
        para etiquetar las votaciones de la Cámara de Diputados de Chile. Utilizamos datos disponibles públicamente para construir 
        un modelo que categoriza las votaciones en varias áreas temáticas, lo cual proporciona una herramienta valiosa para el análisis 
        político y la transparencia gubernamental.
        
        ### Objetivos del Proyecto
        - **Etiquetado Automático de Votaciones**: Desarrollar un modelo que clasifique las votaciones de los diputados en distintas categorías temáticas.
        - **Transparencia y Análisis**: Ofrecer una herramienta que permita a los ciudadanos analizar el comportamiento de los diputados y evaluar su participación en diferentes áreas de política.
        - **Desarrollo Profesional**: Adquirir y aplicar habilidades en el ámbito del aprendizaje automático y la ciencia de datos.
        """
    )

    # Metodología
    st.subheader("Metodología")

    st.write(
        """
        ### 1. Adquisición y Preparación de Datos
        - **Obtención de Datos**: Utilizamos técnicas de web scraping para recolectar datos relevantes sobre las votaciones y las intervenciones de los diputados.
        - **Limpieza de Datos**: Aplicamos diversas técnicas para la limpieza de datos, incluyendo la eliminación de registros incompletos y la normalización del texto. Se utilizó preprocesamiento de texto como conversión a minúsculas y eliminación de caracteres especiales.
        
        ### 2. Procesamiento y Modelado
        - **Vectorización del Texto**: Se aplicó el método TF-IDF para transformar el texto en vectores numéricos, utilizando un conjunto de stop words en español para mejorar la relevancia de las características.
        - **Entrenamiento del Modelo**: El modelo Random Forest se entrenó para clasificar múltiples etiquetas simultáneamente utilizando `MultiOutputClassifier`. La división del dataset en conjuntos de entrenamiento y prueba, junto con técnicas de escalado, permitió un entrenamiento eficiente.
        - **Optimización de Hiperparámetros**: Se utilizó GridSearchCV para encontrar los mejores parámetros del modelo, mejorando así su precisión.
        
        ### 3. Evaluación
        - **Evaluación del Modelo**: Se evaluó el rendimiento del modelo utilizando métricas de precisión y matrices de confusión para cada etiqueta.
        - **Resultados**: El modelo mostró un buen rendimiento en la clasificación de las votaciones, y los resultados están disponibles para su análisis.
        """
    )

    # El Equipo
    st.subheader("El Equipo")

    st.write(
        """
        ### Miembros del Equipo
        - **Mario Castillo**: Encargado del flujo de tareas y coordinación del proyecto. Tiene un profundo conocimiento en el desarrollo de productos de aprendizaje automático. Encargado del ajuste de parámetros y optimización del modelo.
        - **Sebastian Garcia y Luis Ortega**: Especialistas en procesamiento de datos y preprocesamiento. Encargados de la limpieza y transformación de datos. Responsables de la implementación y evaluación del modelo. 
        
        ### Institución
        Este proyecto es desarrollado por un equipo de estudiantes de la Universidad Católica de Temuco, dentro de la carrera de Ingeniería Civil en Informática.
        """
    )

    # Impacto y Futuro
    st.subheader("Impacto y Futuro")

    st.write(
        """
        ### Impacto Esperado
        - **Transparencia Política**: Facilitará a los ciudadanos el análisis de las votaciones y el comportamiento de los diputados.
        - **Herramienta de Análisis**: Proveerá una herramienta útil para investigadores y analistas políticos.
        
        ### Futuro del Proyecto
        - **Ampliación del Modelo**: Incluir intervenciones de diputados en las votaciones para mejorar la precisión del modelo.
        - **Desarrollo de Nuevas Funcionalidades**: Implementar características adicionales para el análisis y visualización de datos.
        
        ### Objetivos Personales
        Como estudiantes de Ingeniería Civil en Informática, buscamos adquirir habilidades prácticas en el campo del aprendizaje automático, fortalecer nuestro conocimiento en la ciencia de datos y prepararnos para futuros desafíos profesionales.
        """
    )

    # Contacto
    st.subheader("Contacto")

    st.write(
        """
        Para más información sobre el proyecto o para colaborar con nosotros, no dudes en contactarnos:
        
        - **Email**: [tu-email@dominio.com]
        - **LinkedIn**: [Perfil de LinkedIn del equipo]
        - **GitHub**: [https://github.com/lortegacurillan/quevotan-dashboard]
        """
    )
elif opcion == "Etiquetas":
    st.title("Distribución de Etiquetas y Relaciones")
    
    # Actualizar datos de etiquetas
    if st.button("Actualizar datos de etiquetas"):
        etiquetas, cantidades = actualizar_datos_etiquetas()
    else:
        etiquetas, cantidades = get_LabelCount(data)
    

    # Crear gráfico de barras
    st.subheader("Distribución de Etiquetas")
        
    #Grafico de barra del arreglo etiqueta y cantidades 

    fig = get_LabelCountGraph(etiquetas, cantidades)
    
    st.subheader("Número de Etiquetas por Texto")

    fig3 = get_CountGraph(data.iloc[:, 13:23])

    st.subheader("Combinaciones de Etiquetas")
        
    fig2 = get_CombinationGraph(data.iloc[:, 13:23])

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
        # Formulario para evitar recarga constante del multiselect
        with st.form(key='multiselect_form'):
            # # Campo de entrada de número de filas a mostrar
            # num_filas = st.slider("Número de filas a mostrar:", 1, len(data), 10)
            columnas = list(data.columns)
            columnas_seleccionadas = st.multiselect("Selecciona las columnas a mostrar:", columnas, default=columnas[11:23])
            submit_button = st.form_submit_button(label='Actualizar filtro')
        
        if 'first_load' not in st.session_state:
            st.session_state.first_load = True

        # Mostrar el DataFrame en la primera carga o cuando se presiona el botón del formulario
        if submit_button or st.session_state.first_load or num_filas: #!= st.session_state.num_filas:
            st.write("Datos del dataframe:", data[columnas_seleccionadas].head(num_filas))
            st.session_state.first_load = False
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
                    # Convertir ndarray a DataFrame
                    respuesta_df = pd.DataFrame(respuesta, columns=data.iloc[:, 13:23].columns)
                    
                    # Mostrar respuesta como tabla
                   # Mostrar respuesta como tabla
                    st.write("Resultado del etiquetado:")
                    mostrar_dataframe_responsivo(respuesta_df, num_filas=1)
            else:
                st.write("Por favor, ingresa un texto.")
