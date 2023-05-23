import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("TOTAL1.csv")


def build_hierarchical_dataframe(df, levels, value_column, color_column=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])

    for i, level in enumerate(levels):
        df_tree = df.groupby(levels[:i + 1]).sum().reset_index()
        if i < len(levels) - 1: 
            # Not the last level
            parents = levels[:i + 1]
            df_tree.columns = parents + ['value']
        else:
            # This is the last level, so add 'id' and 'parent' columns
            parents = levels[:i] if i > 0 else ['']
            df_tree.columns = ['id'] + parents + ['value']

        df_all_trees = pd.concat([df_all_trees, df_tree], axis=0, ignore_index=True)

    total = pd.DataFrame(dict(id='total', parent='',
                              value=df[value_column].sum(),
                              color='white' if color_column is None else df[color_column].sum()), 
                              index=[0])
    df_all_trees = pd.concat([df_all_trees, total], axis=0, ignore_index=True)

    return df_all_trees

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

