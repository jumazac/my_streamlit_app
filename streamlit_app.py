from Q1sunburst import create_sunburst_chartQs
from Q1sunburst import create_sunburst_chartCampus
from Q1sunburst import create_sunburst_chartSpin

import sys
print(sys.executable)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go






import streamlit as st



st.set_page_config(layout="wide")


# Define two columns
col1, col2 = st.columns(2)

# Place the logo in the first column
col1.markdown("![LOGO](https://i.imgur.com/DBZxXXg.png)")

# Place the header in the second column
col2.markdown("<h1 style='text-align: left; color: black;'>Ubike GO</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; justify-content: space-around;">
        <a href="#home">HOME</a>
        <a href="#market-analysis">Market Analysis</a>
        <a href="#map">MAP</a>
        <a href="#why-it-is-imperative">Why it is imperative</a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("""
    <div style="display: flex; justify-content: space-around; background-color: #F63366; padding: 10px;">
        <h2 style="color: white; margin: 0; font-size: 18px;"><a style="color: white; text-decoration: none;" href='#home'>HOME</a></h2>
        <h2 style="color: white; margin: 0; font-size: 18px;"><a style="color: white; text-decoration: none;" href='#market'>Market</a></h2>
        <h2 style="color: white; margin: 0; margin-left: 80px; font-size: 18px;"><a style="color: white; text-decoration: none;" href='#map'>MAP</a></h2>
        <h2 style="color: white; margin: 0; font-size: 18px;"><a style="color: white; text-decoration: none;" href='#why-it-is-imperative'>Why it is imperative</a></h2>
    </div>
""", unsafe_allow_html=True)


st.markdown("<br>"*2, unsafe_allow_html=True)


# Line break or space of 7 lines
st.markdown("<br>"*2, unsafe_allow_html=True)

st.markdown("<h2 id='home' style='display: none;'>HOME</h2>", unsafe_allow_html=True)

# Create the "HOME" section
st.markdown("<h4 id='home'>HOME</h1>", unsafe_allow_html=True)

# Define a new set of three columns
col4, line_col, col5 = st.columns([5, 0.2, 5])  # using a ratio to make the middle column thinner

# Write some text in the far right column of the new row with 6 line breaks after
col5.markdown("<p style='font-size:23px;'>What is this about?<br></p>", unsafe_allow_html=True)
col5.markdown("<p style='font-size:17px;'>Our groundbreaking service, Ubike Go, streamlines the campus life for university students, Specifically designed to meet students' needs, it offers an efficient solution for those striving to meet their academic and extracurricular commitments promptly. With Ubike Go, students can reach their destination within minutes, maintaining their independence, while eliminating the hassle, cost, and fatigue of daily commutes. This service ensures minimal effort on their part and promotes an enhanced quality of life.</p>", unsafe_allow_html=True)

col5.markdown("<br><br>", unsafe_allow_html=True)

# Write more text in the far right column of the new row
col5.markdown("<p style='font-size:23px;'>The distinctive edge we provide?<br></p>", unsafe_allow_html=True)
col5.markdown("<p style='font-size:17px;'>Primarily, comprehending students' needs and preferences, and integrating this insight with various engineering fields and their technological applications, enables us to design a bespoke and innovative response. This translates into a high-quality service, offered at an affordable cost, while simultaneously liberating students from the burden of owning traditional assets.</p>", unsafe_allow_html=True)

# Draw a vertical line by using a column with a small width and a tall, thin html div
line_col.markdown("<div style='height: 600px; border-left: 2px solid gray'></div>", unsafe_allow_html=True)

# Write some text in the first column of the second new row with 6 line breaks after
col4.markdown("<p style='font-size:23px;'>What do the students need?<br><br></p>", unsafe_allow_html=True)
col4.markdown("""
<p style='font-size:17px;'>
- Simplification of student life <br>
<br>
- Time Saver: Reduces average travel time, enhancing study, social, and activity time.<br>
<br>
- Affordable & Volume Discount: Priced within student budget with lower prices for increased usage, significantly less than owning a solution.<br>
<br>
- Comfortable & Quick Usage: Customized for user needs with no bike ownership hassles, offering seamless transportation perfect for on-the-go students.<br>
<br>
- Effortless Benefits: Stress-free, easy commuting enhances focus on high-value tasks and potentially improves academic performance.<br>
<br>
- Aligned with Government Objectives: In line with current federal and district commuting goals.
""", unsafe_allow_html=True)


# Add space
st.markdown("""
    <div style="height:190px;"></div>
""", unsafe_allow_html=True)


col6, col7, col8 = st.columns(3)
col6, col7, col8 = st.columns((1.3, 1.2, 1))

col7.markdown("<p style='font-size:23px;'>What are the numbers at the U?<br><br></p>", unsafe_allow_html=True)

# Add space
st.markdown("""
    <div style="height:100px;"></div>
""", unsafe_allow_html=True)


# Create the "Section 2" section
st.markdown("<h3 id='market-analysis'>Market analysis</h1>", unsafe_allow_html=True)


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
    hovertemplate='<b style="font-size: 16px;">%{label} </b> <br> <span style="font-size: 14px;">Count: %{value}<br> Path %{id}<br> percentage: %{customdata[0]:.2f}<br> global_percentage: %{customdata[1]:.2f}</span>',
    customdata=df_hierarchical['custom_data'],  # Here is where you include both 'percentage' and 'global_percentage'
    maxdepth=3,
    insidetextfont=dict(size=20),  # adjust size as needed
    outsidetextfont=dict(size=20)  # adjust size as needed
))



