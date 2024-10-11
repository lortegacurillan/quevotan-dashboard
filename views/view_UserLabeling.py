import pandas as pd
import streamlit as st
import random
from back.post_HumanLabelData import save_Data_To_Postgres

# Function to get a random vote
def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

# Main view
def show_UserLabeling(data: pd.DataFrame):
    st.title("Etiquetado de Votaciones del Congreso")

    # Define available labels
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Initialize session state variables if they don't exist
    if "new_vote_required" not in st.session_state:
        st.session_state.new_vote_required = True  # Ensure it starts with a fresh vote

    if "selected_vote" not in st.session_state or st.session_state.new_vote_required:
        # Get a new random vote if one is required
        vote_index = get_Random_Vote(data)
        st.session_state.selected_vote = data.iloc[vote_index]
        st.session_state.new_vote_required = False  # Reset the flag after loading the vote

    # Always refer to the fixed vote stored in session state
    vote = st.session_state.selected_vote  

    # Display selected vote
    st.write("Lee el siguiente tema de votación y selecciona las etiquetas correspondientes.")
    st.markdown(f"## {vote['votaciones_Nombre']}")
    st.markdown(f"##### {vote['_id']}")

    # Create a form for label selection
    selected_Labels = {}
    with st.form(key='labeling_form'):
        st.write("Selecciona las etiquetas que correspondan:")
        for label in labels:
            selected_Labels[label] = st.checkbox(label, key=label)  # Ensure each checkbox has a unique key
        submitted = st.form_submit_button("Enviar")

    # After form submission
    if submitted:
        if any(selected_Labels.values()):
            # Prepare data for submission
            data_to_send = {
                'vote_index': vote['_id'],
                'votaciones_Nombre': vote['votaciones_Nombre'],
                'Seguridad y Defensa': int(selected_Labels["Seguridad y Defensa"]),
                'Relaciones Internacionales': int(selected_Labels["Relaciones Internacionales"]),
                'Energía y Medioambiente': int(selected_Labels["Energía y Medioambiente"]),
                'Justicia y Derechos Humanos': int(selected_Labels["Justicia y Derechos Humanos"]),
                'Educación': int(selected_Labels["Educación"]),
                'Políticas Sociales': int(selected_Labels["Políticas Sociales"]),
                'Deporte, Cultura y Salud': int(selected_Labels["Deporte, Cultura y Salud"]),
                'Política Económica': int(selected_Labels["Política Económica"]),
                'Política Interna': int(selected_Labels["Política Interna"]),
                'Participación Ciudadana': int(selected_Labels["Participación Ciudadana"]),
            }

            # Save data to PostgreSQL
            save_Data_To_Postgres(data_to_send)

            # Success message
            st.success("¡Gracias por tu colaboración!")

            # Mark that a new vote is required for the next cycle
            st.session_state.new_vote_required = True

            # Clear the form by resetting the session state for checkboxes **AFTER** submission
            for label in labels:
                if label in st.session_state:
                    del st.session_state[label]  # Reset checkbox state

            # Refresh the page to display the new vote
            st.experimental_rerun()  # Safe method to refresh the page without experimental functions

        else:
            st.warning("Por favor, selecciona al menos una etiqueta.")
