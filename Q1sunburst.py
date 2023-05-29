import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    df = df.copy()
    # Create an id for each row
    df['id'] = df.index.astype(str) + "-" + df['Q1'].astype(str) + "-" + df['Why_1'].astype(str)

    # Define the label and parent for each row based on the hierarchy 'Q1', 'Why_1', 'Q2', 'Why_2'
    df['label'] = df['Q1'] + "-" + df['Why_1']
    df['parent'] = df['Q1']

    # Create the root node
    total_row = pd.DataFrame({"id": "Total", "label": "Total", "parent": ""}, index=[0])
    df = pd.concat([total_row, df])

    fig = go.Figure(go.Sunburst(
        labels=df['label'],  # This will be the text displayed for each section of the chart
        parents=df['parent'],  # This defines the hierarchical structure of the chart
        ids=df['id'],  # This is a unique identifier for each row of your data
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    
    return fig