fig.update_layout(
    title_text="Main chart",    
    width=600,  # Set the width of the chart
    height=600  # Set the height of the chart
)

fig.update_layout(
    title_text="Main Sunburst",
    title_font=dict(size=23),  # Adjust the size as needed
)



cols = st.columns([1,3,2])

fig.update_layout(
    autosize=False,
    width=600,  # Modify these values as per your needs
    height=600,
)

cols[1].plotly_chart(fig)

# Define the labels and descriptions
labels = ['1. Year','2. Sex','3. Spin Usage?','4. Live on campus?','5. Question 1', '6. Question 2','7. Location']
descriptions = [
    "Year of the student",
    "Sex of the student",
    "Does the student use SPIN?",
    "Does the student live on campus",
    "Could your campus mobility be made more efficient? In terms of time, money and energy",
    "Would you be interested in an affordable, easy to use, fully autonomous ebike ride sharing service on campus? ",
    "The location of the interview"
]

# Create a DataFrame
df_labels = pd.DataFrame({
    'Ring': labels,
    'Description': descriptions
})

# Convert the DataFrame to an HTML table
table_html = df_labels.to_html(index=False)

# Style the HTML table with CSS
styled_table = f"""
<style>
    table, th, td {{
        border: 0 !important;
    }}
    table {{
        width: 100%;
    }}
    th, td {{
        text-align: left;
        padding: 8px;
        font-size: 17px;
    }}
    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
</style>
{table_html}
"""

# Display the table in the second column
cols[2].markdown(styled_table, unsafe_allow_html=True)

legend_height = 450  # The height of your sunburst chart in pixels
num_legend_items = 5  # The number of legend items

# Set the height of the container to be the same as the chart
container_style = f"height: {legend_height}px; display: flex; flex-direction: column; justify-content: space-between;"

cols[0].markdown(f"""
<div style='{container_style}'>
    <p style='text-align: center;'><div style='width: 20px; height: 20px; background: #0168c8;'></div> 1ST YEAR</p>
    <p style='text-align: center;'><div style='width: 20px; height: 20px; background: #82c9fe;'></div> 2ND YEAR</p>
    <p style='text-align: center;'><div style='width: 20px; height: 20px; background: #ffabab;'></div> 3RD YEAR</p>
    <p style='text-align: center;'><div style='width: 20px; height: 20px; background: #ff2a2a;'></div> 4TH YEAR</p>
    <p style='text-align: center;'><div style='width: 20px; height: 20px; background: #28b09c;'></div> MASTERS</p>
</div>
""", unsafe_allow_html=True)

# Add space
st.markdown("<br><br><br><br>", unsafe_allow_html=True)



# Define four columns instead of three
cols = st.columns([1, 0.1, 1, 0.1, 1])  # Adjust the numbers as needed

# Add your first sunburst chart
cols[0].markdown("Question 1 and 2")
fig, legend = create_sunburst_chartQs(df)  # Here's where you call the function and assign its returns
fig.update_layout(width=300, height=300)  # Set the width and height of the chart
cols[0].plotly_chart(fig)
cols[0].markdown(legend, unsafe_allow_html=True)

# Define the labels and descriptions
labels = ['Question 1','Reason','Quesition 2','Reason']
descriptions = [
    "Could your campus mobility be made more efficient? In terms of time, money and energy",
    "The Why",
    "Would you be interested in an affordable, easy to use, fully autonomous ebike ride sharing service on campus?",
    "The Why"]

# Create a DataFrame
df_table = pd.DataFrame({
    'Ring': labels,
    'Descriptions': descriptions
})

# Display the table
cols[0].table(df_table)

