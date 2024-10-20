import streamlit as st
import time

def typewriter_Effect(containers, texts, delay=0.01):
    '''function to simulate the typing effect on multiple containers in parallel.

    Parameters:
        containers (list): List of Streamlit containers to write to.
        texts (list): List of texts to display.
        delay (float, optional): Delay between each character. Defaults to 0.01.

    Returns:
        None
    '''
    texts = [list(text) for text in texts]
    lengths = [len(text) for text in texts]
    max_length = max(lengths)
    
    current_texts = ['' * len(text) for text in texts]

    for i in range(max_length):
        for j, (container, text) in enumerate(zip(containers, texts)):
            if i < len(text):
                current_texts[j] += text[i]
                container.markdown(current_texts[j], unsafe_allow_html=True)
        
        time.sleep(delay)

    st.write()

def show_About():
    '''
    Function to display the About Us page.

    Returns:
        None
    '''
    if 'animation_shown' not in st.session_state:
        st.session_state.animation_shown = False

    st.title("Sobre Nosotros")

    # Introducción
    with st.container():
        st.subheader("Introducción")
        intro_text = """
            Aquí te proporcionamos una visión general sobre nuestra 
            iniciativa, el equipo detrás del proyecto, y el objetivo de nuestra solución.
        """
        intro_container = st.empty()

    # El Proyecto
    with st.container():
        st.subheader("El Proyecto")
        col1, col2 = st.columns([3, 1])
        with col1:
            project_text = """
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
            project_container = st.empty()

        with col2:
            st.image("src/proyecto.jpg", use_column_width=True)
        
    # Metodología
    with st.container():
        st.subheader("Metodología")
        methodology_text = """
            ### 1. Adquisición y Preparación de Datos
            - **Obtención de Datos**: Utilizamos técnicas de web scraping para recolectar datos relevantes sobre las votaciones y las intervenciones de los diputados.
            - **Limpieza de Datos**: Aplicamos diversas técnicas para la limpieza de datos, incluyendo la eliminación de registros incompletos y la normalización del texto.
            
            ### 2. Procesamiento y Modelado
            - **Vectorización del Texto**: Se aplicó el método TF-IDF para transformar el texto en vectores numéricos.
            - **Entrenamiento del Modelo**: El modelo Random Forest se entrenó para clasificar múltiples etiquetas simultáneamente.
            - **Optimización de Hiperparámetros**: Se utilizó GridSearchCV para encontrar los mejores parámetros del modelo.
            
            ### 3. Evaluación
            - **Evaluación del Modelo**: Se evaluó el rendimiento del modelo utilizando métricas de precisión y matrices de confusión para cada etiqueta.
            - **Resultados**: El modelo mostró un buen rendimiento en la clasificación de las votaciones.
        """
        methodology_container = st.empty()

    # El Equipo
    with st.container():
        st.subheader("El Equipo")
        team_text = """
            ### Miembros del Equipo
            - **Mario Castillo**: Encargado del flujo de tareas y coordinación del proyecto.
            - **Sebastian Garcia y Luis Ortega**: Especialistas en procesamiento de datos y preprocesamiento.
            
            ### Institución
            Este proyecto es desarrollado por un equipo de estudiantes de la Universidad Católica de Temuco, dentro de la carrera de Ingeniería Civil en Informática.
        """
        team_container = st.empty()
        
        st.image("src/U.jpg", use_column_width=False)
    
    # Impacto y Futuro
    with st.container():
        st.subheader("Impacto y Futuro")
        impact_text = """
            ### Impacto Esperado
            - **Transparencia Política**: Facilitará a los ciudadanos el análisis de las votaciones y el comportamiento de los diputados.
            - **Herramienta de Análisis**: Proveerá una herramienta útil para investigadores y analistas políticos.
            
            ### Futuro del Proyecto
            - **Ampliación del Modelo**: Incluir intervenciones de diputados en las votaciones para mejorar la precisión del modelo.
            - **Desarrollo de Nuevas Funcionalidades**: Implementar características adicionales para el análisis y visualización de datos.
        """
        impact_container = st.empty()
        
        st.image("src/futuro.jpg", use_column_width=True)
    
    # Contacto
    with st.container():
        st.subheader("Contacto")
        contact_text = """
            Para más información sobre el proyecto o para colaborar con nosotros, no dudes en contactarnos:
            - **Email**: [mario.castillo2019@alu.uct.cl, sebastian.garcia2019@alu.uct.cl, lortega2020@alu.uct.cl]
            - **GitHub**: [https://github.com/lortegacurillan/quevotan-dashboard]
        """
        contact_container = st.empty()

    if not st.session_state.animation_shown:
        st.session_state.animation_shown = True
        typewriter_Effect(
            containers=[intro_container, project_container, methodology_container, team_container, impact_container, contact_container],
            texts=[intro_text, project_text, methodology_text, team_text, impact_text, contact_text],
            delay=0.02
        )
    else:
        # Mostrar el texto completo si la animación ya se ha mostrado
        for container, text in zip(
            [intro_container, project_container, methodology_container, team_container, impact_container, contact_container],
            [intro_text, project_text, methodology_text, team_text, impact_text, contact_text]
        ):
            container.markdown(text, unsafe_allow_html=True)

def label_selection_form(labels, vote, form_key, form_submit_label="Enviar"):
    """
    Function to handle the label selection form in a reusable way using a multiselect input.

    Parameters:
        labels (list): List of label options for the form.
        vote (dict): The current vote data, including 'votaciones_Nombre' and '_id'.
        form_key (str): A unique key for the form.
        form_submit_label (str): The label for the submit button. Default is "Enviar".

    Returns:
        dict or None: Returns a dictionary of selected labels mapped to 1/0, or None if not submitted.
    """
    with st.form(key=form_key):
        st.write("Selecciona las etiquetas que correspondan:")
        selected_labels = st.multiselect(
            "Selecciona las etiquetas:",
            options=labels,
            default=[],  # No preselected labels
            key=f"{form_key}_multiselect"
        )

        submitted = st.form_submit_button(form_submit_label)

        if submitted:
            if selected_labels:
                # Convert multiselect result to a dictionary format with 1/0
                selected_dict = {label: int(label in selected_labels) for label in labels}
                
                # Prepare the final data to send based on the selected labels
                data_to_send = {
                    'vote_index': vote['_id'],
                    'votaciones_Nombre': vote['votaciones_Nombre'],
                    **selected_dict
                }
                return data_to_send
            else:
                st.warning("Por favor, selecciona al menos una etiqueta.")
                return None

    return None
