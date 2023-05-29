import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def create_sunburst(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)
    df['unique_id'] = df['Q1'] + '-' + df['Why_1'] + '-' + df['Q2'] + '-' + df['Why_2'] + '-' + df.index.astype(str)

    # Total level
    df_total = pd.DataFrame({'id': ['Total'], 'counts': [df.shape[0]]})
    df_total['parent'] = ''
    df_total['unique_id'] = 'Total'

    # Q1 level
    df_q1 = df.groupby('Q1').size().reset_index(name='counts')
    df_q1['parent'] = 'Total'
    df_q1['unique_id'] = df_q1['Q1']

    # Why_1 level
    df_why1 = df.groupby(['Q1', 'Why_1']).size().reset_index(name='counts')
    df_why1['parent'] = df_why1['Q1']
    df_why1['unique_id'] = df_why1['Q1'] + '-' + df_why1['Why_1']

    # Q2 level
    df_q2 = df.groupby(['Q1', 'Why_1', 'Q2']).size().reset_index(name='counts')
    df_q2['parent'] = df_q2['Q1'] + '-' + df_q2['Why_1']
    df_q2['unique_id'] = df_q2['Q1'] + '-' + df_q2['Why_1'] + '-' + df_q2['Q2']

    # Why_2 level
    df_why2 = df.groupby(['Q1', 'Why_1', 'Q2', 'Why_2']).size().reset_index(name='counts')
    df_why2['parent'] = df_why2['Q1'] + '-' + df_why2['Why_1'] + '-' + df_why2['Q2']
    df_why2['unique_id'] = df_why2['Q1'] + '-' + df_why2['Why_1'] + '-' + df_why2['Q2'] + '-' + df_why2['Why_2']

    # Combine all levels
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2, df_why2], ignore_index=True)

    fig = go.Figure(go.Sunburst(
    ids=df_sunburst['id'],
    labels=df_sunburst['id'],
    parents=df_sunburst['parent'],
    values=df_sunburst['counts'],
))
    return fig

