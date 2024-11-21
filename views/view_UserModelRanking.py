import pandas as pd
import numpy as np
import streamlit as st
import random
import time
from datetime import datetime, timedelta
from back.post_RankingData import save_UserModelRanking_To_Postgres

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
    renamed_columns = [label_mapping.get(col, col) for col in filtered_predictions.columns]
    filtered_predictions.columns = renamed_columns
    return filtered_predictions

def can_submit() -> bool:
    if "last_submission" not in st.session_state:
        return True
    return datetime.now() - st.session_state.last_submission >= timedelta(seconds=5)

def show_UserModelRanking(data: pd.DataFrame, softmax_Data: pd.DataFrame):
    st.markdown("""
    <style>
        @keyframes highlight {
            0% { box-shadow: 0 0 0 0 rgba(255,255,255,0.1); }
            50% { box-shadow: 0 0 20px 0 rgba(255,255,255,0.2); }
            100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.1); }
        }
        .vote-container {
            animation: highlight 2s ease-in-out;
            animation-delay: 0.1s;
            animation-fill-mode: both;
            content-visibility: auto;
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
            1. Compare las predicciones de ambos modelos<br>
            2. Vote por el modelo que considere más preciso<br>
            3. Explique su elección en el cuadro de comentarios
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter and prepare predictions
    gpt_labels = vote_row[[f"GPT_{label}" for label in labels]]
    rtm_labels = vote_row[[f"RTM_{label}" for label in labels]]
    filtered_gpt_labels = filter_predictions(pd.DataFrame(gpt_labels).T, labels, model_type="GPT")
    filtered_rtm_labels = filter_predictions(pd.DataFrame(rtm_labels).T, labels, model_type="RTM")

    # Display model predictions in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #FFFFFF;'>Modelo 1</h3>", unsafe_allow_html=True)
        st.write(filtered_gpt_labels)
    
    with col2:
        st.markdown("<h3 style='color: #FFFFFF;'>Modelo 2</h3>", unsafe_allow_html=True)
        st.write(filtered_rtm_labels)

    # Rest of your existing form code...
    with st.form(key='ranking_form', clear_on_submit=True):
        model_choice = st.radio(
            "### ¿Cuál modelo consideras que tuvo la mejor prediccion para esta votación?",
            ["Modelo 1", "Modelo 2"]
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
                        model_mapping = 0 if model_choice == "Modelo 1" else 1
                        data_to_send = {
                            'vote_index': vote_index,
                            'vote_name': vote_name,
                            'chosen_model': model_mapping,
                            'user_comment': user_comment
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