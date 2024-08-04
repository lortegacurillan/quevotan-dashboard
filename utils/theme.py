import streamlit as st

def set_color_scheme(color_scheme):
    colors = {
        "dark": {
            "background": "dark",
        },
        "white": {
            "background": "#FFFFFF",
            "text": "#000000",
            "primary": "#0000FF",
            "secondary": "#008000",
            "accent": "#FFA500",
        },
        "lightgrey": {
            "background": "#D3D3D3",
            "text": "#000000",
            "primary": "#0000FF",
            "secondary": "#008000",
            "accent": "#FFA500",
        },
        "lightblue": {
            "background": "#ADD8E6",
            "text": "#000000",
            "primary": "#0000FF",
            "secondary": "#008000",
            "accent": "#FFA500",
        },
        "lightgreen": {
            "background": "#90EE90",
            "text": "#000000",
            "primary": "#0000FF",
            "secondary": "#008000",
            "accent": "#FFA500",
        },
    }
    if color_scheme != "dark":
        
        scheme = colors.get(color_scheme, colors["white"])
        
        st.markdown(f"""
            <style>
                .main {{
                    background-color: {scheme["background"]};
                    color: {scheme["text"]};
                }}
                .stButton>button {{
                    background-color: {scheme["primary"]};
                    color: {scheme["text"]};
                }}
                .stSelectbox>div>div>div {{
                    background-color: {scheme["secondary"]};
                    color: {scheme["text"]};
                }}
                .stMarkdown, .stHeader, .stTextInput, .stTextArea, .stCheckbox, .stRadio, .stSidebar {{
                    color: {scheme["text"]};
                }}
                .stSlider>.stSliderKnob {{
                    background-color: {scheme["accent"]};
                }}
            </style>
        """, unsafe_allow_html=True)
