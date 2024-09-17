import pandas as pd
import streamlit as st
import plotly.express as px
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

