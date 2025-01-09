from pymongo import MongoClient
from load_Model import load_model  

# Conexion a MongoDB (Local)
client = MongoClient("mongodb://localhost:27017/")
db = client["quevotan"]  
votaciones_collection = db["votaciones"]
etiquetas_index_collection = db["EtiquetasIndex"]

# Cargar el modelo, vectorizador y escalador
modelo_path = "RandomForestModel/multi_target_forest.pkl"
modelo_rf, vectorizador_tfidf, escalador = load_model(modelo_path)

if modelo_rf is None or vectorizador_tfidf is None or escalador is None:
    print("Error al cargar el modelo. Verifica el archivo y el código.")
    exit()

# Obtener las etiquetas de la coleccion EtiquetasIndex
etiquetas_index = list(etiquetas_index_collection.find())
etiquetas_map = {i["id"]: i["etiqueta"] for i in etiquetas_index} 

def etiquetar_votacion(texto):
    texto_vectorizado = vectorizador_tfidf.transform([texto])
    texto_escalado = escalador.transform(texto_vectorizado.toarray())
    
    # Predicciones del modelo (arreglo binario)
    etiquetas_predichas = modelo_rf.predict(texto_escalado)[0]
    
    # Mapear indices predichos (1) a IDs de EtiquetasIndex
    etiquetas_aplicadas = [
        etiquetas_index[i]["id"]
        for i, prediccion in enumerate(etiquetas_predichas)
        if prediccion == 1
    ]
    return etiquetas_aplicadas


# Procesar los documentos en la coleccion votaciones
contador_etiquetados = 0 
for votacion in votaciones_collection.find(): 
    nombre = votacion.get("nombre", "")  
    
    etiquetas_aplicadas = etiquetar_votacion(nombre)
    
    votaciones_collection.update_one(
        {"_id": votacion["_id"]},
        {"$set": {"etiquetas": etiquetas_aplicadas}}
    )
    contador_etiquetados += 1  

# Mostrar la cantidad de documentos etiquetados
print(f"Etiquetado completado. Se etiquetaron {contador_etiquetados} documentos con IDs de EtiquetasIndex.")
