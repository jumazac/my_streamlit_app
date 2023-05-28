import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")




def create_sunburst(df):
    # Create a unique id for each row
    df['id'] = df.index.astype(str) + "-" + df['Q1'].astype(str) + "-" + df['Why_1'].astype(str) + "-" + df['Q2'].astype(str) + "-" + df['Why_2'].astype(str)
    
    print(df)


# Define the label and parent for each row based on the hierarchy 'Q1', 'Why_1', 'Q2', 'Why_2'
    df['label'] = df['Q1'] + " " + df['Why_1'] + " " + df['Q2'] + " " + df['Why_2']
    df['parent'] = df['Q1'] + " " + df['Why_1'] + " " + df['Q2']
    fig = go.Figure(go.Sunburst(
        labels=df['Why_2'],  # This should be a column with the names for each of the individual sections of the chart
        parents=df['Why_1'],  # This should be a column with the names for the parent category of each section
        ids=df['id'],  # This should be a column with unique identifiers for each section
        hovertext=df['Why_2'],
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

sunburst_chart = create_sunburst(df)

st.plotly_chart(sunburst_chart)
