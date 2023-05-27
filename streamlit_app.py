import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')

def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    # Define your color mapping
    color_mapping = {
        '1ST': 'red',
        '2ND': 'blue',
        '3RD': 'green',
        '4TH': 'yellow',
        'MASTER' : 'purple'
        # Add more if needed
    }
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i in range(len(levels)):
        level = levels[i]
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.applymap(lambda s: s.upper() if type(s) == str else s).groupby(levels[:i+1]).size().reset_index(name='counts')
        df_tree['label'] = dfg[level].copy()
        if i != 0:
            df_tree['parent'] = dfg[levels[:i]].copy().apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
        else:
            df_tree['parent'] = 'total'
        df_tree['id'] = dfg[levels[:i+1]].copy().apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
        df_tree['value'] = dfg['counts']
        df_tree['color'] = [color_mapping[x] for x in dfg[value_column].tolist()]
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                              value=df[value_column].count(),
                              color="white"
                              ))
    df_all_trees = pd.concat([df_all_trees, total.to_frame().T], ignore_index=True)
    return df_all_trees

# Usage
# levels = list(reversed(['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?','SEX','YEAR'])) # levels used for the hierarchical chart
levels = list(reversed(['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?', 'SEX','YEAR'])) # levels used for the hierarchical chart
value_column = 'YEAR' 
color_column = ['YEAR'] 

df_hierarchical = build_hierarchical_dataframe(df, levels, value_column)
print(df_hierarchical.to_string())
# Create the sunburst chart
fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=df_hierarchical['label'],
    ids=df_hierarchical['id'],
    parents=df_hierarchical['parent'],
    values=df_hierarchical['value'],
    branchvalues='total',
    marker=dict(
        colors=df_hierarchical['color'],  # Now, these are specific color names
        colorscale=None  # Setting to None since we're using specific color names
    ),
    maxdepth=2

))


# Display the sunburst chart in Streamlit
st.plotly_chart(fig)

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

