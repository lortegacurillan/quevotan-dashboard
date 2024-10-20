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

    # Create a form for label selection using multiselect
    with st.form(key='labeling_form'):
        st.write("Selecciona las etiquetas que correspondan:")
        selected_labels = st.multiselect(
            "Selecciona las etiquetas:",
            options=labels,
            default=[],  # No preselected labels
            key="multiselect_labels"
        )
        submitted = st.form_submit_button("Enviar")

    # After form submission
    if submitted:
        if selected_labels:
            # Prepare data for submission, setting the labels to 1 if selected, otherwise 0
            data_to_send = {
                'vote_index': vote['_id'],
                'votaciones_Nombre': vote['votaciones_Nombre'],
                'Seguridad y Defensa': int("Seguridad y Defensa" in selected_labels),
                'Relaciones Internacionales': int("Relaciones Internacionales" in selected_labels),
                'Energía y Medioambiente': int("Energía y Medioambiente" in selected_labels),
                'Justicia y Derechos Humanos': int("Justicia y Derechos Humanos" in selected_labels),
                'Educación': int("Educación" in selected_labels),
                'Políticas Sociales': int("Políticas Sociales" in selected_labels),
                'Deporte, Cultura y Salud': int("Deporte, Cultura y Salud" in selected_labels),
                'Política Económica': int("Política Económica" in selected_labels),
                'Política Interna': int("Política Interna" in selected_labels),
                'Participación Ciudadana': int("Participación Ciudadana" in selected_labels),
            }

            # Save data to PostgreSQL
            save_Data_To_Postgres(data_to_send)

            # Success message
            st.success("¡Gracias por tu colaboración!")

            # Mark that a new vote is required for the next cycle
            st.session_state.new_vote_required = True

            # Reset the multiselect state
            st.session_state.pop("multiselect_labels", None)

            # Refresh the page to display the new vote
            st.experimental_rerun()  # Safe method to refresh the page without experimental functions

        else:
            st.warning("Por favor, selecciona al menos una etiqueta.")
