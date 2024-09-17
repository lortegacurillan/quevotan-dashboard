import pandas as pd
import streamlit as st
import random
from firebase_admin import credentials, initialize_app

cred = credentials.ApplicationDefault()
initialize_app(cred)

def get_random_vote(data):
    random_index = random.randint(0, len(data) - 1)
    return data.iloc[random_index]

def labeling_view(data):
    st.title("Etiquetado de Votaciones")

    # Get a random vote
    vote = get_random_vote(data)

    st.write("Por favor, lee el siguiente texto y selecciona las etiquetas que consideres apropiadas.")

    # Display the vote text
    st.markdown(f"### {vote['Texto']}")  # Adjust 'Texto' to your column name

    # Create checkboxes for labels
    selected_labels = []
    with st.form(key='labeling_form'):
        st.write("Selecciona las etiquetas que correspondan:")
        for label in labels:
            if st.checkbox(label):
                selected_labels.append(label)
        submitted = st.form_submit_button("Enviar")

    # When the form is submitted
    if submitted:
        if selected_labels:
            # Prepare data to send to Firestore
            data_to_send = {
                'vote_id': vote['id'],  # Replace 'id' with your identifier column
                'texto': vote['Texto'],
                'selected_labels': selected_labels,
                'timestamp': firestore.SERVER_TIMESTAMP  # Import firestore from firebase_admin
            }

            # Send data to Firestore (we'll cover this in the next section)
            send_data_to_firestore(data_to_send)

            st.success("¡Gracias por tu colaboración!")
        else:
            st.warning("Por favor, selecciona al menos una etiqueta.")
