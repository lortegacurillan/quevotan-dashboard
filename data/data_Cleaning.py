import pandas as pd
from back.get_Data import get_Data

# Cargar el archivo Excel
df = get_Data('Prueba')

# Eliminar el prefijo '_x000D_\n' de la primera columna
# Asegúrate de que 'Columna1' es el nombre de la primera columna o usa df.iloc[:, 0] para seleccionar por índice
df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: x.strip('_x000D_\n                                ') if isinstance(x, str) else x)

# Guardar el dataframe modificado de vuelta a Excel
df.to_excel('data\test_data_with_labels.xlsx', index=False)