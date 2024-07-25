import matplotlib.pyplot as plt
import pandas as pd


def get_CombinationGraph(combinaciones:int, ):
    ax = plt.subplots(figsize=(10, 6))
    combinaciones.plot(kind='bar', ax=ax)
    ax.set_xlabel('Combinaciones de Etiquetas')
    ax.set_ylabel('Cantidad')
    ax.set_title('Combinaciones de Etiquetas')
    plt.xticks(rotation=45)
    return plt

def get_CountGraph(data,num_etiquetas:int, ):
    ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data.index, num_etiquetas, alpha=0.7)
    ax.set_xlabel('Índice del Texto')
    ax.set_ylabel('Número de Etiquetas')
    ax.set_title('Número de Etiquetas por Texto')
    return plt

def get_LabelCountGraph(labels, counts):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, counts)
    ax.set_xlabel('Etiquetas')
    ax.set_ylabel('Cantidad')
    ax.set_title('Distribución de Etiquetas')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    return fig  

