import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")




def create_sunburst(df):
    df['id'] = df.index.astype(str) + "-" + df['Q1'].astype(str)

    fig = go.Figure(go.Sunburst(
        labels=df['Q1'],  # Labels are Q1 values
        parents=[""] * len(df),  # Parents are empty, as Q1 is the top level
        ids=df['id'],  # ids are the unique identifiers we created
        hovertext=df['Q1'],
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

sunburst_chart = create_sunburst(df)

st.plotly_chart(sunburst_chart)
