import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from RandomForestModel.load_Model import load_model
import joblib
import numpy as np
import re


def load_model(filename):
    try:
        loaded_objects = joblib.load(filename)
        if isinstance(loaded_objects, tuple) and len(loaded_objects) == 3:
            return loaded_objects
        else:
            raise ValueError("Loaded object is not a tuple with 3 elements.")
    except Exception as e:
        return None, None, None



# Load model components
loaded_model, loaded_vectorizer, loaded_scaler = load_model('RandomForestModel/multi_target_forest.pkl')

if loaded_model is None or loaded_vectorizer is None or loaded_scaler is None:
    raise ValueError("Failed to load model components. Check the logs for details.")

def get_QueryResponse(text: str, model=loaded_model, vectorizer=loaded_vectorizer, scaler=loaded_scaler) -> np.ndarray:
    # Process the text
    text_processed = text.lower()
    text_processed = re.sub(r'[^\w\s]', '', text_processed)

    # Vectorize the text
    text_vectorized = vectorizer.transform([text_processed])

    # Create a null vector for 'votaciones_Nombre'
    total_features = scaler.n_features_in_
    text_features = text_vectorized.shape[1]
    name_vector_size = total_features - text_features
    name_vector = np.zeros((1, name_vector_size))

    # Combine text features with the null vector
    Y_test_combined = np.hstack((name_vector, text_vectorized.toarray()))

    # Scale the features
    Y_test_scaled = scaler.transform(Y_test_combined)

    # Predict the labels
    y_pred = model.predict(Y_test_scaled)

    return y_pred
