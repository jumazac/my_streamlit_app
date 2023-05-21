import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data
df = pd.read_csv("TOTAL1.csv")


levels = ['IN EVENT?']

# Function to build hierarchical DataFrame
def build_hierarchical_dataframe(df, levels, value_column='count'):
    d = dict(zip([f"level_{i+1}" for i in range(len(levels))], levels))
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        d_temp = d.copy()
        d_temp.pop(f"level_{i+1}")
        df_grouped = df.groupby(by=list(d_temp.values())).count().reset_index()
        df_tree['id'] = df_grouped[level].copy()
        
        if i < len(levels) - 1:
            df_tree['parent'] = df_grouped[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        
        df_tree['value'] = df_grouped[value_column]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
        
    df_all_trees = df_all_trees.sort_values(by='id')
    df_all_trees = df_all_trees.reset_index(drop=True)
    total = pd.Series(dict(id='total', parent='',
                           value=df[value_column].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    
    return df_all_trees

# Build the hierarchical DataFrame
df_all_trees = build_hierarchical_dataframe(df, levels)

# Create the sunburst chart
fig = px.sunburst(df_all_trees, 
                  path=['parent', 'id'], 
                  values='value')

# Show the chart
fig.show()


# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)

