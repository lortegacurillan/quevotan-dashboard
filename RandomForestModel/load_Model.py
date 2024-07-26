import joblib

def load_model(filename):
    try:
        loaded_objects = joblib.load(filename)
        if isinstance(loaded_objects, tuple) and len(loaded_objects) == 3:
            return loaded_objects
        else:
            raise ValueError("Loaded object is not a tuple with 3 elements.")
    except Exception as e:
        return None, None, None
