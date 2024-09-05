import pandas as pd
import streamlit as st
import os
import sys
import logging
import numpy as np
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RandomForestModel.load_Model import load_model
from sklearn.utils import parallel_backend

#Logging configuration
logging.basicConfig(level=logging.DEBUG)

#Load the model components
loaded_model, loaded_vectorizer, loaded_scaler = load_model('RandomForestModel/multi_target_forest.pkl')
loaded_model.n_jobs = 1 # Avoid thread conflicts

def get_QueryResponse(text: str, model=loaded_model, vectorizer=loaded_vectorizer, scaler=loaded_scaler)->np.ndarray:
    '''
    This function takes a text and returns the predicted labels for it

    Parameters:
    text (str): The text to predict
    model (RandomForestClassifier): The model to predict the labels
    vectorizer (TfidfVectorizer): The vectorizer to transform the text
    scaler (StandardScaler): The scaler to scale the features

    Returns:
    np.ndarray: The predicted labels
    '''

    #Text processing
    text_processed = text.lower()
    text_processed = re.sub(r'[^\w\s]', '', text_processed)

    #text vectorization
    text_vectorized = vectorizer.transform([text_processed])

    #Create a null vector for 'votaciones_Nombre'
    total_features = scaler.n_features_in_
    text_features = text_vectorized.shape[1]
    name_vector_size = total_features - text_features
    name_vector = np.zeros((1, name_vector_size))

    #combine text features with null vector
    Y_test_combined = np.hstack((name_vector, text_vectorized.toarray()))

    #sclaing the features
    Y_test_scaled = scaler.transform(Y_test_combined)

    #lable prediction with threading backend
    with parallel_backend('threading'):
        y_pred = model.predict(Y_test_scaled)

    return y_pred

def search_votacion(text:str, df:pd.DataFrame):
    '''
    This function takes a text and returns the labels of the votation if it is found in the DataFrame

    Parameters:
    text (str): The text to search in the DataFrame
    df (pd.DataFrame): The DataFrame with the labels

    Returns:
    pd.DataFrame or str: The labels of the votation if it is found, or a message if it is not found
    '''
    if text in df['votaciones_Nombre'].values:
        #columns to return if the text is found
        columnas = [
            'Seguridad y Defensa', 'Relaciones Internacionales', 'Energía y Medioambiente',
            'Justicia y Derechos Humanos', 'Educación', 'Políticas Sociales',
            'Deporte, Cultura y Salud', 'Política Económica', 'Política Interna',
            'Participación Ciudadana'
        ]
        coincidences = df[df['votaciones_Nombre'] == text][columnas].iloc[0]  # Solo la primera coincidencia
        true_columns = coincidences[coincidences == 1].index.tolist()  # Filtrar columnas con valor 1
        reframed_coincidences = coincidences[true_columns].to_frame()  # Convertir a DataFrame
        return reframed_coincidences.transpose()  # Invertir columnas y filas
    else:
        return "Esta votación no fue etiquetada por GPT."