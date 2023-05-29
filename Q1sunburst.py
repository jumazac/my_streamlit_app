import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Group the dataframe by 'Q1' and 'Why_1' to get counts
    df_counts = df.groupby(['Q1', 'Why_1']).size().reset_index(name='counts')

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    # Create DataFrames for 'Q1' and 'Why_1' levels
    df_q1 = df_counts[['Q1', 'counts']].groupby('Q1').sum().reset_index()
    df_q1.columns = ['id', 'counts']
    df_q1['parent'] = 'Total'

    df_why1 = df_counts.copy()
    df_why1.columns = ['parent', 'id', 'counts']

    # Calculate local and global percentages for 'df_q1' and 'df_why1'
    df_q1['percentage'] = df_q1['counts'] / df_q1['counts'].sum() * 100
    df_q1['global_percentage'] = df_q1['counts'] / df_counts['counts'].sum() * 100

    df_why1['percentage'] = df_why1.groupby('parent')['counts'].apply(lambda x: x / x.sum() * 100)
    df_why1['global_percentage'] = df_why1['counts'] / df_counts['counts'].sum() * 100

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1])

    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['id'],
        labels=df_sunburst['id'], 
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'], 
        branchvalues='total',
        hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> Percentage: %{customdata[0]:.2f}%<br> Global Percentage: %{customdata[1]:.2f}%',
        customdata=df_sunburst[['percentage', 'global_percentage']].values,
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig
