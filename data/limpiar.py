import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel('data\Test_DataWithLabels.xlsx')

# Eliminar el prefijo '_x000D_\n' de la primera columna
# Asegúrate de que 'Columna1' es el nombre de la primera columna o usa df.iloc[:, 0] para seleccionar por índice
df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: x.strip('_x000D_\n                                ') if isinstance(x, str) else x)

# Guardar el dataframe modificado de vuelta a Excel
df.to_excel('data\Test_DataWithLabels.xlsx', index=False)