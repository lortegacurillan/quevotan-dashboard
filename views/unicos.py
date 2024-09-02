import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from back.get_UniqueLabels import check_UniqueLabels, add_ToDataFrame
from back.get_Data import get_Mismatches

df = get_Mismatches()

# Function to show mismatches view
def show_mismatches(df):
    st.title("GPT vs RTM Prediction Mismatches")
     # Display the DataFrame in Streamlit
    st.dataframe(df)

    # Optionally, allow users to download the mismatches as a CSV file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download mismatches as CSV",
        data=csv,
        file_name='mismatches.csv',
        mime='text/csv',
        )
    
    st.write("No mismatches found between GPT and RTM predictions.")

