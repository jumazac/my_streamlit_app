import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data

# Load your data
df = pd.read_csv("TOTAL1.csv")
print(df)

# Ensure AGE is numeric (int or float)
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')

# Replace AGE with a mapped color value
age_dict = {18: 0, 19: 1/6, 20: 2/6, 21: 3/6, 22: 4/6, 23: 5/6, 24: 1}
df['color_value'] = df['AGE'].map(lambda age: age_dict[age])

# Group data
df_grouped = df.groupby(['IN EVENT?', 'LOCATION']).size().reset_index(name='counts')

fig = go.Figure(go.Sunburst(
    labels=df_grouped['LOCATION'],
    parents=df_grouped['IN EVENT?'],
    values=df_grouped['counts'],
    branchvalues='total',
))

st.plotly_chart(fig)

print(df.columns)

import streamlit as st

st.write("Hello, world!")

