import streamlit as st
import pandas as pd
import plotly.express as px

st.title('My First Streamlit App')

data = pd.read_csv('TOTAL1.csv')
st.dataframe(data.head())
data.columns = data.columns.str.strip()
data = data.fillna("N/A")


st.write(data.columns)

fig = px.sunburst(data, path=['IN EVENT?', 'LOCATION', 'Q1','Why 1','Q2','Why 2','USE SPIN ?','THINK SPIN','LIVE CAMPUS?','Where'], values='AGE', color='SEX',  
                 color_discrete_sequence=px.colors.sequential.Plasma,  # Define your color scale
                  hover_data=data.columns)  # Include all columns in hover data
fig.update_traces(textinfo='label+percent parent')  # Show label and percent of parent on each sector
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0)) 

st.plotly_chart(fig)





