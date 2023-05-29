import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Adding unique identifier
    df.reset_index(inplace=True)

    # Group the dataframe by 'Q1', 'Why_1', 'Q2' and 'Why_2' to get counts
    df_q1 = df.groupby(['index', 'Q1']).size().reset_index(name='counts')
    df_why1 = df.groupby(['index', 'Q1', 'Why_1']).size().reset_index(name='counts')
    df_q2 = df.groupby(['index', 'Q1', 'Why_1', 'Q2']).size().reset_index(name='counts')
    df_why2 = df.groupby(['index', 'Q1', 'Why_1', 'Q2', 'Why_2']).size().reset_index(name='counts')

    # Create unique identifiers based on the index and the labels
    df_q1['id'] = df_q1['index'].astype(str) + "-" + df_q1['Q1']
    df_why1['id'] = df_why1['index'].astype(str) + "-" + df_why1['Why_1']
    df_q2['id'] = df_q2['index'].astype(str) + "-" + df_q2['Q2']
    df_why2['id'] = df_why2['index'].astype(str) + "-" + df_why2['Why_2']

    # Create parent identifiers
    df_q1['parent'] = "Total"
    df_why1['parent'] = df_why1['index'].astype(str) + "-" + df_why1['Q1']
    df_q2['parent'] = df_q2['index'].astype(str) + "-" + df_q2['Why_1']
    df_why2['parent'] = df_why2['index'].astype(str) + "-" + df_why2['Q2']

    # Concatenate all dataframes
    df_sunburst = pd.concat([df_q1, df_why1, df_q2, df_why2], ignore_index=True)

    # Create sunburst
    fig = go.Figure(go.Sunburst(
        labels=df_sunburst['parent'], 
        parents=df_sunburst['id'],
        values=df_sunburst['counts'],
    ))
    
    return fig

