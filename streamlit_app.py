import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function to build hierarchical dataframe
def build_hierarchical_dataframe(df, levels):
    df_tree = pd.DataFrame(columns=['id', 'parent', 'label', 'value', 'percentage'])

    for i, level in enumerate(levels):
        dfg = df.groupby(levels[:i+1]).size().reset_index(name='value')
        dfg['id'] = dfg[levels[:i+1]].apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
        dfg['label'] = dfg[level].copy().astype(str)
        dfg['parent'] = ''
        if i > 0:
            dfg['parent'] = dfg[levels[:i]].apply(lambda row: ' / '.join(row.values.astype(str)), axis=1)
        dfg['percentage'] = dfg['value'] / df.shape[0] * 100
        df_tree = pd.concat([df_tree, dfg], ignore_index=True, sort=False)

    return df_tree

# Load data
df = pd.read_csv("TOTAL1.csv")

# Define levels, with 'IN EVENT?' as the root
levels = ['LOCATION', 'IN EVENT?']

# Build hierarchical dataframe
df_all_trees = build_hierarchical_dataframe(df, levels)

# Create sunburst
fig = go.Figure(go.Sunburst(
    ids=df_all_trees['id'],
    labels=df_all_trees['label'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{text}%',
    text=df_all_trees['percentage'],
))

# Update layout for the figure
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), hoverlabel=dict(font=dict(size=16)))

# Display the chart in Streamlit
st.plotly_chart(fig)

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

