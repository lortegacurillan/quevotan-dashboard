import pandas as pd


def get_Data(what:str)-> pd.DataFrame:
    if what == 'Prueba':
        df = pd.read_excel('data/Test_DataWithLabels.xlsx')
    elif what == 'sampled':
        df = pd.read_excel('data/CorpusEtiquetado_Sampled.xlsx')
    return df