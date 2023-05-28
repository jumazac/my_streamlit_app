import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")

# Create a unique id for each row
print(df.head())


def create_sunburst(df):
    df['id'] = df.index.astype(str) + "-" + df['Q1'].astype(str) + "-" + df['Why_1'].astype(str) + "-" + df['Q2'].astype(str) + "-" + df['Why_2'].astype(str)

    df['Why_1'].fillna('N/A', inplace=True)
    df['Why_2'].fillna('N/A', inplace=True)
    
    fig = go.Figure(go.Sunburst(
        labels=df['Why_2'], 
        parents=df['Why_1'],
        ids=df['id'],
        hovertext=df['Why_2'],
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

sunburst_chart = create_sunburst(df)

st.plotly_chart(sunburst_chart)
