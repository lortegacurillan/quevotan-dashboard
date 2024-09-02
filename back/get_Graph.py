import pandas as pd
import streamlit as st
import plotly.express as px

def get_CombinationGraph(data:pd.DataFrame):
    '''
    Display a bar chart with the combination of labels in the data

    Parameters:
    data (pd.DataFrame): The DataFrame with the labels

    Returns:
    None
    '''
    if not data.empty:
        # Process the combination of labels
        colum_label = data.columns
        colum_name = [col.replace('Etiqueta ', '') for col in colum_label]
        data_comb = data[colum_label].apply(lambda x: ','.join([colum_name[i] for i in range(len(x)) if x.iloc[i] == 1]), axis=1)
        combination = data_comb.value_counts().sort_values(ascending=False)

        #create a bar chart for the combination of labels
        fig = px.bar(combination, x=combination.index, y=combination.values, title='combination de Etiquetas')
        fig.update_xaxes(title='combination', tickangle=45)
        fig.update_yaxes(title='Cantidad')
        fig.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_tickangle=-45)

        #Configurar zoom inicial y scroll horizontal
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="category"
            ),
            xaxis_range=[0, 10],  #Initial Zoom for the first 10 elements 
            height=600,
            margin=dict(l=40, r=40, t=40, b=40),
        )

        st.plotly_chart(fig)
    else:
        st.warning("No se pudo obtener el dataframe.")

def get_CountGraph(data:pd.DataFrame):
    '''
    Display a bar chart with the number of labels in the data

    Parameters:
    data (pd.DataFrame): The DataFrame with the labels

    Returns:
    None
    '''

    #create a bar chart that shows how many texts have n labels
    label_qty = data.sum(axis=1)
    label_count = label_qty.value_counts().sort_index()

    # Crear gráfico de barras
    fig = px.bar(x=label_count.index, y=label_count.values, title='Cantidad de Textos por Número de Etiquetas')
    fig.update_xaxes(title='Número de Etiquetas')
    fig.update_yaxes(title='Cantidad de Textos')

    st.plotly_chart(fig)

def get_LabelCountGraph(labels, counts):
    '''
    Display a bar chart with the labels and their counts

    Parameters:
    labels (list): The list of labels
    counts (list): The list of counts

    Returns:
    None
    '''
    # Ordenar datos por cantidad
    sorted_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)
    etiquetas_sorted = [labels[i] for i in sorted_indices]
    cantidades_sorted = [counts[i] for i in sorted_indices]

    # Crear gráfico de barras con Streamlit y Plotly
    fig = px.bar(x=etiquetas_sorted, y=cantidades_sorted, title='Conteo de Etiquetas')
    fig.update_xaxes(title='Etiquetas', categoryorder='total descending')
    fig.update_yaxes(title='Cantidad')

    st.plotly_chart(fig)