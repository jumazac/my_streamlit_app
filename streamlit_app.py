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
df_tree['parent'] = ''

# Generate counts for 'LOCATION' grouped by 'IN EVENT?'
df_tree2 = df.groupby(['IN EVENT?', 'LOCATION']).size().reset_index(name='value')
df_tree2['id'] = df_tree2['LOCATION']
df_tree2['parent'] = df_tree2['IN EVENT?']

# Calculate percentage within each group and reset index
df_tree2['percentage'] = df_tree2.groupby('IN EVENT?')['value'].apply(lambda x: x / x.sum() * 100).reset_index(drop=True)

# Concatenate dataframes
df_sunburst = pd.concat([df_tree, df_tree2], ignore_index=True)

# Create the sunburst chart
fig = go.Figure(go.Sunburst(
    labels=df_sunburst['id'],
    parents=df_sunburst['parent'],
    values=df_sunburst['value'],
    hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{text}%',
    text=['{:.2f}%'.format(p) for p in df_sunburst['percentage']],
))

# Update layout for the figure
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                  hoverlabel=dict(font=dict(size=16)))

# Display the chart in Streamlit
st.plotly_chart(fig)

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

