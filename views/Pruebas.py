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

def show_pruebas(actualizar_dataframe):
    st.title("Consulta de Etiquetas")

    if st.button("Actualizar datos del dataframe"):
        data = actualizar_dataframe('Prueba')
    else:
        data = actualizar_dataframe('Prueba')

    if not data.empty:
        # Campo de entrada de número de filas a mostrar
        inicio_filas, fin_filas = st.slider("Número de filas a mostrar:", 1, len(data), (1,10))
        st.write("Datos de prueba")
        st.write("En esta sección puedes consultar y etiquetar votaciones de la Cámara de Diputados de Chile. Con la diferencia de que se mostraran solo los datos de prueba, es decir, sujerencias para probar el etiquetado del modelo, ya que estos datos no fueron revisados por el modelo al momento de entrenarse.")
        st.write("Señalando la cantidad necesaria que quiera mostrar a continuación.")
        with st.form(key='multiselect_form'):
            columnas = list(data.columns)
            columnas_seleccionadas = st.multiselect("Selecciona las columnas a mostrar:", columnas, default=columnas)
            submit_button = st.form_submit_button(label='Actualizar filtro')

        if 'first_load' not in st.session_state:
            st.session_state.first_load = True

        if submit_button or st.session_state.first_load or inicio_filas:
            st.write("aqui se mostrara el resultado de las columnas seleccionadas y la cantidad de filas que se le asigno. siendo las columnas las siguientes:")
            st.write("votaciones_Nombre:estos son los nombres de las votaciones que se realizaron en la camara de diputados.")
            st.write("Texto:Este es el conjunto total de las opiniones realizadas en la camara de diputados.")
            etiquetas = [
        "Seguridad y Defensa",
        "Relaciones Internacionales",
        "Energía y Medioambiente",
        "Justicia y Derechos Humanos",
        "Educación",
        "Políticas Sociales",
        "Deporte, Cultura y Salud",
        "Política Económica",
        "Política Interna",
        "Participación Ciudadana"
            ]
            st.write("Etiquetas seleccionadas: Estas son las etiquetas que se le asignaron a las votaciones realizadas en la camara de diputados. estas pueden ser:")
            st.markdown('\n'.join([f"{i+1}. {etiqueta}" for i, etiqueta in enumerate(etiquetas)]))
            st.write(f"Datos del dataframe (de la fila {inicio_filas} a la fila {fin_filas}):")
            st.write(data[columnas_seleccionadas].iloc[inicio_filas-1:fin_filas])
            st.session_state.first_load = False
    else:
        st.warning("No se pudo obtener el dataframe.")

    with st.form(key='etiquetado_form'):
        texto_a_etiquetar = st.text_input("Ingresa el texto a etiquetar:")
        st.write("Aqui podra ingresar un texto para ser etiquetado por nuestro modelo en donde se le mostrara el resultado de las etiquetas que se le asignaron. Siendo el 1 una aparicion de la etiqueta y el 0 una no aparicion de la etiqueta.")
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
