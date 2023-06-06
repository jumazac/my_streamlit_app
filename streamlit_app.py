from Q1sunburst import create_sunburst_chartQs
from Q1sunburst import create_sunburst_chartCampus
from Q1sunburst import create_sunburst_chartSpin

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



import streamlit as st


st.set_page_config(layout="wide")

# Define three columns
col1, col2, col3 = st.columns(3)




# Create a header
st.markdown("# Ubike GO ")

# Create a custom header with links
st.markdown("""
    <div style="display: flex; justify-content: space-around; background-color: #F63366; padding: 10px;">
        <h2 style="color: white; margin: 0;"><a style="color: white; text-decoration: none;" href='https://example.com/link1'>Market analysis</a></h2>
        <h2 style="color: white; margin: 0; margin-left: 80px;"><a style="color: white; text-decoration: none;" href='https://example.com/link2'>MAP</a></h2>
        <h2 style="color: white; margin: 0;"><a style="color: white; text-decoration: none;" href='https://example.com/link3'>Why it is imperative</a></h2>
    </div>
""", unsafe_allow_html=True)

# Create a single column layout for the main chart
col_main = st.columns(1)


# Load data 
df = pd.read_csv("TOTAL1NOTEPAD.txt", delimiter=',')




# Replace NaNs with 'N/A' in 'Why_1' and 'Why_2' columns
df['Why_1'] = df['Why_1'].fillna('N/A')
df['Why_2'] = df['Why_2'].fillna('N/A')

df['THINK_SPIN'] = df['THINK_SPIN'].fillna("N/a")





def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i in range(len(levels)):
        level = levels[i]
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.applymap(lambda s: s.upper() if type(s) == str else s).groupby(levels[:i+1]).size().reset_index(name='counts')
        df_tree['label'] = dfg[level].copy()
        if i != 0:
            df_tree['parent'] = dfg[levels[:i]].copy().apply(lambda row: '->'.join(row.values.astype(str)), axis=1)
        else:
            df_tree['parent'] = 'total'
        df_tree['id'] = dfg[levels[:i+1]].copy().apply(lambda row: '->'.join(row.values.astype(str)), axis=1)
        df_tree['value'] = dfg['counts']
        df_tree['color'] = [color_mapping[x] for x in dfg[value_column].tolist()]
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                              value=df[value_column].count(),
                              color="white"
                              ))
    df_all_trees = pd.concat([df_all_trees, total.to_frame().T], ignore_index=True)
    return df_all_trees



# Define your color mapping
color_mapping = {
    '1ST': 'red',
    '2ND': 'blue',
    '3RD': 'green',
    '4TH': 'yellow',
    'MASTER' : 'purple'
    # Add more if needed
}



# Specify the hierarchy levels
levels = list(reversed(['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?', 'SEX','YEAR'])) # levels used for the hierarchical chart
value_column = 'YEAR' 
color_column = ['YEAR'] 

#build the heirachical data frame 
df_hierarchical = build_hierarchical_dataframe(df, levels, value_column)

# Compute the percentage and global_percentage columns
df_hierarchical['percentage'] = df_hierarchical.groupby('parent')['value'].transform(lambda x: x / x.sum() * 100)
df_hierarchical['global_percentage'] = (df_hierarchical['value'] / 126) * 100
# Map the color values
df_hierarchical['color'] = df_hierarchical['value'].map(color_mapping)
# Build the custom_data column
df_hierarchical['custom_data'] = list(zip(df_hierarchical.percentage, df_hierarchical.global_percentage))


# Create the sunburst chart
fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=df_hierarchical['label'],
    ids=df_hierarchical['id'],
    parents=df_hierarchical['parent'],
    values=df_hierarchical['value'],
    branchvalues='total',
    marker=dict(
        colors=df_hierarchical['color']
    ),
    hovertemplate='<b>%{label} </b> <br> Count: %{value}<br> Path %{id}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}',
    customdata=df_hierarchical['custom_data'],  # Here is where you include both 'percentage' and 'global_percentage'
    maxdepth=2

    
))


fig.update_layout(
    title_text="Main chart",
    width=800,  # Set the width of the chart
    height=800  # Set the height of the chart
)

fig.update_layout(
    title_text="Main Sunburst",
    title_font=dict(size=30),  # Adjust the size as needed
)

# Create the columns for the layout
cols = st.columns([1,1]) 

# Define the labels and descriptions
labels = ['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?', 'SEX','YEAR']
descriptions = [
    "Description of what 'LOCATION' represents",
    "Description of what 'Q2' represents",
    "Description of what 'Q1' represents",
    "Description of what 'LIVE_CAMPUS?' represents",
    "Description of what 'USE_SPIN?' represents",
    "Description of what 'SEX' represents",
    "Description of what 'YEAR' represents"
]

# Create a DataFrame
df_labels = pd.DataFrame({
    'Label': labels,
    'Description': descriptions
})

# Display the DataFrame as a table in the second column
cols[1].table(df_labels)



cols = st.columns([1,2,1]) 
cols[1].plotly_chart(fig)

# Define the labels and descriptions
labels = ['LOCATION','Q2','Q1','LIVE_CAMPUS?','USE_SPIN?', 'SEX','YEAR']
descriptions = [
    "Description of what 'LOCATION' represents",
    "Description of what 'Q2' represents",
    "Description of what 'Q1' represents",
    "Description of what 'LIVE_CAMPUS?' represents",
    "Description of what 'USE_SPIN?' represents",
    "Description of what 'SEX' represents",
    "Description of what 'YEAR' represents"
]

# Create a DataFrame
df_labels = pd.DataFrame({
    'Label': labels,
    'Description': descriptions
})

# Display the DataFrame as a table in the second column
cols[1].table(df_labels)

# Create the legend
legend_cols = st.columns(5)


legend_cols[0].markdown("<p style='text-align: center;'><div style='width: 20px; height: 20px; background: #0168c8;'></div> 1ST YEAR</p>", unsafe_allow_html=True)
legend_cols[1].markdown("<p style='text-align: center;'><div style='width: 20px; height: 20px; background: #82c9fe;'></div> 2ND YEAR</p>", unsafe_allow_html=True)
legend_cols[2].markdown("<p style='text-align: center;'><div style='width: 20px; height: 20px; background: #ffabab;'></div> 3RD YEAR</p>", unsafe_allow_html=True)
legend_cols[3].markdown("<p style='text-align: center;'><div style='width: 20px; height: 20px; background: #ff2a2a;'></div> 4TH YEAR</p>", unsafe_allow_html=True)
legend_cols[4].markdown("<p style='text-align: center;'><div style='width: 20px; height: 20px; background: #28b09c;'></div> MASTERS</p>", unsafe_allow_html=True)


# Add space
st.markdown("<br><br><br><br>", unsafe_allow_html=True)



# Define three columns for the other charts
cols = st.columns([1, 1, 1])  # Adjust the numbers as needed

# For create_sunburst_chartQs chart
cols[0].markdown("Question 1 and 2")
fig = create_sunburst_chartQs(df)
fig.update_layout(width=500, height=500)  # Set the width and height of the chart
cols[0].plotly_chart(fig)

# For create_sunburst_chartCampus chart
cols[1].markdown("Living location")
fig = create_sunburst_chartCampus(df)
fig.update_layout(width=500, height=500)  # Set the width and height of the chart
cols[1].plotly_chart(fig)

# For create_sunburst_chartSpin chart
cols[2].markdown("Do you use spin?")
fig = create_sunburst_chartSpin(df)
fig.update_layout(width=500, height=500)  # Set the width and height of the chart
cols[2].plotly_chart(fig)
