import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Group the dataframe by 'Q1', 'Why_1', 'Q2', 'Why_2' to get counts
    df_counts = df.groupby(['Q1', 'Why_1', 'Q2', 'Why_2']).size().reset_index(name='counts')

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})
    print(df_total)

    # Create DataFrames for 'Q1', 'Why_1', 'Q2', 'Why_2' levels
    df_q1 = df_counts[['Q1', 'counts']].groupby('Q1').sum().reset_index()
    df_q1.columns = ['id', 'counts']
    df_q1['parent'] = 'Total'
    print(df_q1)

    df_why1 = df_counts[['Q1', 'Why_1', 'counts']].groupby(['Q1', 'Why_1']).sum().reset_index()
    df_why1.columns = ['parent', 'id', 'counts']
    print(df_why1)

    df_q2 = df_counts[['Q1', 'Why_1', 'Q2', 'counts']].groupby(['Q1', 'Why_1', 'Q2']).sum().reset_index()
    df_q2.columns = ['parent_1', 'parent_2', 'id', 'counts']
    df_q2['parent'] = df_q2['parent_1'] + ' - ' + df_q2['parent_2']
    df_q2.drop(['parent_1', 'parent_2'], axis=1, inplace=True)
    print(df_q2)

    df_why2 = df_counts[['Q1', 'Why_1', 'Q2', 'Why_2', 'counts']].copy()
    df_why2.columns = ['parent_1', 'parent_2', 'parent_3', 'id', 'counts']
    df_why2['parent'] = df_why2['parent_1'] + ' - ' + df_why2['parent_2'] + ' - ' + df_why2['parent_3']
    df_why2.drop(['parent_1', 'parent_2', 'parent_3'], axis=1, inplace=True)
    print(df_why2)

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2, df_why2])
    print(df_sunburst)

    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['id'],
        labels=df_sunburst['id'], 
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'], 
        branchvalues='total',
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig

