import pandas as pd
import plotly.graph_objects as go

def create_sunburst(df):
    # Add 'Total' as the root of your hierarchy
    df['Total'] = 'Total'
    
    # Create an id for each row
    df['id'] = df['Total'].astype(str) + "-" + df['Q1'].astype(str) + "-" + df['Why_1'].astype(str)
    
    # Define the label and parent for each row based on the hierarchy 'Total', 'Q1', 'Why_1'
    df['label'] = df['Q1'].astype(str) + "-" + df['Why_1'].astype(str)
    df['parent'] = df['Total'].astype(str) + "-" + df['Q1'].astype(str)

    fig = go.Figure(go.Sunburst(
        labels=df['label'],  # This will be the text displayed for each section of the chart
        parents=df['parent'],  # This defines the hierarchical structure of the chart
        ids=df['id'],  # This is a unique identifier for each row of your data
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig