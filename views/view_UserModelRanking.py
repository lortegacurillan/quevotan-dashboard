import pandas as pd
import numpy as np
import streamlit as st
import random
import time
from datetime import datetime, timedelta
from back.post_RankingData import save_UserModelRanking_To_Postgres
import base64
import os

def get_Softmax_Vote(data: pd.DataFrame) -> int:
    inverted_occurrences = data['appearance_count'].max() - data['appearance_count']
    exp_occurrences = np.exp(inverted_occurrences)
    probabilities = exp_occurrences / exp_occurrences.sum()
    chosen_index = np.random.choice(data.index, p=probabilities)
    return chosen_index

def filter_predictions(predictions, labels, model_type="GPT"):
    columns_with_ones = predictions.columns[(predictions == 1).any(axis=0)]
    filtered_predictions = predictions[columns_with_ones]
    label_mapping = {f"{model_type}_{label}": label for label in labels}
    
    # Get selected and unselected labels
    selected_labels = [label_mapping[col] for col in filtered_predictions.columns]
    unselected_labels = [label for label in labels if label not in selected_labels]
    
    return selected_labels, unselected_labels

def can_submit() -> bool:
    if "last_submission" not in st.session_state:
        return True
    return datetime.now() - st.session_state.last_submission >= timedelta(seconds=5)

