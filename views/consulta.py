import streamlit as st
import pandas as pd
from back.get_Query import get_QueryResponse

def mostrar_dataframe_responsivo(df):
    max_columns = 5
    num_columns = len(df.columns)

    if num_columns > max_columns:
        for i in range(0, num_columns, max_columns):
            subset_df = df.iloc[:, i:i + max_columns]
            st.dataframe(subset_df)
    else:
        st.dataframe(df)

def show_consulta(data,actualizar_dataframe):
    st.title("Consulta de Etiquetas")
    
    if st.button("Actualizar datos del dataframe"):
        data = actualizar_dataframe()
    else:
        data = actualizar_dataframe()

    if not data.empty:      
        # Campo de entrada de número de filas a mostrar
        num_filas = st.slider("Número de filas a mostrar:", 1, len(data), 10)
        with st.form(key='multiselect_form'):
            columnas = list(data.columns)
            columnas_seleccionadas = st.multiselect("Selecciona las columnas a mostrar:", columnas, default=columnas[11:23])
            submit_button = st.form_submit_button(label='Actualizar filtro')

        if 'first_load' not in st.session_state:
            st.session_state.first_load = True

        if submit_button or st.session_state.first_load or num_filas:
            st.write("Datos del dataframe:", data[columnas_seleccionadas].head(num_filas))
            st.session_state.first_load = False
    else:
        st.warning("No se pudo obtener el dataframe.")
    
    with st.form(key='etiquetado_form'):
        texto_a_etiquetar = st.text_input("Ingresa el texto a etiquetar:")
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            if texto_a_etiquetar:
                with st.spinner("Enviando texto al backend..."):
                    respuesta = get_QueryResponse(texto_a_etiquetar)
                    respuesta_df = pd.DataFrame(respuesta, columns=data.iloc[:, 13:23].columns)

                    columnas_con_uno = respuesta_df.loc[:, (respuesta_df == 1).iloc[0]]
                    respuesta_df_filtrada = respuesta_df[columnas_con_uno.columns]

                    st.write("Resultado del etiquetado:")
                    colums_query = st.multiselect("Resultados:", list(respuesta_df_filtrada.columns), default=list(respuesta_df_filtrada.columns), disabled=True)
                    mostrar_dataframe_responsivo(respuesta_df_filtrada)
                    mostrar_dataframe_responsivo(respuesta_df)
            else:
                st.write("Por favor, ingresa un texto.")
