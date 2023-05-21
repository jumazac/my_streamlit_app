import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
df = pd.read_csv("TOTAL1.csv")


df_tree = df['IN EVENT?'].value_counts().reset_index()
df_tree.columns = ['id', 'value']


# Calculate total for percentage calculation
total = df_tree['value'].sum()

# Calculate percentage
df_tree['percentage'] = df_tree['value'] / total * 100

# Create the sunburst chart
fig = px.sunburst(df_tree, path=['id'], values='value',
                  hover_data={'id': True,
                              'value': True,
                              'percentage': ':.2f'},
                  hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{customdata[2]}%')

# Show the chart
st.plotly_chart(fig)

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

