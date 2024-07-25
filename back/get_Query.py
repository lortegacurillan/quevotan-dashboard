from ./RandomForestModel.load_Model import load_model

load_model()

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

loaded_model, loaded_vectorizer, loaded_scaler = load_model('model\multi_target_forest.pkl')



import re
def test(text: str, model: MultiOutputClassifier, vectorizer: TfidfVectorizer, scaler: StandardScaler) -> pd.DataFrame:
    # Pasar el texto a lower case y quitar los caracteres especiales
    text_processed = text.lower()
    text_processed = re.sub(r'[^\w\s]', '', text_processed)

    # Vectorización del texto
    text_vectorized = vectorizer.transform([text_processed])

    # Crear un vector nulo para 'votaciones_Nombre' ya que solo estamos probando el texto
    # Determinar el tamaño esperado del vector nulo
    # Número total de características que el scaler espera
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
    X_test_scaled = scaler.transform(Y_test_combined)

    # Predicción de las etiquetas
    y_pred = model.predict(X_test_scaled)

    return y_pred
