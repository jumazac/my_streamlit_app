import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




df = pd.read_csv("TOTAL1.csv")

# Specify the levels
levels = ['YEAR', 'SEX', 'AGE']

def build_hierarchical_dataframe(df, levels):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.
    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).size().reset_index(name='value')
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg['value']
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
        
    total = pd.Series(dict(id='total', parent='', value=df.shape[0]))
    df_all_trees = pd.concat([df_all_trees, pd.DataFrame(total).T], ignore_index=True)
    return df_all_trees

df_all_trees = build_hierarchical_dataframe(df, levels)

fig = px.sunburst(df_all_trees, path=['parent', 'id'], values='value')

st.plotly_chart(fig)


# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

