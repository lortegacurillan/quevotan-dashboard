import pandas as pd
import streamlit as st
import plotly.express as px
from collections import defaultdict
from back.get_LabelCount import get_RTMLabelCount
from back.get_Graph import get_LabelCountGraph, get_ComparisonGraph

def show_mismatches(data: pd.DataFrame, mismatches_df: pd.DataFrame):
    st.title("Comparativa de Predicciones RTM vs. GPT-3.5")

    # Display label distribution
    etiquetas, cantidades = get_RTMLabelCount(mismatches_df)
    st.subheader("Distribución de Etiquetas que no coincidieron con las predicciones de GPT-3.5")
    get_LabelCountGraph(etiquetas, cantidades)

    # Display comparison graph
    st.subheader("Votos cuyas predicciones modeladas no coincidieron (RTM vs. GPT-3.5)")
    get_ComparisonGraph(data, mismatches_df)

    st.subheader("Detalle de los desajustes entre RTM y GPT-3.5")
    if mismatches_df is not None and not mismatches_df.empty:
        st.dataframe(mismatches_df, use_container_width=True)
    else:
        st.warning("No hay desajustes para mostrar.")

    # Download mismatches as CSV
    csv = mismatches_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar desajustes como CSV",
        data=csv,
        file_name='desajustes.csv',
        mime='text/csv',
    )

    # Calculate and display failure metrics
    st.subheader("Métricas de Fallo para las Etiquetas")
    aciertos = defaultdict(int)
    fallos = defaultdict(int)

    # Iterate over each row to calculate hits and misses
    for _, row in mismatches_df.iterrows():
        for column in mismatches_df.columns:
            if column.startswith('RTM_') or column.startswith('GPT_'):
                etiqueta = column.split('_', 1)[1]  # Get the label without the prefix
                if row[column] == 1:  # If it is 1, it means the label was marked
                    if column.startswith('RTM_') and row[column] == row[f'GPT_{etiqueta}']:
                        aciertos[etiqueta] += 1
                    elif column.startswith('RTM_') and row[column] != row[f'GPT_{etiqueta}']:
                        fallos[etiqueta] += 1

    # Create DataFrame for frequency analysis
    etiquetas = list(aciertos.keys())
    frecuencias_df = pd.DataFrame({
        'Etiqueta': etiquetas,
        'Aciertos': [aciertos[etiqueta] for etiqueta in etiquetas],
        'Fallos': [fallos[etiqueta] for etiqueta in etiquetas],
    })

    # Calculate failure percentage
    frecuencias_df['Porcentaje_Fallos'] = (frecuencias_df['Fallos'] / (frecuencias_df['Aciertos'] + frecuencias_df['Fallos'])) * 100

    # Display frequency table
    st.subheader("Tabla de Frecuencias de Fallos por Etiqueta")
    st.dataframe(frecuencias_df, use_container_width=True)

    # Text summaries
    etiqueta_mas_fallos = frecuencias_df.sort_values(by='Porcentaje_Fallos', ascending=False).iloc[0]
    etiqueta_mas_precisa = frecuencias_df.sort_values(by='Porcentaje_Fallos').iloc[0]

    resumen_fallos = f"La etiqueta con más errores en proporción a sus aciertos es '{etiqueta_mas_fallos['Etiqueta']}' con un porcentaje de fallos de {etiqueta_mas_fallos['Porcentaje_Fallos']:.2f}%."
    resumen_precision = f"La etiqueta con mayor precisión es '{etiqueta_mas_precisa['Etiqueta']}' con un porcentaje de fallos de {etiqueta_mas_precisa['Porcentaje_Fallos']:.2f}%."

    st.subheader("Resumen de Métricas")
    st.write(resumen_fallos)
    st.write(resumen_precision)

