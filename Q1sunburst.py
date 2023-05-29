import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Add an unique identifier column
    df['id'] = range(1, len(df) + 1)

    # Group the dataframe by 'Q1', 'Why_1', 'Q2', 'Why_2' to get counts
    df_counts = df.groupby(['Q1', 'Why_1', 'Q2', 'Why_2', 'id']).size().reset_index(name='counts')

    print("\n=== df_counts ===")
    print(df_counts.head())

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    print("\n=== df_total ===")
    print(df_total)

    # Create DataFrames for 'Q1', 'Why_1', 'Q2', 'Why_2' levels
    df_q1 = df_counts[['Q1', 'id', 'counts']].groupby(['Q1', 'id']).sum().reset_index()
    df_q1.columns = ['id', 'child_id', 'counts']
    df_q1['parent'] = 'Total'

    print("\n=== df_q1 ===")
    print(df_q1.head())

    df_why1 = df_counts[['Q1', 'Why_1', 'id', 'counts']].groupby(['Q1', 'Why_1', 'id']).sum().reset_index()
    df_why1.columns = ['parent', 'id', 'child_id', 'counts']

    print("\n=== df_why1 ===")
    print(df_why1.head())

    df_q2 = df_counts[['Why_1', 'Q2', 'id', 'counts']].groupby(['Why_1', 'Q2', 'id']).sum().reset_index()
    df_q2.columns = ['parent', 'id', 'child_id', 'counts']

    print("\n=== df_q2 ===")
    print(df_q2.head())

    df_why2 = df_counts.copy()
    df_why2.columns = ['Q1', 'Why_1', 'Q2', 'Why_2', 'child_id', 'counts']

    print("\n=== df_why2 ===")
    print(df_why2.head())

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2, df_why2])

    print("\n=== df_sunburst ===")
    print(df_sunburst.head())

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

