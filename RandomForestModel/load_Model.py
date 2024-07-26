import joblib
import logging

def load_model(filename):
    try:
        model, vectorizer, scaler = joblib.load(filename)
        return model, vectorizer, scaler
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None, None, None
