import joblib

filename = 'RandomForestModel/multi_target_forest.pkl'
loaded_objects = joblib.load(filename)
print(type(loaded_objects), len(loaded_objects) if isinstance(loaded_objects, tuple) else "Not a tuple")
