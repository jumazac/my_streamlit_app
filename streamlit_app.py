import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
df = pd.read_csv("TOTAL1.csv")


df_tree = df['IN EVENT?'].value_counts().reset_index()
df_tree.columns = ['id', 'value']

# Add a 'total' row to the DataFrame
total = df_tree['value'].sum()
df_tree = df_tree.append({'id': 'total', 'value': total}, ignore_index=True)

# Create the sunburst chart
fig = px.sunburst(df_tree, 
                  path=['id'], 
                  values='value')

# Show the chart
fig.show()

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

