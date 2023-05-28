import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")




def create_sunburst(df):
    # Group the dataframe by 'Q1' and count the number of each unique value
    grouped_df = df.groupby('Q1').size().reset_index(name='counts')

    # Compute total count to calculate the global percentage
    total_counts = grouped_df['counts'].sum()

     # Compute global_percentage and percentage for each group
    grouped_df['global_percentage'] = (grouped_df['counts'] / total_counts) * 100
    grouped_df['percentage'] = (grouped_df['counts'] / grouped_df['counts'].sum()) * 100





    fig = go.Figure(go.Sunburst(
        labels=grouped_df['Q1'],  # Labels are unique 'Q1' values
        parents=[""] * len(grouped_df),  # Parents are empty, as 'Q1' is the top level
        values=grouped_df['counts'],  # The size of each slice is determined by the count of each unique value in 'Q1'
        hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}',
        customdata=list(zip(grouped_df.percentage, grouped_df.global_percentage)),  # Include both 'percentage' and 'global_percentage'
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

sunburst_chart = create_sunburst(df)

st.plotly_chart(sunburst_chart)