# Style the HTML table with CSS
styled_table = f"""
<style>
    table, th, td {{
        border: 0 !important;
    }}
    table {{
        width: 100%;
    }}
    th, td {{
        text-align: left;
        padding: 8px;
        font-size: 20px;
    }}
    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
</style>
{table_html}
"""

# Add a thin vertical line in the second column
cols[1].markdown("<hr style='border:1px solid gray; height:500px; width:1px; display:inline-block;' />", unsafe_allow_html=True)

# Add your second sunburst chart in the third column
cols[2].markdown("Living location")
fig, legend_campus = create_sunburst_chartCampus(df)
fig.update_layout(width=300, height=300)  # Set the width and height of the chart
cols[2].plotly_chart(fig)
cols[2].markdown(legend_campus, unsafe_allow_html=True)

# Define the labels and descriptions
labels = ['Do you Live on campus?','Where?']
descriptions = [
    "YES or NO",
    "Living Location"]

# Create a DataFrame
df_table = pd.DataFrame({
    'Ring': labels,
    'Descriptions': descriptions
})

# Display the table
cols[2].table(df_table)

# Style the HTML table with CSS
styled_table = f"""
<style>
    table, th, td {{
        border: 0 !important;
    }}
    table {{
        width: 100%;
    }}
    th, td {{
        text-align: left;
        padding: 8px;
        font-size: 20px;
    }}
    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
</style>
{table_html}
"""


cols[3].markdown("<hr style='border:1px solid gray; height:500px; width:1px; display:inline-block;' />", unsafe_allow_html=True)

# Add your third sunburst chart in the fifth column
cols[4].markdown("Do you use spin?")
fig, use_spin = create_sunburst_chartSpin(df)
fig.update_layout(width=300, height=300)  # Set the width and height of the chart
cols[4].plotly_chart(fig)
cols[4].markdown(use_spin, unsafe_allow_html=True)

# Define the labels and descriptions
labels = ['Do you use Spin?','What do you think of it?']
descriptions = [
    "YES or NO",
    "Reason"]

# Create a DataFrame
df_table = pd.DataFrame({
    'Ring': labels,
    'Descriptions': descriptions
})

# Display the table
cols[4].table(df_table)

# Style the HTML table with CSS
styled_table = f"""
<style>
    table, th, td {{
        border: 0 !important;
    }}
    table {{
        width: 100%;
    }}
    th, td {{
        text-align: left;
        padding: 8px;
        font-size: 20px;
    }}
    tr:nth-child(even) {{
        background-color: #f2f2f2;
    }}
</style>
{table_html}
"""

st.markdown("<br>"*2, unsafe_allow_html=True)

# Create the "MAP" section
st.markdown("<h2 id='map'>MAP</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns((1, 2, 1))
with col2:
    st.image("https://i.imgur.com/PSrs3vF.png", width=800)

st.markdown("<h2 id='why-it-is-imperative'>Why it is imperative</h2>", unsafe_allow_html=True)

# Create the "why imperative" 
col3, col4 = st.columns([2, 1])
with col3:
    st.header('Maslow hierarchy of the U students')
    st.image("https://i.imgur.com/AHwfyTu.png", caption='Maslow hierarchy of the U students', width=800)

# Display the list in the second column
with col4:
    st.header('Benefits of E-bike Ridesharing Service')
    # Define the data with number of line breaks
    data = {
        "Benefits": [
            {"text": "Surrounding all Concepts (Quality of Life): Our e-bike service enhances students' quality of life by addressing cost, time, convenience, health, and academic impact.", "breaks": 1},
            {"text": "Self-Actualization (Academic Impact): By reducing commuting inefficiencies, our service allows students to focus more on their academic goals and personal growth.", "breaks": 2},
            {"text": "Esteem (Physical Health): E-bike riding promotes physical health and well-being, boosting self-esteem through improved fitness and increased energy levels.", "breaks": 3},
            {"text": "Belonging (Convenience and Well-being): Our e-bike service offers a convenient mode of transport, fostering a sense of belonging and connection with the university environment.", "breaks": 3},
            {"text": "Safety Needs (Time Efficiency):With readily available e-bikes, students can commute quickly across campus, saving time for academic pursuits and leisure activities.", "breaks": 3},
            {"text": "Physiological Needs (Cost Efficiency): Our e-bike service saves students money by eliminating car ownership, gas, and parking costs, providing a budget-friendly transportation option", "breaks": 2},
        ]
    }

    st.write("<br>", unsafe_allow_html=True)  # Add a line break

    

# Create a DataFrame
df = pd.DataFrame(data)

with col3:
    # Display the table in Streamlit
    st.table(df)
