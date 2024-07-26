import pandas as pd
import streamlit as st
import plotly.express as px

def get_CombinationGraph(data):
    if not data.empty:
        # Procesar combinaciones de etiquetas
        etiqueta_columns = data.columns 
        etiqueta_names = [col.replace('Etiqueta ', '') for col in etiqueta_columns]
        data_comb = data[etiqueta_columns].apply(lambda x: ','.join([etiqueta_names[i] for i in range(len(x)) if x.iloc[i] == 1]), axis=1)
        combinaciones = data_comb.value_counts().sort_values(ascending=False)
        
        # Crear gráfico de barras para combinaciones de etiquetas
        fig = px.bar(combinaciones, x=combinaciones.index, y=combinaciones.values, title='Combinaciones de Etiquetas')
        fig.update_xaxes(title='Combinaciones', tickangle=45)
        fig.update_yaxes(title='Cantidad')
        fig.update_layout(xaxis={'categoryorder':'total descending'}, xaxis_tickangle=-45)
        
        # Configurar zoom inicial y scroll horizontal
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="category"
            ),
            xaxis_range=[0, 10],  # Zoom inicial para mostrar los primeros 10 elementos
            height=600,
            margin=dict(l=40, r=40, t=40, b=40),
        )
        
        st.plotly_chart(fig)
    else:
        st.warning("No se pudo obtener el dataframe.")

def get_CountGraph(data):
    # Crear un gráfico que muestre cuántos textos hay con n etiquetas
    num_etiquetas = data.sum(axis=1)
    etiquetas_counts = num_etiquetas.value_counts().sort_index()
    
    # Crear gráfico de barras
    fig = px.bar(x=etiquetas_counts.index, y=etiquetas_counts.values, title='Cantidad de Textos por Número de Etiquetas')
    fig.update_xaxes(title='Número de Etiquetas')
    fig.update_yaxes(title='Cantidad de Textos')
    
    st.plotly_chart(fig)

def get_LabelCountGraph(labels, counts):
    # Ordenar datos por cantidad
    sorted_indices = sorted(range(len(counts)), key=lambda i: counts[i], reverse=True)
    etiquetas_sorted = [labels[i] for i in sorted_indices]
    cantidades_sorted = [counts[i] for i in sorted_indices]
    
    # Crear gráfico de barras con Streamlit y Plotly
    fig = px.bar(x=etiquetas_sorted, y=cantidades_sorted, title='Conteo de Etiquetas')
    fig.update_xaxes(title='Etiquetas', categoryorder='total descending')
    fig.update_yaxes(title='Cantidad')
    
    st.plotly_chart(fig)