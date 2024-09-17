import pandas as pd

# Create a function that takes the columns of the dataframe from position 14 to 23 and counts the number of times each label appears in the entire dataframe. The return will be two arrays, the first with the names of the labels and the second with the count of their value
def get_LabelCount(df:pd.DataFrame):
    '''
    This function counts the number of times each label appears in the entire dataframe
    
    Parameters:
    df (pd.DataFrame): The DataFrame with the labels
    
    Returns:
    Tuple: A tuple with two arrays, the first with the names of the labels and the second with the count of their value
    '''
    
    labels = df.iloc[:, 13:23].sum().sort_values(ascending=False)
    label_count = labels.values
    label_names = labels.index
    return label_names, label_count

def get_GPTLabelCount(df:pd.DataFrame):
    labels = df.iloc[:, 2:12].sum().sort_values(ascending=False)
    label_count = labels.values
    label_names = labels.index
    return label_names, label_count

def get_RTMLabelCount(df:pd.DataFrame):
    labels = df.iloc[:, 12:22].sum().sort_values(ascending=False)
    label_count = labels.values
    label_names = labels.index
    return label_names, label_count
