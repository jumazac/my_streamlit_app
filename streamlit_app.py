import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("TOTAL1.csv")

# Count the occurrences for each combination of "IN EVENT?", "LOCATION", and "Q1".
df_counts = df.groupby(['IN EVENT?', 'LOCATION', 'Q1']).size().reset_index(name='counts')

levels = ['Q1', 'LOCATION', 'IN EVENT?']  # levels used for the hierarchical chart
value_column = 'counts'

def build_hierarchical_dataframe(df, levels, value_column, color_column=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).sum(numeric_only=True)
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        df_all_trees = pd.concat([df_all_trees, df_tree])
        print("This is df_tree after concat with level {}: \n{}".format(level, df_tree))  # print df_tree here
    total = pd.Series(dict(id='total', parent='',
                           value=df[value_column].sum(),
                           color='white' if color_column is None else df[color_column].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    print("This is df_all_trees after final append: \n{}".format(df_all_trees))  # print df_all_trees here
    return df_all_trees

df_all_trees = build_hierarchical_dataframe(df_counts, levels, value_column)

# Create the sunburst chart
fig = go.Figure(go.Sunburst(
    labels=df_all_trees['id'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    branchvalues='total',
    marker=dict(
        colors=df_all_trees['value'],
        colorscale='RdBu'),
    hovertemplate='<b>%{label} </b> <br> Count: %{value}',
))

fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

