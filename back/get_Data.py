import pandas as pd


def get_Data(file_name:str)-> pd.DataFrame:
    '''
    This function reads the data from the file_name and returns a DataFrame

    Parameters:
    file_name (str): The name of the file to read the data from

    Returns:
    pd.DataFrame: The DataFrame with the data from the file
    '''
    if file_name == 'Prueba':
        df = pd.read_excel('data/Test_DataWithLabels.xlsx')
    elif file_name == 'sampled':
        df = pd.read_excel('data/CorpusEtiquetado_Sampled.xlsx')
    return df

def get_Mismatches()-> pd.DataFrame:
    df = pd.read_excel('data/mismatches.xlsx')
    return df