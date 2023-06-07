import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def create_sunburst_chartQs(df):
    # Preprocessing steps
    df = df.copy()
    df.fillna("N/A", inplace=True)

    # Convert 'USE_SPIN?' to lowercase
    df['USE_SPIN?'] = df['USE_SPIN?'].str.lower()

    # Create the combined ID columns
    df['id_q1'] = df['Q1']
    df['id_why1'] = df['Q1'] + "-" + df['Why_1']
    df['id_q2'] = df['Q1'] + "-" + df['Why_1'] + "-" + df['Q2']
    df['id_why2'] = df['Q1'] + "-" + df['Why_1'] + "-" + df['Q2'] + "-" + df['Why_2']

    # Group the dataframe by combined IDs to get counts
    df_counts_q1 = df.groupby(['id_q1']).size().reset_index(name='counts')
    df_counts_why1 = df.groupby(['id_why1']).size().reset_index(name='counts')
    df_counts_q2 = df.groupby(['id_q2']).size().reset_index(name='counts')
    df_counts_why2 = df.groupby(['id_why2']).size().reset_index(name='counts')  # corrected here

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    df_q1 = df_counts_q1.copy()
    df_q1.columns = ['id', 'counts'] 
    df_q1['labels'] = df_q1['id'].apply(lambda x: x.split("-")[-1])
    df_q1['parent'] = 'Total'

    df_why1 = df_counts_why1.copy()
    df_why1.columns = ['id', 'counts']  
    df_why1['labels'] = df_why1['id'].apply(lambda x: x.split("-")[-1])
    df_why1['parent'] = df_why1['id'].apply(lambda x: x.split("-")[0])

    df_q2 = df_counts_q2.copy()
    df_q2.columns = ['id', 'counts']
    df_q2['labels'] = df_q2['id'].apply(lambda x: x.split("-")[-1])
    df_q2['parent'] = df_q2['id'].apply(lambda x: "-".join(x.split("-")[:-1]))

    df_why2 = df_counts_why2.copy()
    df_why2.columns = ['id', 'counts'] 
    df_why2['labels'] = df_why2['id'].apply(lambda x: x.split("-")[-1])
    df_why2['parent'] = df_why2['id'].apply(lambda x: "-".join(x.split("-")[:-1]))

    
# Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_q1, df_why1, df_q2, df_why2]).reset_index(drop=True)  # Reset index

    # Calculate the local and global percentages
    total_count = df_sunburst['counts'].sum()

    df_sunburst['local_percent'] = df_sunburst.groupby('parent', group_keys=False)['counts'].apply(lambda x: x / x.sum() * 100)
    df_sunburst['global_percent'] = df_sunburst['counts'] / total_count * 100
    df_sunburst['hoverinfo'] = df_sunburst['labels'].astype(str) + '<br>Local: ' + df_sunburst['local_percent'].round(2).astype(str) + '%' + '<br>Global: ' + df_sunburst['global_percent'].round(2).astype(str) + '%'


    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['id'],
        labels=df_sunburst['labels'], 
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'], 
        hovertext=df_sunburst['hoverinfo'],  # using hoverinfo for hover text
        branchvalues='total',
        maxdepth=3,
        
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    # Create and display the legend table

    legend = """
| Color | NO | Color | MAYBE | Color | YES |
|-------|----|-------|-------|-------|-----|
| <div style="width: 20px; height: 20px; background: #ff2a2a;"></div> | | <div style="width: 20px; height: 20px; background: #0168c8;"></div> | | <div style="width: 20px; height: 20px; background: #82c9fe;"></div> | |
"""




    legend = """
    | Color | Description |
    |-------|-------------|
    | <div style="width: 20px; height: 20px; background: #ff2a2a;"></div> | NO |
    | <div style="width: 20px; height: 20px; background: #0168c8;"></div> | MAYBE |
    | <div style="width: 20px; height: 20px; background: #82c9fe;"></div> | YES |
    """
    st.markdown(legend, unsafe_allow_html=True)



    return fig, legend







#######################################################


def create_sunburst_chartCampus(df):

