import joblib
def load_model(filename):
    try:
        model, vectorizer, scaler = joblib.load(filename)
        return model, vectorizer, scaler
    except Exception as e:
        return f"Error al cargar el modelo: {e}"





