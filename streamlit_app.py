import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Specify the levels, color column, and value column
levels = ['IN EVENT?']

df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
df_all_trees['id'] = df[levels[0]]
df_all_trees['parent'] = ""
df_all_trees['value'] = 1

fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=df_all_trees['id'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    branchvalues='total',
    hovertemplate='<b>%{label} </b> <br> Value: %{value}<br> Percentage of Total: %{percent:.2%}',
    maxdepth=2
))

fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))

st.plotly_chart(fig)




import streamlit as st

st.write("Hello, world!")

