from Q1sunburst import create_sunburst_chartQs
from Q1sunburst import create_sunburst_chartCampus
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load data 
df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')


# Replace NaNs with 'N/A' in 'Why_1' and 'Why_2' columns
df['Why_1'] = df['Why_1'].fillna('N/A')
df['Why_2'] = df['Why_2'].fillna('N/A')

fig = create_sunburst_chartQs(df)
st.plotly_chart(fig)

fig = create_sunburst_chartCampus(df)
st.plotly_chart(fig)

def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i in range(len(levels)):
        level = levels[i]
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.applymap(lambda s: s.upper() if type(s) == str else s).groupby(levels[:i+1]).size().reset_index(name='counts')
        df_tree['label'] = dfg[level].copy()
        if i != 0:
            df_tree['parent'] = dfg[levels[:i]].copy().apply(lambda row: '->'.join(row.values.astype(str)), axis=1)
        else:
            df_tree['parent'] = 'total'
        df_tree['id'] = dfg[levels[:i+1]].copy().apply(lambda row: '->'.join(row.values.astype(str)), axis=1)
        df_tree['value'] = dfg['counts']
        df_tree['color'] = [color_mapping[x] for x in dfg[value_column].tolist()]
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                              value=df[value_column].count(),
                              color="white"
                              ))
    df_all_trees = pd.concat([df_all_trees, total.to_frame().T], ignore_index=True)
    return df_all_trees



# Define your color mapping
color_mapping = {
    '1ST': 'red',
    '2ND': 'blue',
    '3RD': 'green',
    '4TH': 'yellow',
    'MASTER' : 'purple'
    # Add more if needed
}



# Specify the hierarchy levels
levels = list(reversed(['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?', 'SEX','YEAR'])) # levels used for the hierarchical chart
value_column = 'YEAR' 
color_column = ['YEAR'] 

#build the heirachical data frame 
df_hierarchical = build_hierarchical_dataframe(df, levels, value_column)

# Compute the percentage and global_percentage columns
df_hierarchical['percentage'] = df_hierarchical.groupby('parent')['value'].transform(lambda x: x / x.sum() * 100)
df_hierarchical['global_percentage'] = (df_hierarchical['value'] / 126) * 100
# Map the color values
df_hierarchical['color'] = df_hierarchical['value'].map(color_mapping)
# Build the custom_data column
df_hierarchical['custom_data'] = list(zip(df_hierarchical.percentage, df_hierarchical.global_percentage))


# Create the sunburst chart
fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=df_hierarchical['label'],
    ids=df_hierarchical['id'],
    parents=df_hierarchical['parent'],
    values=df_hierarchical['value'],
    branchvalues='total',
    marker=dict(
        colors=df_hierarchical['color']
    ),
    hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> Path %{id}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}',
    customdata=df_hierarchical['custom_data'],  # Here is where you include both 'percentage' and 'global_percentage'
    maxdepth=2
))
# Display the sunburst chart in Streamlit
st.plotly_chart(fig)
st.markdown("<br>", unsafe_allow_html=True)




# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)




