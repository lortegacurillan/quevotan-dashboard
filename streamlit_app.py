# streamlit_app.py
import sys
import os
import streamlit as st
import pandas as pd
from back.get_Data import get_Data
from utils.theme import set_color_scheme

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import views
from views.view_About import show_About
from views.view_LabelsMetrics import show_Labels
from views.view_UniqueQuery import get_UniqueQuery
from views.view_TestData import show_TestData
from views.view_Mismatches import show_mismatches
from views.view_UserLabeling import show_UserLabeling
from views.view_UserModelRanking import show_UserModelRanking

# Configuration
RANKING_MODE = True  # Toggle for ranking-only mode

# App configuration
st.set_page_config(
    page_title='¿Que Votan? dashboard',
    page_icon=':earth_americas:', 
    layout="wide",
)

# CSS styling
st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding: 1rem 2rem;
        }
        .css-1lcbmhc {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# Data loading
@st.cache_data
def load_data():
    return {
        'main': get_Data('corpus_etiquetado_sampled'),
        'mismatches': get_Data('expanded_mismatches'),
        'predictions': get_Data('gpt_rtm_comparison'),
        'softmax': get_Data('vote_ranking_softmax')
    }

data = load_data()

# View configurations
VIEWS = {
    'ranking_only': {
        'options': ['Ranking'],
        'default': 'Ranking',
        'show_sidebar': False
    },
    'full': {
        'options': ["About", "Etiquetas", "Consulta", "Pruebas", "Comparativa", "Formulario", "Ranking"],
        'default': "About",
        'show_sidebar': True
    }
}

def render_sidebar(view_config):
    """Render sidebar based on configuration"""
    if view_config['show_sidebar']:
        st.sidebar.image("src/quevotan.jpg", use_column_width=True)
        st.sidebar.title("Menú")
        return st.sidebar.selectbox("Selecciona una vista:", view_config['options'])
    return view_config['default']

def render_view(selected_view):
    """Render the selected view"""
    view_map = {
        "About": lambda: show_About(),
        "Etiquetas": lambda: show_Labels(data['main']),
        "Consulta": lambda: get_UniqueQuery(data['main'], get_Data),
        "Pruebas": lambda: show_TestData(get_Data),
        "Comparativa": lambda: show_mismatches(data['main'], data['mismatches']),
        "Formulario": lambda: show_UserLabeling(data['main']),
        "Ranking": lambda: show_UserModelRanking(data['mismatches'], data['softmax'])
    }
    
    view_map[selected_view]()

def main():
    # Select view configuration based on mode
    view_config = VIEWS['ranking_only'] if RANKING_MODE else VIEWS['full']
    
    # Get selected view
    selected_view = render_sidebar(view_config)
    
    # Render selected view
    render_view(selected_view)

if __name__ == "__main__":
    main()