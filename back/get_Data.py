import pandas as pd


def get_Data()-> pd.DataFrame:
    df = pd.read_excel('data\CorpusEtiquetado_Sampled.xlsx')
    return df