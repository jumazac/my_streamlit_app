import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Load your data
df = pd.read_csv("TOTAL1.csv")

# Ensure AGE is numeric (int or float)
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

# Replace AGE with a mapped color value
age_dict = {18: 0, 19: 1/6, 20: 2/6, 21: 3/6, 22: 4/6, 23: 5/6, 24: 1}
df['color_value'] = df['AGE'].map(lambda age: age_dict[age])

# Specify the levels, color column, and value column
levels = ['IN EVENT?', 'LOCATION', 'Q1','Why 1','Q2','Why 2','USE SPIN ?','THINK SPIN','LIVE CAMPUS?','Where','AGE','SEX','color_value']
color_column = 'color_value'
value_column = 'YEAR'

def build_hierarchical_dataframe(df, levels, color_column=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).size().reset_index(name='value')  # Use size here instead of sum
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg['value']
        if color_column:
            df_tree['color'] = dfg[color_column]

        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
        
    total = pd.Series(dict(id='total', parent='', 
                           value=df.shape[0],   # Use shape[0] here to get the total count
                           color=df[color_column].sum() if color_column else None))
    df_all_trees = pd.concat([df_all_trees, pd.DataFrame(total).T], ignore_index=True)
    return df_all_trees

df_all_trees = build_hierarchical_dataframe(df, levels, color_column)
print(df_all_trees.head())
print(df_all_trees.tail())

st.write(df_all_trees)

fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=df_all_trees['id'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    branchvalues='total',
    marker=dict(
        colors=df_all_trees['color'],
        colorscale='RdBu',
    ),
    hovertemplate='<b>%{label} </b> <br> Value: %{value}<br> Percentage of Total: %{percent:.2%}',
    maxdepth=2
))

fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))

st.plotly_chart(fig)

import streamlit as st

st.write("Hello, world!")

