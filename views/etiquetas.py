import streamlit as st
from back.get_LabelCount import get_LabelCount
from back.get_Graph import get_LabelCountGraph, get_CountGraph, get_CombinationGraph

def show_etiquetas(data):
    st.title("Distribución de Etiquetas y Relaciones")

    # Actualizar datos de etiquetas
    if st.button("Actualizar datos de etiquetas"):
        etiquetas, cantidades = get_LabelCount(data)
    else:
        etiquetas, cantidades = get_LabelCount(data)

    # Crear gráfico de barras
    st.subheader("Distribución de Etiquetas")
    fig = get_LabelCountGraph(etiquetas, cantidades)
    # st.plotly_chart(fig)

    st.subheader("Número de Etiquetas por Texto")
    fig3 = get_CountGraph(data.iloc[:, 13:23])
    # st.plotly_chart(fig3)

    st.subheader("Combinaciones de Etiquetas")
    fig2 = get_CombinationGraph(data.iloc[:, 13:23])
    # st.plotly_chart(fig2)
