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

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Cargar componentes del modelo
loaded_model, loaded_vectorizer, loaded_scaler = load_model('RandomForestModel/multi_target_forest.pkl')
loaded_model.n_jobs = 1  # Asegúrate de que el modelo use un solo trabajo

def get_QueryResponse(text: str, model=loaded_model, vectorizer=loaded_vectorizer, scaler=loaded_scaler):
    # Procesar el texto
    text_processed = text.lower()
    text_processed = re.sub(r'[^\w\s]', '', text_processed)

    # Vectorizar el texto
    text_vectorized = vectorizer.transform([text_processed])

    # Crear un vector nulo para 'votaciones_Nombre'
    total_features = scaler.n_features_in_
    text_features = text_vectorized.shape[1]
    name_vector_size = total_features - text_features
    name_vector = np.zeros((1, name_vector_size))

    # Combinar características de texto con el vector nulo
    Y_test_combined = np.hstack((name_vector, text_vectorized.toarray()))

    # Escalar las características
    Y_test_scaled = scaler.transform(Y_test_combined)

    # Predecir las etiquetas con el backend threading
    with parallel_backend('threading'):
        y_pred = model.predict(Y_test_scaled)

    return y_pred

def search_votacion(texto, df):
    if texto in df['votaciones_Nombre'].values:
        # Columnas a devolver si se encuentra el texto
        columnas = [
            'Seguridad y Defensa', 'Relaciones Internacionales', 'Energía y Medioambiente',
            'Justicia y Derechos Humanos', 'Educación', 'Políticas Sociales',
            'Deporte, Cultura y Salud', 'Política Económica', 'Política Interna',
            'Participación Ciudadana'
        ]
        resultado = df[df['votaciones_Nombre'] == texto][columnas].iloc[0]  # Solo la primera coincidencia
        columnas_con_uno = resultado[resultado == 1].index.tolist()  # Filtrar columnas con valor 1
        resultado_invertido = resultado[columnas_con_uno].to_frame()  # Convertir a DataFrame
        return resultado_invertido.transpose()  # Invertir columnas y filas
    else:
        return "Esta votación no fue etiquetada por GPT."