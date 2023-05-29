import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Group the dataframe by 'Q1' and 'Why_1' to get counts
    df_counts = df.groupby(['Q1', 'Why_1']).size().reset_index(name='counts')

    # Calculate global count
    total_count = df.shape[0]
    
    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [total_count], "percentage": [100]})

    # Create DataFrames for 'Q1' and 'Why_1' levels
    df_q1 = df_counts[['Q1', 'counts']].groupby('Q1').sum().reset_index()
    df_q1.columns = ['id', 'counts']
    df_q1['parent'] = 'Total'
    df_q1['percentage'] = df_q1['counts'] / total_count * 100

    df_why1 = df_counts.copy()
    df_why1.columns = ['parent', 'id', 'counts']
    df_why1['percentage'] = df_why1.groupby('parent')['counts'].apply(lambda x: x / x.sum() * 100)

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1])

    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['id'],
        labels=df_sunburst['id'], 
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'],
        branchvalues='total',
        hovertext=df_sunburst.apply(lambda row: f"{row['id']}<br>Percentage: {row['percentage']:.2f}%", axis=1),
        hoverinfo='text'
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig
