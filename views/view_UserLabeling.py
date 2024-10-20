import pandas as pd
import streamlit as st
import random
from back.post_HumanLabelData import save_Data_To_Postgres
from .view_About import label_selection_form

def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

def show_UserLabeling(data: pd.DataFrame):
    st.title("Etiquetado de Votaciones del Congreso")

    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    if "new_vote_required" not in st.session_state:
        st.session_state.new_vote_required = True

    if "selected_vote" not in st.session_state or st.session_state.new_vote_required:
        vote_index = get_Random_Vote(data)
        st.session_state.selected_vote = data.iloc[vote_index]
        st.session_state.new_vote_required = False

    vote = st.session_state.selected_vote

    st.write("Lee el siguiente tema de votación y selecciona las etiquetas correspondientes.")
    st.markdown(f"## {vote['votaciones_Nombre']}")
    st.markdown(f"##### {vote['_id']}")

    # Call the refactored function for label selection using multiselect
    data_to_send = label_selection_form(labels, vote, form_key="user_labeling_form")

    if data_to_send:
        save_Data_To_Postgres(data_to_send)
        st.success("¡Gracias por tu colaboración!")

        st.session_state.new_vote_required = True

        # Reset the multiselect state
        st.session_state.pop("user_labeling_form_multiselect", None)

        st.experimental_rerun()
