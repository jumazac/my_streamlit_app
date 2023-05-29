import pandas as pd
import plotly.graph_objects as go
import streamlit as st



def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Group the dataframe by 'Q1', 'Why_1', and 'Q2' to get counts
    df_counts = df.groupby(['Q1', 'Why_1', 'Q2']).size().reset_index(name='counts')

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    # Create DataFrames for 'Q1' and 'Why_1' levels
    df_q1 = df_counts[['Q1', 'counts']].groupby('Q1').sum().reset_index()
    df_q1.columns = ['id', 'counts']
    df_q1['parent'] = 'Total'

    df_why1 = df_counts[['Q1', 'Why_1', 'counts']].copy()
    df_why1['id'] = df_why1['Q1'] + '-' + df_why1['Why_1']
    df_why1['parent'] = df_why1['Q1']
    df_why1 = df_why1[['parent', 'id', 'counts']]

    # Prepare the 'Q2' level data:
    df_q2 = df_counts.copy()
    df_q2['id'] = df_counts['Q1'] + "-" + df_counts['Why_1'] + "-" + df_counts['Q2'] 
    df_q2['parent'] = df_counts['Q1'] + "-" + df_counts['Why_1']
    df_q2 = df_q2[['id', 'parent', 'counts']]   

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2])
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






