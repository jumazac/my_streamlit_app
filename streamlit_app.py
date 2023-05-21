import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data

# Load your data
df = pd.read_csv("TOTAL1.csv")
print(df)

# Simplified Data
data = {'IN EVENT?': ['NO', 'NO', 'YES', 'YES', 'NO', 'NO'],
        'LOCATION': ['UNION', 'UNION', 'LASSONDE', 'LASSONDE', 'KALHERT', 'KALHERT'],
        'AGE': [18, 19, 20, 21, 22, 23]}

df = pd.DataFrame(data)

# Group data
df_grouped = df.groupby(['IN EVENT?', 'LOCATION']).size().reset_index(name='counts')

fig = go.Figure(go.Sunburst(
    labels=df_grouped['LOCATION'],
    parents=df_grouped['IN EVENT?'],
    values=df_grouped['counts'],
    branchvalues='total',
))

st.plotly_chart(fig)

st.plotly_chart(fig)

print(df.columns)

import streamlit as st

st.write("Hello, world!")

