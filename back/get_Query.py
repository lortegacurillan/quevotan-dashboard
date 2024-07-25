import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RandomForestModel import load_Model

import numpy as np
import re
import numpy as np

loaded_model, loaded_vectorizer, loaded_scaler = load_Model.load_model('RandomForestModel/multi_target_forest.pkl')


def get_QueryResponse(text: str, model= loaded_model, vectorizer= loaded_vectorizer, scaler= loaded_scaler)-> np.ndarray:
    # Pasar el texto a lower case y quitar los caracteres especiales
    text_processed = text.lower()
    text_processed = re.sub(r'[^\w\s]', '', text_processed)

    # Vectorización del texto
    text_vectorized = vectorizer.transform([text_processed])

    # Crear un vector nulo para 'votaciones_Nombre' ya que solo estamos probando el texto
    total_features = scaler.n_features_in_

    # Número de características del texto vectorizado
    text_features = text_vectorized.shape[1]

    # Tamaño del vector nulo
    name_vector_size = total_features - text_features

    # Crear un vector nulo para 'votaciones_Nombre'
    name_vector = np.zeros((1, name_vector_size))#name_vector_size = X_name.shape[1]
    # Combinar las características de texto vectorizadas con las demás características
    Y_test_combined = np.hstack((name_vector, text_vectorized.toarray()))

    # Escalar las características
    Y_test_scaled = scaler.transform(Y_test_combined)

    # Predicción de las etiquetas
    y_pred = model.predict(Y_test_scaled)

    return y_pred
 



query = """
"""



