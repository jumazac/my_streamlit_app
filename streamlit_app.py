import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1.csv")

# Generate counts for 'IN EVENT?'
df_tree = df['IN EVENT?'].value_counts().reset_index()
df_tree.columns = ['id', 'value']

# Calculate total for percentage calculation
total = df_tree['value'].sum()

# Calculate percentage
df_tree['percentage'] = df_tree['value'] / total * 100

# Create the sunburst chart
fig = go.Figure(go.Sunburst(
    labels=df_tree['id'],
    parents=['' for _ in df_tree['id']],
    values=df_tree['value'],
    hovertext=['{:.2f}%'.format(p) for p in df_tree['percentage']],
    hoverinfo="label+text+value"
))

# Update layout for the figure
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

# Display the chart in Streamlit
st.plotly_chart(fig)

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

