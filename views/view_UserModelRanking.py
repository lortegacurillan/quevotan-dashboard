import pandas as pd
import numpy as np
import streamlit as st
import random
import time
from datetime import datetime, timedelta
from back.post_RankingData import save_UserModelRanking_To_Postgres
import os

def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

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
    if 'consent_given' not in st.session_state:
        st.session_state['consent_given'] = False
    if 'expertise_rated' not in st.session_state:
        st.session_state['expertise_rated'] = False
    if 'expertise_level' not in st.session_state:
        st.session_state['expertise_level'] = None

    # Add styles including vertical button stacking
    st.markdown("""
        <style>
            .blur-overlay {
                filter: blur(5px);
                pointer-events: none;
            }
            .consent-dialog {
                background-color: #1e1e1e;
                padding: 2rem;
                border-radius: 0.5rem;
                border-left: 5px solid #4a4a4a;
                margin: 2rem auto;
                max-width: 600px;
            }
            .button-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1rem;
                margin-top: 1rem;
                width: 100%;
            }
            .button-container > div {
                width: 100%;
                display: flex;
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.consent_given:
        with st.container():
            st.markdown("""
                <div class='consent-dialog'>
                    <h2 style='color: #ffffff;'>Consentimiento Informado</h2>
                    <p style='color: #ffffff;'>
                        Al participar en esta evaluación, usted acepta que:
                        <br>• Sus respuestas serán utilizadas con fines de investigación
                        <br>• Los datos serán tratados de forma anónima
                        <br>• Puede detener su participación en cualquier momento
                    </p>
                    <div class='button-container'>
            """, unsafe_allow_html=True)
            
            if st.button("Acepto participar en la evaluación"):
                st.session_state.consent_given = True
                st.experimental_rerun()
            
            with open("src/CI cuestionario.pdf", "rb") as pdf_file:
                st.download_button(
                    label="Descargar comprobante de consentimiento",
                    data=pdf_file,
                    file_name="Consentimiento Informado.pdf",
                    mime="application/pdf"
                )
            
            st.markdown("""
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<div class='blur-overlay'>", unsafe_allow_html=True)
            return

    # Show expertise rating if not rated
    elif not st.session_state.expertise_rated:
        with st.container():
            st.markdown("""
                <div class='consent-dialog'>
                    <h2 style='color: #ffffff;'>Nivel de Experiencia</h2>
                    <p style='color: #ffffff;'>
                        Por favor, indique una autopercepcion de su nivel de conocimiento sobre política y legislación chilena:
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            expertise = st.slider("Nivel de experiencia (1-10):", 1, 10, 5)
            if st.button("Confirmar"):
                st.session_state.expertise_level = expertise
                st.session_state.expertise_rated = True
                st.experimental_rerun()
            
            # Blur rest of content
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
    vote_row = data.iloc[vote_index]

    # Extract vote information with matching box style
    vote_name = vote_row['vote_Name']
    st.markdown(f"""
    <style>
        @keyframes fadeHighlight {{
            0% {{ background-color: #ffffff; }}
            100% {{ background-color: #1e1e1e; }}
        }}
    </style>
    <div style='padding: 1rem; 
                animation: fadeHighlight 2s ease-out; 
                background-color: #1e1e1e; 
                border-radius: 0.5rem; 
                margin: 1rem 0; 
                border-left: 5px solid #4a4a4a;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #666666;'>Voto:</h4>
        <h2 style='font-size: 1.8rem; margin: 0; color: #ffffff;'>
            {vote_name}
        </h2>
    </div>

    <div style='padding: 1rem; 
                background-color: #1e1e1e; 
                border-radius: 0.5rem; 
                margin: 1rem 0; 
                border-left: 5px solid #4a4a4a;'>
        <h4 style='margin: 0 0 0.5rem 0; color: #666666;'>Instrucciones:</h4>
        <p style='font-size: 1.3rem; margin: 0; color: #ffffff; font-weight: 500;'>
            1. Lea el Voto y compare ambas opciones<br>
            2. Escoge la opcion que consideres mas aplicable al Voto<br>
            3. Agrega categorias adicionales si consideras aplicable<br>
            4. Escribe un comentario sobre tu elección
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter and prepare predictions
    gpt_labels = vote_row[[f"GPT_{label}" for label in labels]]
    rtm_labels = vote_row[[f"RTM_{label}" for label in labels]]
    gpt_selected, gpt_unselected = filter_predictions(pd.DataFrame(gpt_labels).T, labels, model_type="GPT")
    rtm_selected, rtm_unselected = filter_predictions(pd.DataFrame(rtm_labels).T, labels, model_type="RTM")

    # Display model predictions in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #FFFFFF;'>Opción 1</h3>", unsafe_allow_html=True)
        st.multiselect(
            "",
            options=gpt_selected,
            default=gpt_selected,
            disabled=True,
            key="gpt_selected"
        )
        
        st.markdown("<p style='color: #666666; margin-top: 1rem;'>Categorías adicionales que consideras aplicables:</p>", unsafe_allow_html=True)
        additional_gpt = st.multiselect(
            "",
            options=gpt_unselected,
            default=[],
            key="gpt_additional"
        )
    
    with col2:
        st.markdown("<h3 style='color: #FFFFFF;'>Opción 2</h3>", unsafe_allow_html=True)
        st.multiselect(
            "",
            options=rtm_selected,
            default=rtm_selected,
            disabled=True,
            key="rtm_selected"
        )
        
        st.markdown("<p style='color: #666666; margin-top: 1rem;'>Categorías adicionales que consideras aplicables:</p>", unsafe_allow_html=True)
        additional_rtm = st.multiselect(
            "",
            options=rtm_unselected,
            default=[],
            key="rtm_additional"
        )
            
    with st.form(key='ranking_form', clear_on_submit=True):
        model_choice = st.radio(
            "### ¿Cuál opción consideras que tuvo la mejor prediccion para esta votación?",
            ["Opción 1", "Opción 2"]
        )
        
        user_comment = st.text_area(
            "Escribe un comentario sobre tu elección:"
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
                        additional_labels = additional_gpt if model_choice == "Opción 1" else additional_rtm

                        model_mapping = 0 if model_choice == "Opción 1" else 1
                        data_to_send = {
                            'vote_index': vote_index,
                            'vote_name': vote_name,
                            'chosen_model': model_mapping,
                            'user_comment': user_comment,
                            'consent_given': st.session_state.consent_given,
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

