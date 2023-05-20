import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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




# Load your data
df = pd.read_csv("TOTAL1.csv")

age_dict = {18: 0, 19: 1/6, 20: 2/6, 21: 3/6, 22: 4/6, 23: 5/6, 24: 1}
df['color_value'] = df['AGE'].map(lambda age: age_dict[age])

colorscale = [[0, 'red'], [1/6, 'orange'], [2/6, 'yellow'], [3/6, 'green'], [4/6, 'blue'], [5/6, 'indigo'], [1, 'violet']] 


levels = ['IN EVENT?', 'LOCATION', 'Q1','Why 1','Q2','Why 2','USE SPIN ?','THINK SPIN','LIVE CAMPUS?','Where','AGE','SEX']
color_column = ['color_value']
value_column = 'YEAR'


def build_hierarchical_dataframe(df, levels, value_column, color_column=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum(numeric_only=False)
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        if color_column:
            df_tree['color'] = dfg[color_column]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                           value=df[value_column].sum(),
                           color=df[color_column].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees

df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_column)
total_value = df[value_column].sum()

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
fig.show()
