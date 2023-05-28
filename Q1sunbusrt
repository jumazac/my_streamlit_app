import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data 
df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")

# Print the first 5 rows of the DataFrame
print(df[['Q1', 'Why_1', 'Q2', 'Why_2']].head())

def create_sunburst(df):
    fig = go.Figure(go.Sunburst(
        labels=df['Why_2'], 
        parents=df['Why_1'],
        ids=df['Q2'],
        hovertext=df['Why_2'],
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

sunburst_chart = create_sunburst(df)

# Print some properties of the sunburst chart
print("Labels in the sunburst chart: ", sunburst_chart['data'][0]['labels'][:10])
print("Parents in the sunburst chart: ", sunburst_chart['data'][0]['parents'][:10])
print("IDs in the sunburst chart: ", sunburst_chart['data'][0]['ids'][:10])

# Display the new sunburst chart in Streamlit
st.plotly_chart(sunburst_chart)
