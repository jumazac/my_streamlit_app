

import zipfile
import json
import os
import pydeck as pdk


def generate_map():
    os.environ["MAPBOX_API_KEY"] = 'pk.eyJ1IjoianVtYXphYyIsImEiOiJjbGowb3RjdTQwZzViM25sbDRjOXI3YzFyIn0.DkUhZZ6V7Y9fKSYUUXhnHw'

    with zipfile.ZipFile(r'C:\Users\JZ\Desktop\mygeodataUNIMAP.zip', 'r') as zip_ref:
        zip_ref.extractall(r'C:\Users\JZ\Desktop\unzipped_files')

    with open('C:/Users/JZ/Documents/GitHub/my_streamlit_app/MAP/mygeodata_merged.json', 'r') as f:
        geojson_data = json.load(f)

    purple_points = ['CLASE EDUCACION', 'CLASE GARFF', ...]  # Include all your purple points

    # Modify the color property
    for feature in geojson_data['features']:
        # Include all your if/elif statements for color modification
        if feature['properties']['Name'] == '1RA CONCETRACION, 8:45-19:45':
            feature['properties']['color'] = [255, 0, 0]
        # ... include the rest of the conditions here

    layer = pdk.Layer(
        'GeoJsonLayer',
        geojson_data,
        opacity=0.8,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        getLineColor="properties.color",
        getFillColor="properties.color",
        getLineWidth=11,
        getRadius=7,
    )

    view_state = pdk.ViewState(
        latitude=40.765313, 
        longitude=-111.838860, 
        zoom=14.70, 
        bearing=0, 
        pitch=0
    )

    r = pdk.Deck(layers=[layer], 
                  initial_view_state=view_state, 
                  map_style='mapbox://styles/jumazac/clj0e0eko00o301pu6i544yft',
                  api_keys={'mapbox': os.environ["MAPBOX_API_KEY"]},
                  map_provider='mapbox')

    return r