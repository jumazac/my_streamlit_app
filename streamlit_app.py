from Q1sunburst import create_sunburst_chartQs
from Q1sunburst import create_sunburst_chartCampus
from Q1sunburst import create_sunburst_chartSpin
from MAPA import generate_map

import os
import json
import zipfile
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk



import streamlit as st

st.set_page_config(layout="wide")


st.markdown("""
<style>
body {
    color: #000000;
    background-color: #FFFFFF;
}
</style>
    """, unsafe_allow_html=True)

# Define two columns
col1, col2 = st.columns([1, 2])

# Place the logo in the first column
col1.markdown('<img src="https://i.imgur.com/DBZxXXg.png" width="400">', unsafe_allow_html=True)

# Place the header in the second column
col2.markdown("<h1 style='text-align: left; color: black; font-size: 70px; font-family: Helvetica;'>Ubike GO</h1>", unsafe_allow_html=True)
col2.markdown("<h2 style='text-align: left; color: black; font-size: 30px; font-family: Helvetica;'>A micromobility service to the student community; low cost, reliable and environmentally safe.</h2>", unsafe_allow_html=True)


st.markdown("<br>"*2, unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; justify-content: space-around; background-color: #F63366; padding: 20px;">
        <a href="#home" style="text-decoration: none; color: white; font-size: 16px;">HOME</a>
        <a href="#market-analysis" style="text-decoration: none; color: white;">Market Analysis</a>
        <a href="#map" style="text-decoration: none; color: white;">MAP</a>
        <a href="#why-it-is-imperative" style="text-decoration: none; color: white;">Why it is imperative</a>
    </div>
    """,
    unsafe_allow_html=True
)



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

st.markdown("<h1 id='why-it-is-imperative'>Why it is imperative</h1>", unsafe_allow_html=True)

# Create the "why imperative" 
col3, col4 = st.columns([2, 1.5])
with col3:
    st.header('Maslow hierarchy of the U students')
    st.image("https://i.imgur.com/AHwfyTu.png", width=800)

# Display the list in the second column
with col4:
    st.header('Benefits of E-bike Ridesharing Service')
    # Define the data with number of line breaks
    data = {
        "Benefits": [
            {"text": "Surrounding all Concepts (Quality of Life): Our e-bike service enhances students' quality of life by addressing cost, time, convenience, health, and academic impact.", "breaks": 1, "color": "rgba(50,153,205,5)"},
            {"text": "Self-Actualization (Academic Impact): By reducing commuting inefficiencies, our service allows students to focus more on their academic goals and personal growth.", "breaks": 2, "color": "rgba(147,38,143,255)"},
            {"text": "Esteem (Physical Health): E-bike riding promotes physical health and well-being, boosting self-esteem through improved fitness and increased energy levels.", "breaks": 3, "color": "rgba(0,166,81,255)"},
            {"text": "Belonging (Autonomy and Well-being): Our e-bike service offers an independent mode of transport, fostering a sense of belonging and connection with the university environment.", "breaks": 3, "color": "rgba(230,231,20,255)"},
            {"text": "Safety Needs (Time Efficiency):With readily available e-bikes, students can commute quickly across campus, saving time for academic pursuits and leisure activities.", "breaks": 3, "color": "rgba(255,186,19,255)"},
            {"text": "Physiological Needs (Cost Efficiency): Our e-bike service saves students money by eliminating car ownership, gas, and parking costs, providing a budget-friendly transportation option", "breaks": 2, "color": "rgba(243,130,47,255)"},
        ]
    }
    for benefit in data["Benefits"]:
        st.markdown(f'<div style="background-color: {benefit["color"]}; color: #222222; padding: 10px;">{benefit["text"]}</div>', unsafe_allow_html=True)
        for _ in range(benefit["breaks"]):
            st.write("<br>", unsafe_allow_html=True)


    

# Create a DataFrame
df = pd.DataFrame(data)



# Create a container
container = st.container()


# Within the container, create a column
with container:
    col1 = st.columns(1)

with col1[0]:
    # Your map code
    view_state = pdk.ViewState(
        latitude=40.7648,  # Coordinates for the University of Utah
        longitude=-111.8421,
        zoom=14.05,
        pitch=0
    )

# Define the DataFrame with all the coordinates
df = pd.DataFrame({
    'location': ['Location1', 'Location2', 'Location3', 'Location4', 'Location5', 'Location6', 'Location7', 'Location8', 'Location9', 'Location10', 'Location11'],
    'coordinates': [
        [
            [-111.838122, 40.776064],
            [-111.836941, 40.774357],
            [-111.835631, 40.774487],
            [-111.834107, 40.773415],
            [-111.832475, 40.771741],
            [-111.830929, 40.769791],
            [-111.827322, 40.767093],
            [-111.825111, 40.768004],
            [-111.821890, 40.770587],
            [-111.820181, 40.773220],
            [-111.834833, 40.775876],
            [-111.836035, 40.774413]
        ],
        [
            [-111.836464, 40.774088],
            [-111.837753, 40.773373],
            [-111.841661, 40.773146],
            [-111.842906, 40.772333],
            [-111.843679, 40.771326],
            [-111.847286, 40.771228],
            [-111.848059, 40.770611],
            [-111.847888, 40.768400],
            [-111.849090, 40.768205],
            [-111.849219, 40.767165],
            [-111.852053, 40.767263],
            [-111.851924, 40.774608],
            [-111.842118, 40.775811]
        ],
        [
            [-111.852523, 40.767337],
            [-111.852523, 40.765160],
            [-111.858041, 40.765143],
            [-111.857910, 40.766947]
        ],
        [
            [-111.852493, 40.764883],
            [-111.852557, 40.760776],
            [-111.862317, 40.760817],
            [-111.862353, 40.764769],
            [-111.852604, 40.764818]
        ],
        [
            [-111.852495, 40.760516],
            [-111.852506, 40.758688],
            [-111.859463, 40.758679],
            [-111.859474, 40.760565]
        ],
        [
            [-111.845713, 40.758236],
            [-111.853551, 40.758220],
            [-111.853640, 40.754270],
            [-111.845610, 40.754091]
        ],
        [
            [-111.854220, 40.758220],
            [-111.862079, 40.758203],
            [-111.862245, 40.754205],
            [-111.854021, 40.754237]
        ],
        [
            [-111.845071, 40.758216],
            [-111.838802, 40.758090],
            [-111.836441, 40.757179],
            [-111.834196, 40.755294],
            [-111.833110, 40.753643],
            [-111.831213, 40.751149],
            [-111.844788, 40.751237],
            [-111.844830, 40.758161]
        ],
        [
            [-111.835735, 40.762028],
            [-111.834835, 40.759341],
            [-111.835124, 40.758647],
            [-111.836025, 40.757607],
            [-111.838141, 40.758415],
            [-111.839580, 40.758642],
            [-111.841510, 40.758688],
            [-111.845181, 40.758679],
            [-111.845149, 40.758939],
            [-111.844645, 40.759281],
            [-111.844183, 40.759346],
            [-111.843313, 40.759167],
            [-111.842497, 40.759045],
            [-111.841800, 40.759086],
            [-111.841113, 40.759200],
            [-111.838826, 40.760386],
            [-111.835691, 40.762052]
        ],
        [
            [-111.835183, 40.762267],
            [-111.832241, 40.763664],
            [-111.830480, 40.761665],
            [-111.834196, 40.759520]
        ],
        [
            [-111.830245, 40.761812],
            [-111.828634, 40.762637],
            [-111.828335, 40.763697],
            [-111.828184, 40.764331],
            [-111.828485, 40.765013],
            [-111.828056, 40.765371],
            [-111.828442, 40.765858],
            [-111.827368, 40.766703],
            [-111.827329, 40.767207],
            [-111.822906, 40.764737],
            [-111.826492, 40.761552],
            [-111.827974, 40.760593],
            [-111.828983, 40.760983],
            [-111.830228, 40.761779]
        ]
    ]
})


# Create the PyDeck layer for the polygons
polygon_layer = pdk.Layer(
    "PolygonLayer",
    data=df,
    get_polygon="coordinates",
    filled=True,
    extruded=False,
    get_fill_color=[0, 0, 0, 150],  # RGBA color value for the fill (transparent black)
    get_line_color=[0, 0, 0],  # RGB color value for the outline (black color)
    get_line_width=1,  # Line width for the outline
    pickable=True
)

df_red = pd.DataFrame({
    'location': ['Location Red'],
    'coordinates': [[
        [-111.845360, 40.765197],
        [-111.847197, 40.765270],
        [-111.847509, 40.763718],
        [-111.846553, 40.762848],
        [-111.845952, 40.762052],
        [-111.845007, 40.762068],
        [-111.844127, 40.762401],
        [-111.844878, 40.763190],
        [-111.845211, 40.764067],
        [-111.845437, 40.765099]
    ]]
})

# Create the PyDeck layer for the red transparent polygon
polygon_layer_red = pdk.Layer(
    "PolygonLayer",
    data=df_red,
    get_polygon="coordinates",
    filled=True,
    extruded=False,
    get_fill_color=[255, 0, 0, 150],  # RGBA color value for the fill (red transparent)
    auto_highlight=True,  # Highlight the polygon on hover
    get_fill_color_highlight=[255, 255, 0, 100],  # RGBA color value for the fill during hover (yellow transparent)
    get_line_color_highlight=[255, 255, 0],  # RGB color value for the outline during hover (yellow color)
    pickable=True,
    tooltip={"text": "Red Polygon"},  # Add tooltip for the red polygon
)

df_orange = pd.DataFrame({
    'location': ['Location Orange'],
    'coordinates': [
        [
            [-111.830712, 40.766424],
            [-111.830255, 40.765871],
            [-111.830341, 40.765571],
            [-111.830963, 40.765302],
            [-111.831515, 40.765995],
            [-111.831962, 40.766440],
            [-111.831833, 40.766749],
            [-111.831124, 40.766830]
        ]
    ]
})

# Create the PyDeck layer for the orange transparent polygon
polygon_layer_orange = pdk.Layer(
    "PolygonLayer",
    data=df_orange,  # Explode the coordinates to ensure equal length
    get_polygon="coordinates",
    filled=True,
    extruded=False,
    get_fill_color=[240, 128, 8, 150]  # RGBA color value for the fill (orange transparent)

)

df_yellow = pd.DataFrame({
    'location': ['Location Yellow'],
    'coordinates': [
        [
            [-111.837131, 40.765205],
            [-111.836863, 40.764547],
            [-111.836455, 40.763523],
            [-111.836637, 40.763214],
            [-111.837271, 40.762840],
            [-111.838130, 40.762800],
            [-111.838699, 40.763596],
            [-111.839815, 40.764953],
            [-111.838356, 40.765619],
            [-111.837937, 40.765749],
            [-111.837078, 40.765107]
        ]
    ]
})

# Create the PyDeck layer for the yellow transparent polygon
polygon_layer_yellow = pdk.Layer(
    "PolygonLayer",
    data=df_yellow,  # Explode the coordinates to ensure equal length
    get_polygon="coordinates",
    filled=True,
    extruded=False,
    get_fill_color=[255, 255, 0, 100]  # RGBA color value for the fill (yellow transparent)
)

r = pdk.Deck(
    layers=[polygon_layer, polygon_layer_red, polygon_layer_orange, polygon_layer_yellow],  # Add both polygon layers to the list
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11"  # Mapbox style URL
)

# Display the map using Streamlit
st.pydeck_chart(r)

# Generate the map
r = generate_map()


col1, col2, col3 = st.beta_columns([1,6,1])

with col2:
    st.pydeck_chart(generate_map())


