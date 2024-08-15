import pandas as pd
#import la funcion get_Data del archivo get_Data.py
from .get_Data import get_Data


df = get_Data('sampled')


# crea una funcion que toma las columnas del dataframe desde la posicion 14 a la 23 y cuenta la cantidad de veces que aparece cada etiqueta en todo el dataframe el retorno seran dos arreglos , el primero con el nombre de las etiquetas y el segundo con el conteo de su valor
def get_LabelCount(df:pd.DataFrame):
    labels = df.iloc[:, 13:23].sum().sort_values(ascending=False)
    label_count = labels.values
    label_names = labels.index
    return label_names, label_count



