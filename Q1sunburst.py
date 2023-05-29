import pandas as pd
import plotly.graph_objects as go
import streamlit as st



def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Create the combined ID columns
    df['id_q1'] = df['Q1']
    df['id_why1'] = df['Q1'] + "-" + df['Why_1']
    df['id_q2'] = df['Q1'] + "-" + df['Why_1'] + "-" + df['Q2']

    # Group the dataframe by combined IDs to get counts
    df_counts_q1 = df.groupby(['id_q1']).size().reset_index(name='counts')
    df_counts_why1 = df.groupby(['id_why1']).size().reset_index(name='counts')
    df_counts_q2 = df.groupby(['id_q2']).size().reset_index(name='counts')

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    # Create DataFrames for each level
    df_q1 = df_counts_q1.copy()
    df_q1['parent'] = 'Total'
    df_q1.columns = ['id', 'counts', 'parent']

    df_why1 = df_counts_why1.copy()
    df_why1['parent'] = df_why1['id_why1'].apply(lambda x: x.split("-")[0])
    df_why1.columns = ['id', 'counts', 'parent']

    df_q2 = df_counts_q2.copy()
    df_q2['parent'] = df_q2['id_q2'].apply(lambda x: "-".join(x.split("-")[:-1]))
    df_q2.columns = ['id', 'counts', 'parent']

    df_why2 = df_counts_why2.copy()
    df_why2['parent'] = df_why2['id_why2'].apply(lambda x: "-".join(x.split("-")[:-1]))
    df_why2.columns = ['id', 'counts', 'parent']

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2, df_why2])
    print(df_sunburst)  # print statement to check the DataFrame

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