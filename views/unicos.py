import pandas as pd
import streamlit as st
import plotly.express as px
from back.get_LabelCount import get_LabelCount, get_GPTLabelCount, get_RTMLabelCount

# Function to create the comparison bar graph
def get_ComparisonGraph(total_labels, gpt_mismatches, rtm_mismatches):
    # Create a DataFrame for plotting
    comparison_df = pd.DataFrame({
        'Label': ['Total Labels', 'GPT Mismatches', 'RTM Mismatches'],
        'Count': [total_labels, gpt_mismatches, rtm_mismatches]
    })

    # Create the bar chart using Plotly Express
    fig = px.bar(comparison_df, x='Label', y='Count', 
                 title='Comparación de Etiquetas: Total vs GPT y RTM Desajustes',
                 labels={'Count': 'Cantidad de Etiquetas', 'Label': 'Categoría'})

    return fig

# Main mismatches view function
def show_mismatches(data, df):
    st.title("Comparación de Predicciones GPT vs. Desajustes en RTM")

    # Use the get_LabelCount function to get total label counts from the main DataFrame (data)
    label_names_total, total_label_counts = get_LabelCount(data)
    total_labels = total_label_counts.sum()  # Sum the total labels in the original data

    # Use the get_GPTLabelCount function to get GPT mismatched label counts
    label_names_gpt, gpt_label_counts = get_GPTLabelCount(df)
    gpt_mismatches = gpt_label_counts.sum()  # Sum the mismatched GPT labels

    # Use the get_RTMLabelCount function to get RTM mismatched label counts
    label_names_rtm, rtm_label_counts = get_RTMLabelCount(df)
    rtm_mismatches = rtm_label_counts.sum()  # Sum the mismatched RTM labels

    # Display the bar chart comparing total labels vs GPT and RTM mismatches
    st.subheader("Comparación entre Etiquetas Totales, GPT y RTM Desajustes")
    fig = get_ComparisonGraph(total_labels, gpt_mismatches, rtm_mismatches)
    st.plotly_chart(fig)

    # Optionally, allow users to download the mismatches as a CSV file
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download mismatches as CSV",
        data=csv,
        file_name='mismatches.csv',
        mime='text/csv',
    )

# Example call in your Streamlit app:
# show_mismatches(data, mismatch_Data)
