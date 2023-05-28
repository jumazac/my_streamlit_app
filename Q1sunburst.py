import streamlit as st
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

# Fill NaN values
df = df.fillna("N/A")




def create_sunburst(df):
    # Group the dataframe by 'Q1' and 'Why_1', and count the number of each unique pair
    grouped_df = df.groupby(['Q1', 'Why_1']).size().reset_index(name='counts')

    # Create a unique id for each 'Q1'-'Why_1' pair in the grouped DataFrame
    grouped_df['id'] = grouped_df['Q1'].astype(str) + "-" + grouped_df['Why_1'].astype(str)

    # Compute total count to calculate the global percentage
    total_counts = grouped_df['counts'].sum()

    # Compute global_percentage and percentage for each group
    grouped_df['global_percentage'] = (grouped_df['counts'] / total_counts) * 100
    grouped_df['percentage'] = (grouped_df['counts'] / grouped_df['counts'].sum()) * 100

    fig = go.Figure(go.Sunburst(
        ids=grouped_df['id'],
        labels=grouped_df['Why_1'],
        parents=grouped_df['Q1'],
        values=grouped_df['counts'],
        hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}',
        customdata=list(zip(grouped_df.percentage, grouped_df.global_percentage)),
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    return fig
sunburst_chart = create_sunburst(df)



test_df = pd.DataFrame({
    'id': ['Yes-Reason1', 'Yes-Reason2', 'No-Reason1', 'No-Reason2'],
    'Q1': ['Yes', 'Yes', 'No', 'No'],
    'Why_1': ['Reason1', 'Reason2', 'Reason1', 'Reason2'],
    'counts': [100, 200, 150, 250],
    'global_percentage': [20, 40, 30, 60],
    'percentage': [20, 40, 30, 60]
})

fig = go.Figure(go.Sunburst(
    ids=test_df['id'],
    labels=test_df['Why_1'],
    parents=test_df['Q1'],
    values=test_df['counts'],
    hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}',
    customdata=list(zip(test_df.percentage, test_df.global_percentage)),
))
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

st.plotly_chart(fig)