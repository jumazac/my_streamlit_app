import zipfile
import json
import os
import pydeck as pdk


def generate_map():
    os.environ["MAPBOX_API_KEY"] = 'pk.eyJ1IjoianVtYXphYyIsImEiOiJjbGowb3RjdTQwZzViM25sbDRjOXI3YzFyIn0.DkUhZZ6V7Y9fKSYUUXhnHw'

    with zipfile.ZipFile('mygeodataUNIMAP.zip', 'r') as zip_ref:
        zip_ref.extractall('unzipped_files')

    # Load the original GeoJSON data
    with open('unzipped_files/mygeodata_merged.json', 'r') as f:
        geojson_data = json.load(f)

    purple_points = ['CLASE EDUCACION', 'CLASE GARFF', 'CLASE BUSINESS', 'CLASE BUSINESS2', 'CLASE ARCH', 
                     'CLASE ART', 'CLASE SOCIALES', 'CLASE SOWORK', 'CLASE BEHSCIENCE', 'CLASE CIENCIA', 
                     'CLASE HUMANIDADES', 'CLASE PHILO', 'CLASE BIO', 'CLASE MATH', 'CLASE MATH ',
                     'CLASE MATH', 'CLASE MATH ', 'CLASE TEATRO ', 'CLASE MUSICA', 'CLASE LAB',
                     'CALSE BIO', 'CLASE DANZA', 'CLASE QUIM', 'CLASE FISICA', 'CLASE ING', 'CLASE ING ',
                     'CLASE ING', 'CLASE ING ', 'CLASE ING', 'CLASE ING ', 'CLASE PC', 'CLASE ING',
                     'CLASE ING ', 'CLASE ING ', 'CLASE VARIAS', 'CLASE KINE', 'CLASE LEYES', 'CLASE QUIM',
                     'CLASE ANTH', 'CLASE BIO', 'CLASE ANTH ', 'CLASE PERF ARTS', 'CLASE ARTSF',
                     'CLASE MED', 'CLASE MED ', 'CLASE MED', 'LIBRERIA MED', 'CLASE MED', 'CLASE PHA',
                     'CLASS ING', 'CLASE BUSINESS']

    # Modify the color property
    for feature in geojson_data['features']:
        # existing conditions
        if feature['properties']['Name'] == '1RA CONCETRACION, 8:45-19:45':
            feature['properties']['color'] = [255, 0, 0, 95]  # RGB color for red
        elif feature['properties']['Name'] == '2DA CONCERNTRACION, 10:00-22:00':
            feature['properties']['color'] = [44, 165, 0, 95]
        elif feature['properties']['Name'] == '3RA CONCENTRACION, 10:00-22:00':
            feature['properties']['color'] = [255, 255, 0, 95]  # RGB color for yellow
        elif feature['properties']['Name'] == 'Polygon 150':
            feature['properties']['color'] = [0, 0, 0,]
        elif feature['properties']['Name'] in ['Polygon 135', 'Polygon 138', 'Polygon 139', 'Polygon 148', 'Polygon 147', 'Polygon 133', 'Polygon 140', 'UNION']:
            feature['properties']['color'] = [0, 0, 0]  # RGB color for black
        elif feature['properties']['Name'] == 'RUTA 1, 1 MILLA':
            feature['properties']['color'] = [0, 84, 255]
        elif feature['properties']['Name'] in purple_points:
            feature['properties']['color'] = [128, 0, 128]  # RGB color for purple
        elif feature['properties']['Name'] in ['CAFETERIA PHC', 'CAFETERIA KALHERT']:
            feature['properties']['color'] = [173, 216, 230]  # RGB color for light blue
        elif feature['properties']['Name'] == 'HOSPITAL':
            feature['properties']['color'] = [85, 107, 47]  # RGB color for swampy green
        elif feature['properties']['Name'] == 'BIBLIOTECA':
            feature['properties']['color'] = [165, 42, 42]  # RGB color for brown
        elif feature['properties']['Name'] == 'TIENDA CAMPUS':
            feature['properties']['color'] = [255, 105, 180]  # RGB color for hot pink
        elif feature['properties']['Name'] == 'ELEVADOR':
            feature['properties']['color'] = [128, 128, 128]  # RGB color for gray
        elif feature['properties']['Name'] in ['STADIO', 'ESTADIO']:
            feature['properties']['color'] = [255, 0, 0]
        elif 'DORMITORIO' in feature['properties']['Name']:  
            feature['properties']['color'] = [34, 139, 34]
        elif feature['properties']['Name'] == 'GYM BASKET':  
            feature['properties']['color'] = [0, 0, 255]  # RGB color for yellow
        elif feature['properties']['Name'] == 'GYM':
            feature['properties']['color'] = [0, 0, 255]  # RGB color for yellow

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
    getPointRadius=7,
    pickable=True,  # Enable hovering
    auto_highlight=True,  # Highlight object on hover
    tooltip={
        "html": "<b>Name:</b> {properties.Name}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
)

    view_state = pdk.ViewState(
        latitude=40.765313, 
        longitude=-111.838860, 
        zoom=14.05, 
        bearing=0, 
        pitch=0
    )

    r = pdk.Deck(layers=[layer], 
                  initial_view_state=view_state, 
                  map_style='mapbox://styles/jumazac/clj1wx5ue00rm01r7hr755dsv',
                  api_keys={'mapbox': os.environ["MAPBOX_API_KEY"]},
                  map_provider='mapbox')

    return r




with zipfile.ZipFile('mygeodataUNIMAP.zip', 'r') as zip_ref:
    zip_ref.extractall('unzipped_files')

# Load the GeoJSON data
with open('unzipped_files/mygeodata_merged.json', 'r') as f:
    geojson_data = json.load(f)

for feature in geojson_data['features']:

    if feature['properties']['Name'] == '2DA CONCERNTRACION, 10:00-22:00':
        feature['properties']['color'] = [255, 0, 0, 95]  # RGB color for red
        print(f"2DA CONCERNTRACION color: {feature['properties']['color']}")
    