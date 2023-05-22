import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1.csv")

# Levels in the hierarchy
levels = ['IN EVENT?', 'LOCATION']

# Add an overall root
df['all'] = 'all'
levels.insert(0, 'all')

# Build the hierarchical dataframe
df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])

for i, level in enumerate(levels[:-1]):
    dfg = df.groupby(levels[i: i + 2]).size().reset_index(name='value')
    dfg.columns = ['parent', 'id', 'value']
    df_tree = df_tree.append(dfg, ignore_index=True)

# Calculate percentage within each group
df_tree['percentage'] = df_tree.groupby('parent')['value'].apply(lambda x: x / x.sum() * 100)

# Exclude 'all' level from visualization
df_tree = df_tree[df_tree['parent'] != 'all']

# Create the sunburst chart
fig = go.Figure(go.Sunburst(
    labels=df_tree['id'],
    parents=df_tree['parent'],
    values=df_tree['value'],
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{text}%',
    text=['{:.2f}%'.format(p) for p in df_tree['percentage']],
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

