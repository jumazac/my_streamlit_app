import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Add 'Total' as the root of your hierarchy
    df['Total'] = 'Total'
    
    # Create a unique id for each row
    df['id'] = df['Total'] + "-" + df['Q1'] + "-" + df['Why_1'] + "-" + df['Q2'] + "-" + df['Why_2']

    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df['id'],
        labels=df['Q1'], 
        parents=df['Total'],
        values=df['id'].count(), # or another column depending on what you want to display
        branchvalues='total',
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig
