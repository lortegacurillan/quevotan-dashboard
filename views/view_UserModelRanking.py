import pandas as pd
import numpy as np
import streamlit as st
import random
from back.post_RankingData import save_UserModelRanking_To_Postgres

# Function to get a random vote
def get_Random_Vote(data: pd.DataFrame) -> int:
    random_index = random.randint(0, len(data) - 1)
    return random_index

def get_Softmax_Vote(data: pd.DataFrame) -> int:
    # Invert occurrences to prioritize lower values
    inverted_occurrences = data['appearance_count'].max() - data['appearance_count']
    
    # Compute softmax probabilities
    exp_occurrences = np.exp(inverted_occurrences)  # Exponentiate the inverted values
    probabilities = exp_occurrences / exp_occurrences.sum()  # Calculate softmax probabilities

    # Select a vote based on the computed probabilities
    chosen_index = np.random.choice(data.index, p=probabilities)
    
    return chosen_index

def filter_predictions(predictions, labels, model_type="GPT"):
    # Find columns with at least one occurrence of 1
    columns_with_ones = predictions.columns[(predictions == 1).any(axis=0)]
    
    # Filter the DataFrame to only include those columns
    filtered_predictions = predictions[columns_with_ones]
    
    # Map the filtered columns to the corresponding labels
    label_mapping = {f"{model_type}_{label}": label for label in labels}
    renamed_columns = [label_mapping.get(col, col) for col in filtered_predictions.columns]
    
    # Set the new column names in the filtered DataFrame
    filtered_predictions.columns = renamed_columns

    return filtered_predictions



# Main view function for UserModelRanking
def show_UserModelRanking(data: pd.DataFrame, softmax_Data: pd.DataFrame):
    st.title("Comparación de Etiquetas: Modelos")

    # Define the labels (these should match the ones in the DataFrame)
    labels = [
        "Seguridad y Defensa", "Relaciones Internacionales", "Energía y Medioambiente",
        "Justicia y Derechos Humanos", "Educación", "Políticas Sociales",
        "Deporte, Cultura y Salud", "Política Económica", "Política Interna", "Participación Ciudadana"
    ]

    # Initialize session state variables if they don't exist
    if "selected_vote_index" not in st.session_state:
        vote_index = get_Softmax_Vote(softmax_Data)
        st.session_state.selected_vote_index = vote_index
        st.session_state.selected_model = None  # Track which model the user selects

    # Get the current vote data
    vote_index = st.session_state.selected_vote_index
    vote_row = data.iloc[vote_index]

    # Extract the vote name and predictions for GPT and RTM
    vote_name = vote_row['vote_Name']  # Assuming 'vote_Name' is the column with the vote name
    gpt_labels = vote_row[[f"GPT_{label}" for label in labels]]  # Extract GPT prediction columns
    rtm_labels = vote_row[[f"RTM_{label}" for label in labels]]  # Extract RTM prediction columns

    # Filter GPT and RTM predictions based on the value of 1 and map back to original labels
    filtered_gpt_labels = filter_predictions(pd.DataFrame(gpt_labels).T, labels, model_type="GPT")
    filtered_rtm_labels = filter_predictions(pd.DataFrame(rtm_labels).T, labels, model_type="RTM")

    # Display the vote name
    st.markdown(f"### {vote_name}")

    # Display Model 1 (GPT) predictions
    st.write("### Modelo 1")
    st.write(filtered_gpt_labels)  # Display as a list instead of a DataFrame for cleaner output

    # Display Model 2 (RTM) predictions
    st.write("### Modelo 2")
    st.write(filtered_rtm_labels)  # Display as a list instead of a DataFrame for cleaner output

    # Allow the user to select which model they prefer
    st.write("### ¿Cuál modelo consideras que tuvo la mejor prediccion para esta votación?")
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
            st.session_state.selected_vote_index = get_Softmax_Vote(softmax_Data)

            # Optional: re-render the page
            st.experimental_rerun()