def show_UserModelRanking(data: pd.DataFrame, softmax_Data: pd.DataFrame):
    # Initialize session state variables
    if 'user_agreement_given' not in st.session_state:
        st.session_state['user_agreement_given'] = False
    if 'expertise_rated' not in st.session_state:
        st.session_state['expertise_rated'] = False
    if 'expertise_level' not in st.session_state:
        st.session_state['expertise_level'] = None

    #gracias felipe thx: dynamic state detection thingy
    theme_mode = st.session_state.get("theme_mode", "light") 
    text_color = "#000000" if theme_mode == "light" else "#ffffff"
    bg_color = "#ffffff" if theme_mode == "light" else "#1e1e1e"
    border_color = "#dddddd" if theme_mode == "light" else "#4a4a4a"

    # Add styles including modern visual appearance for PDF viewer and buttons
    st.markdown(f"""
        <style>
            body {{
                background-color: {bg_color};
                color: {text_color};
            }}
            .pdf-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .pdf-viewer {{
                display: block;
                margin: 0 auto;
                max-width: 900px;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3);
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            iframe {{
                width: 80%;
                height: 670px;
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }}
            .stMultiSelect {{
                min-width: 300px !important;
            }}
            .stMultiSelect > div > div {{
                white-space: normal !important;
                height: auto !important;
            }}
        </style>
        """, unsafe_allow_html=True)

    if not st.session_state.user_agreement_given:
        st.markdown("""
        <style>
            .pdf-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;

            }
            .button-container {
                display: flex;
                flex-direction: row;
                justify-content: center;
                align-items: center;


            }
            iframe {
                width: 80%;
                height: 670px;
                border: none;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)

        # Contenedor principal para el PDF y los botones
        st.markdown("<div class='pdf-container'>", unsafe_allow_html=True)

        # Mostrar el visor PDF embebido
        pdf_path = 'src/CI cuestionario.pdf'
        # Título del documento
        st.title("Consentimiento Informado Cuestionario")

        # Contenido del documento
        st.markdown("""
        ### Universidad Católica de Temuco, Comité de Ética de la Investigación  
        **Dirección:** Manuel Montt 56, Fono: 452205489, Temuco, Chile.

        Estimado Usuario:

        Usted ha sido invitado a participar en el estudio titulado **“Modelos clasificadores en el lenguaje natural para el análisis de corpus de la honorable cámara de diputadas y diputados de Chile”**, dirigido por el académico **Dr. Julio César Rojas Mora** de la Facultad de Ingeniería de la Universidad Católica de Temuco.

        El objetivo de este estudio es comparar los resultados de etiquetación automática de contenido legislativo respecto al título de cada votación.

        Si usted acepta participar en este estudio, se le solicitará que responda un cuestionario, que contiene preguntas sobre su percepción de las diferentes etiquetas asignadas a cada votación. El cuestionario en sí le tomará aproximadamente **10 minutos**.

        La **participación en esta actividad es voluntaria** y no involucra ningún daño o peligro para su salud física o mental. Usted puede negarse a participar en cualquier momento del estudio sin que deba dar razones para ello, ni recibir ningún tipo de sanción.

        Los **datos obtenidos serán de carácter confidencial** y se guardará el anonimato. Estos datos serán organizados con un número asignado a cada participante. Su identidad estará disponible solo para el personal del proyecto y se mantendrá completamente confidencial. Los datos estarán a cargo del equipo de investigación de este estudio para el posterior desarrollo de informes y publicaciones dentro de revistas científicas. Todos los nuevos hallazgos significativos desarrollados durante el curso de la investigación le serán entregados a usted. Además, se entregará al establecimiento educacional un informe con los resultados globales sin identificar el nombre de los participantes.

        Las informaciones recolectadas no serán usadas para ningún otro propósito, además de los señalados anteriormente, sin su autorización previa y por escrito.

        Cualquier pregunta que desee hacer durante el proceso de investigación podrá contactar al académico **Dr. Julio César Rojas Mora** de la Facultad de Ingeniería de la Universidad Católica de Temuco.  
        - **Teléfono**: +56-45-2205229  
        - **Correo electrónico**: [jrojas@inf.uct.cl](mailto:jrojas@inf.uct.cl)  
        """)

        # Botón para visualizar el PDF
        pdf_path = 'src/CI cuestionario.pdf'  # Asegúrate de que este archivo exista en tu directorio
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'


        # Contenedor para los botones
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        # Botón para descargar el PDF
        # Botón para aceptar
        if st.button("Acepto participar en la evaluación", key="accept_button"):
            st.session_state.user_agreement_given = True
            st.experimental_rerun()
        with open("src/CI cuestionario.pdf", "rb") as pdf_file:
            st.download_button(
                label="Descargar comprobante de acuerdo",
                data=pdf_file,
                file_name="Acuerdo_Usuario.pdf",
                mime="application/pdf",
                key="download_button"
            )
        
        if st.button('Ver documento en formato pdf'):
            st.markdown(pdf_display, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return


    # Show expertise rating if not rated
    elif not st.session_state.expertise_rated:
        with st.container():
            st.markdown(r"""
                <div class='user-dialog'>
                    <h2 style='color: {text_color};'>Nivel de Experiencia</h2>
                    <p style='color: {text_color};'>
                        Por favor, indique una autopercepción de su nivel de conocimiento sobre política y legislación chilena:
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            expertise = st.slider("Nivel de Conocimiento (1-10):", 1, 10, 5)
            if st.button("Confirmar"):
                st.session_state.expertise_level = expertise
                st.session_state.expertise_rated = True
                st.experimental_rerun()
            
            st.markdown("<div class='blur-overlay'>", unsafe_allow_html=True)
            return

    # Show main content if all requirements met
    st.markdown("""
        <style>
            /* Increase width of multiselect dropdowns */
            .stMultiSelect {
                min-width: 300px !important;
            }
            
            /* Ensure menu items don't get truncated */
            .stMultiSelect > div > div {
                white-space: normal !important;
                height: auto !important;
            }
            
            /* Style for dropdown options */
            .stMultiSelect [data-baseweb="select"] {
                white-space: normal;
                word-wrap: break-word;
            }
        </style>
    """, unsafe_allow_html=True)
    # Define labels
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Initialize or get vote index
    if "selected_vote_index" not in st.session_state:
        vote_index = get_Softmax_Vote(softmax_Data)
        st.session_state.selected_vote_index = vote_index
    
    # Get current vote data
    vote_index = st.session_state.selected_vote_index
    vote_row = data[data['index'] == vote_index]

    # Step 5: Extract components (example: vote_name and labels)
    print('```````',vote_row,'```````````')
    vote_name = vote_row[data.columns.get_loc('vote_Name')]
    gpt_labels = vote_row[data.columns.get_loc('GPT_predictions_start_column'):data.columns.get_loc('GPT_predictions_end_column') + 1]
    rtm_labels = vote_row[data.columns.get_loc('RTM_predictions_start_column'):data.columns.get_loc('RTM_predictions_end_column') + 1]
    # Modificar estilos en línea, asegurando consistencia
    st.markdown(f"""
        <div style="
            padding: 1rem; 
            background-color: {bg_color} !important; 
            color: {text_color} !important; 
            border-left: 5px solid {border_color}; 
            border-radius: 0.5rem; 
            margin-bottom: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; color: {text_color} !important;">Instrucciones:</h4>
            <p style="font-size: 1.3rem; margin: 0; font-weight: 500; color: {text_color} !important;">
                1. Lea el Voto y compare ambas opciones.<br>
                2. Escoge la opción que consideres más aplicable al Voto.<br>
                3. Selecciona las categorías que consideres correctas y aplicables<br>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Mostrar el texto del voto
    vote_name = vote_row['vote_Name']
    st.markdown(f"""
        <div translate="no" style="
            padding: 1rem; 
            background-color: {bg_color} !important; 
            color: {text_color} !important; 
            border-left: 5px solid {border_color}; 
            border-radius: 0.5rem; 
            margin-bottom: 1rem;">
            <h4 style="margin: 0 0 0.5rem 0; color: {text_color} !important;">Voto:</h4>
            <h2 style="font-size: 1.8rem; margin: 0; color: {text_color} !important;">
                {vote_name}
            </h2>
        </div>
    """, unsafe_allow_html=True)


    # Filter and prepare predictions
    #gpt_labels = vote_row[[f"GPT_{label}" for label in labels]]
    #rtm_labels = vote_row[[f"RTM_{label}" for label in labels]]
    gpt_selected, gpt_unselected = filter_predictions(pd.DataFrame(gpt_labels).T, labels, model_type="GPT")
    rtm_selected, rtm_unselected = filter_predictions(pd.DataFrame(rtm_labels).T, labels, model_type="RTM")

    # Display model predictions in columns
    col1, col2 = st.columns(2)

    with col1:
        # Table for Opción 1 with a simple title row
        gpt_table_html = f"""
        <table style="width: 100%; border-collapse: collapse; border: 1px solid white; text-align: center;">
            <tr>
                <th style="padding: 8px; border: 1px solid white;">Opción 1</th>
            </tr>
            {''.join(f'<tr><td style="padding: 8px; border: 1px solid white;">{label}</td></tr>' for label in gpt_selected)}
        </table>
        """
        st.markdown(gpt_table_html, unsafe_allow_html=True)

    with col2:
        # Table for Opción 2 with a simple title row
        rtm_table_html = f"""
        <table style="width: 100%; border-collapse: collapse; border: 1px solid white; text-align: center;">
            <tr>
                <th style="padding: 8px; border: 1px solid white;">Opción 2</th>
            </tr>
            {''.join(f'<tr><td style="padding: 8px; border: 1px solid white;">{label}</td></tr>' for label in rtm_selected)}
        </table>
        """
        st.markdown(rtm_table_html, unsafe_allow_html=True)




    st.divider()
    with st.form(key='ranking_form', clear_on_submit=True):
        st.markdown("<p style='color: {text_color}!important; margin-top: 1rem;'>Selecciona todas las categorías que consideres correctas respecto al voto mostrado:</p>", unsafe_allow_html=True)
        additional_labels = st.multiselect(
            "",
            options=labels,
            default=[],
            key="gpt_additional"
        )
        model_choice = st.radio(
            "### ¿Cuál opción consideras que tuvo la mejor prediccion para esta votación?",
            ["Opción 1", "Opción 2"]
        )
        
        
        submitted = st.form_submit_button("Enviar")
        
        if submitted:
            if not model_choice:
                st.warning("Por favor, selecciona un modelo.")
            elif not can_submit():
                st.warning("Por favor, espere unos segundos antes de enviar otro voto.")
            else:
                with st.spinner('Procesando tu voto...'):
                    try:
                        # Map the selected model and prepare data
                        additional_labels = additional_labels

                        model_mapping = 0 if model_choice == "Opción 1" else 1
                        data_to_send = {
                            'vote_index': vote_index,
                            'vote_general_index': vote_general_index,
                            'vote_name': vote_name,
                            'chosen_model': model_mapping,
                            'consent_given': st.session_state.user_agreement_given,
                            'expertise_level': st.session_state.expertise_level,
                            'additional_labels': additional_labels if additional_labels else []
                        }
                        
                        # Save to database
                        save_UserModelRanking_To_Postgres(data_to_send)
                        
                        # Update submission timestamp
                        st.session_state.last_submission = datetime.now()
                        
                        # Show success and delay
                        st.success("¡Gracias por tu colaboración!")
                        time.sleep(1)
                        
                        # Get new vote and update state
                        new_vote_index = get_Softmax_Vote(softmax_Data)
                        st.session_state.selected_vote_index = new_vote_index
                        
                        # Rerun to refresh
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error al procesar el voto: {str(e)}")
