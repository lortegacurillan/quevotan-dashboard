import pandas as pd
import streamlit as st
import random
from back.post_RankingData import save_UserModelRanking_To_Postgres

# Function to get a random vote
def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

# Main view function for UserModelRanking
def show_UserModelRanking(data: pd.DataFrame):
    st.title("Comparación de Etiquetas: GPT-3.5 vs. RTM")

    # Define the labels (these should match the ones in the DataFrame)
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Initialize session state variables if they don't exist
    if "selected_vote_index" not in st.session_state:
        vote_index = get_Random_Vote(data)
        st.session_state.selected_vote_index = vote_index

    # Get the current vote data
    vote_index = st.session_state.selected_vote_index
    vote_row = data.iloc[vote_index]

    # Extract the vote name and predictions for GPT and RTM
    vote_name = vote_row['vote_Name']  # Assuming 'vote_Name' is the column with the vote name
    gpt_labels = vote_row[[f"{label}_GPT" for label in labels]]  # Extract GPT prediction columns
    rtm_labels = vote_row[[f"{label}_RTM" for label in labels]]  # Extract RTM prediction columns

    # Display the vote name
    st.markdown(f"### {vote_name}")

    # Display GPT-3.5 and RTM labels side by side in editable text fields
    st.write("### Etiquetas propuestas por GPT-3.5")
    edited_gpt_labels = {}
    for idx, label in enumerate(gpt_labels.index):
        edited_gpt_labels[label] = st.text_input(f"GPT-3.5 - {label}", gpt_labels[label])

    st.write("### Etiquetas propuestas por RTM")
    edited_rtm_labels = {}
    for idx, label in enumerate(rtm_labels.index):
        edited_rtm_labels[label] = st.text_input(f"RTM - {label}", rtm_labels[label])

    # Allow the user to select which model they prefer
    st.write("### ¿Cuál modelo consideras mejor para esta votación?")
    model_choice = st.radio("Elige el modelo:", ["GPT-3.5", "RTM"])

    # Provide a text area for comments
    user_comment = st.text_area("Escribe un comentario sobre tu elección:")

    # Create a form to submit the user's feedback
    with st.form(key='ranking_form'):
        submitted = st.form_submit_button("Enviar")

    # After submission
    if submitted:
        # Structure the data for submission (to be handled later)
        data_to_send = {
            'vote_name': vote_name,
            'gpt_labels': edited_gpt_labels,
            'rtm_labels': edited_rtm_labels,
            'chosen_model': model_choice,
            'user_comment': user_comment
        }

        save_UserModelRanking_To_Postgres(data_to_send)

        st.success("¡Gracias por tu colaboración!")

        # Randomly select a new vote for the next round
        st.session_state.selected_vote_index = get_Random_Vote(data)

        # Optional: re-render the page
        st.experimental_rerun()
