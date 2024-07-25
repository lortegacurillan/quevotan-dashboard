import streamlit as st
from back.get_Data import get_Data
from back.get_Graph import get_CombinationGraph, get_CountGraph
from back.get_LabelCount import get_LabelCount


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
    etiquetas, cantidades = get_LabelCount()
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
        etiquetas, cantidades = get_LabelCount()
    
    if etiquetas and cantidades:
        # Crear gráfico de barras
        st.subheader("Distribución de Etiquetas (Barras)")
        
        # Ordenar datos por cantidad
        sorted_indices = sorted(range(len(cantidades)), key=lambda i: cantidades[i], reverse=True)
        etiquetas_sorted = [etiquetas[i] for i in sorted_indices]
        cantidades_sorted = [cantidades[i] for i in sorted_indices]
        
        # Mostrar gráfico de barras con Streamlit
        st.bar_chart(pd.DataFrame({
            'Etiqueta': etiquetas_sorted,
            'Cantidad': cantidades_sorted
        }).set_index('Etiqueta'))
        
        # Crear gráfico de combinaciones de etiquetas
        st.subheader("Combinaciones de Etiquetas")
        
        # Obtener y procesar el DataFrame
        data = backend_obtener_dataframe()
        
        if not data.empty:
            # Contar combinaciones de etiquetas
            data_comb = data[['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3']].astype(str).agg('-'.join, axis=1)
            combinaciones = data_comb.value_counts()
            fig = get_CombinationGraph(combinaciones)
            st.pyplot(fig)
            
            # Crear gráfico de dispersión
            st.subheader("Número de Etiquetas por Texto")
            
            # Contar el número de etiquetas por texto
            num_etiquetas = data[['Etiqueta 1', 'Etiqueta 2', 'Etiqueta 3']].sum(axis=1)
            
            fig = get_CountGraph(data,num_etiquetas)
           
            st.pyplot(fig)
        else:
            st.warning("No se pudo obtener el dataframe.")
    else:
        st.warning("No se pudieron obtener los datos de etiquetas.")

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
                    respuesta = enviar_texto_al_backend(texto_a_etiquetar)
                    # Mostrar respuesta
                    st.write("Respuesta del backend:", respuesta)
            else:
                st.write("Por favor, ingresa un texto.")