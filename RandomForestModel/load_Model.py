import joblib
def load_model(filename):
    try:
        model, vectorizer, scaler = joblib.load(filename)
        return model, vectorizer, scaler
    except Exception as e:
        return f"Error al cargar el modelo: {e}"




loaded_model, loaded_vectorizer, loaded_scaler = load_model('RandomForestModel\multi_target_forest.pkl')