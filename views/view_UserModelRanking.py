import pandas as pd
import streamlit as st
import random
from back.post_RankingData import save_UserModelRanking_To_Postgres

# Function to get a random vote
def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

# Function to filter the prediction columns to show only categories with a value of 1
def filter_predictions(predictions, labels):
    # Get the columns that have a value of 1
    filtered_predictions = predictions.loc[:, (predictions == 1).any()]
    # Map the column names to the generic labels based on their original index
    filtered_predictions.columns = [labels[i] for i in range(len(filtered_predictions.columns))]
    return filtered_predictions

# Main view function for UserModelRanking
def show_UserModelRanking(data: pd.DataFrame):
    st.title("Comparación de Etiquetas: Modelos")

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
        st.session_state.selected_model = None  # Track which model the user selects

    # Get the current vote data
    vote_index = st.session_state.selected_vote_index
    vote_row = data.iloc[vote_index]

    # Extract the vote name and predictions for GPT and RTM
    vote_name = vote_row['vote_Name']  # Assuming 'vote_Name' is the column with the vote name
    gpt_labels = vote_row[[f"{label}_GPT" for label in labels]]  # Extract GPT prediction columns
    rtm_labels = vote_row[[f"{label}_RTM" for label in labels]]  # Extract RTM prediction columns

    # Filter GPT and RTM predictions and rename the columns for display
    filtered_gpt_labels = filter_predictions(pd.DataFrame(gpt_labels).T, labels)
    filtered_rtm_labels = filter_predictions(pd.DataFrame(rtm_labels).T, labels)

    # Display the vote name
    st.markdown(f"### {vote_name}")

    # Display Model 1 (GPT) predictions
    st.write("### Modelo 1")
    st.dataframe(filtered_gpt_labels)

    # Display Model 2 (RTM) predictions
    st.write("### Modelo 2")
    st.dataframe(filtered_rtm_labels)

    # Allow the user to select which model they prefer
    st.write("### ¿Cuál modelo consideras mejor para esta votación?")
    model_choice = st.radio("Elige el modelo:", ["Modelo 1", "Modelo 2"], key="model_choice")

    # Provide a text area for comments
    user_comment = st.text_area("Escribe un comentario sobre tu elección:")

    # Create a form to submit the user's feedback
    with st.form(key='ranking_form'):
        submitted = st.form_submit_button("Enviar")

    if submitted:
        # Only proceed if a model has been selected
        if not model_choice:
            st.warning("Por favor, selecciona un modelo.")
        else:
            # Map the selected model to 0 or 1
            model_mapping = 0 if model_choice == "Modelo 1" else 1

            # Structure the data for submission
            data_to_send = {
                'vote_index': vote_index,  # Add the vote index to be stored
                'vote_name': vote_name,
                'chosen_model': model_mapping,  # Store 0 for Model 1 (GPT) and 1 for Model 2 (RTM)
                'user_comment': user_comment
            }

            save_UserModelRanking_To_Postgres(data_to_send)

            st.success("¡Gracias por tu colaboración!")

            # Reset the selected model and form
            st.session_state.selected_model = None

            # Reset the model choice key to reset the radio button state
            st.session_state.pop("model_choice", None)

            # Randomly select a new vote for the next round
            st.session_state.selected_vote_index = get_Random_Vote(data)

            # Optional: re-render the page
            st.experimental_rerun()
