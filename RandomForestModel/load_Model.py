import joblib
def load_model(filename):
    model, vectorizer, scaler = joblib.load(filename)
    return model, vectorizer, scaler