# Preprocessing steps
  # Preprocessing steps
    df = df.copy()
    df['LIVE_CAMPUS?'].fillna("N/A", inplace=True)
    df['Where'].fillna("N/A", inplace=True)

    # Create the combined ID columns
    df['id_live_campus'] = df['LIVE_CAMPUS?']
    df['id_where'] = df['LIVE_CAMPUS?'] + "-" + df['Where']

    # Group the dataframe by combined IDs to get counts
    df_counts_live_campus = df.groupby(['id_live_campus']).size().reset_index(name='counts')
    df_counts_where = df.groupby(['id_where']).size().reset_index(name='counts')

    # Create a DataFrame for the root 'Total'
    df_total = pd.DataFrame({"id": ["Total"], "parent": [""], "counts": [df.shape[0]]})

    df_live_campus = df_counts_live_campus.copy()
    df_live_campus.columns = ['id', 'counts'] 
    df_live_campus['labels'] = df_live_campus['id']
    df_live_campus['parent'] = 'Total'

    df_where = df_counts_where.copy()
    df_where.columns = ['id', 'counts']  
    df_where['labels'] = df_where['id'].apply(lambda x: x.split("-")[-1])
    df_where['parent'] = df_where['id'].apply(lambda x: x.split("-")[0])

    # Concatenate all DataFrames
    df_sunburst = pd.concat([df_total, df_live_campus, df_where])

    # Calculate local and global percentages
    df_sunburst.reset_index(inplace=True)
    df_sunburst['local_percent'] = df_sunburst.groupby('parent', group_keys=False)['counts'].apply(lambda x: x / x.sum() * 100)
    df_sunburst['global_percent'] = df_sunburst['counts'] / df_sunburst['counts'].sum() * 100


    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['id'],
        labels=df_sunburst['labels'], 
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'], 
        branchvalues='total',
        hovertext=df_sunburst.apply(lambda row: f'Local percentage: {row["local_percent"]:.2f}%, Global percentage: {row["global_percent"]:.2f}%', axis=1),
        hoverinfo='label+text+value',
        maxdepth=3,
    ))
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    



    return fig










##############################################

def create_sunburst_chartSpin(df):
    # Fill NA values with "n/a"
    df = pd.read_csv('TOTAL1.csv')

    df.fillna("n/a", inplace=True)

    # Ensure uniqueness by converting to upper case and stripping leading/trailing whitespace
    df['USE_SPIN?'] = df['USE_SPIN?'].str.upper().str.strip()
    df['THINK_SPIN'] = df['THINK_SPIN'].str.upper().str.strip()

    # Compute counts for each combination of 'USE_SPIN?' and 'THINK_SPIN'
    df_sunburst = df.groupby(['USE_SPIN?', 'THINK_SPIN']).size().reset_index(name='counts')
    total_count = df_sunburst['counts'].sum()

    # Create new DataFrame for sunburst chart with 'parent', 'labels' and 'counts'
    df_sunburst_total = pd.DataFrame({
        'parent': [''] + ['Total' for _ in df_sunburst['USE_SPIN?'].unique()],
        'labels': ['Total'] + list(df_sunburst['USE_SPIN?'].unique()),
        'counts': [total_count] + list(df.groupby(['USE_SPIN?']).size())
    })
    df_sunburst_labels = pd.DataFrame({
        'parent': list(df_sunburst['USE_SPIN?']),
        'labels': list(df_sunburst['THINK_SPIN']),
        'counts': list(df_sunburst['counts'])
    })
    df_sunburst = pd.concat([df_sunburst_total, df_sunburst_labels])

    # Compute local and global percentages and create hover information
    df_sunburst.reset_index(inplace=True, drop=True)  # Reset index
    df_sunburst['local_percent'] = df_sunburst.groupby('parent', group_keys=False)['counts'].apply(lambda x: x / x.sum() * 100)
    df_sunburst['global_percent'] = df_sunburst['counts'] / total_count * 100
    df_sunburst['hoverinfo'] = df_sunburst['labels'].astype(str) + '<br>Local: ' + df_sunburst['local_percent'].round(2).astype(str) + '%' + '<br>Global: ' + df_sunburst['global_percent'].round(2).astype(str) + '%'

    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=df_sunburst['labels'],
        parents=df_sunburst['parent'],
        values=df_sunburst['counts'],
        hoverinfo='label+text+value',
        hovertext=df_sunburst['hoverinfo'],
        branchvalues='total',
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig.update_layout(
    width=500,  # Set the width of the chart
    height=500  # Set the height of the chart
)
    
    return fig
