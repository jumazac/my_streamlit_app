import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("TOTAL1.csv")


def build_hierarchical_dataframe(df, levels, color_column):
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).size().reset_index(name='counts')
        df_tree['id'] = dfg[level].copy().astype(str)
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy().astype(str)
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg['counts']
        df_tree['color'] = dfg[color_column].astype(str)
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)

    total = pd.Series(dict(id='total', parent='', value=df.shape[0], color=df[color_column].astype(str).iloc[0]))
    df_all_trees = pd.concat([df_all_trees, total.to_frame().T], ignore_index=True)
    return df_all_trees


# Usage
levels = ['LOCATION', 'Q2', 'Q1', 'LIVE CAMPUS?', 'USE SPIN?', 'SEX', 'YEAR'] # levels used for the hierarchical chart
color_column = 'YEAR' 
df_hierarchical = build_hierarchical_dataframe(df, levels, color_column)

# Create the sunburst chart using plotly.express
fig = px.sunburst(df_hierarchical, path=['id'], values='value', color='color')

# Display the sunburst chart in Streamlit
st.plotly_chart(fig)


# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

