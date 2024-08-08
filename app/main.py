import json
import plotly
import logging
import psycopg2
import pandas as pd
import geopandas as gpd
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)
logging.basicConfig(level = logging.INFO)
log = logging.getLogger(__name__)

pg_conn = psycopg2.connect(
    database = "d72a67cdceapef", 
    user = "uc92dmpvijavad", 
    password = "pa7f74c3a5dc0caca8d24c700606b0eea9f1624f404b4079fb11087a2b1fb4858", 
    host = "c6sfjnr30ch74e.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com", 
    port = "5432"
)
pg_cursor = pg_conn.cursor() 

melbourne_coordinates = {"lat": -37.8136, "lon": 144.9631}

@app.route('/', methods = ['GET'])
def index():
    """
    A function rendering landing page.
    """

    return render_template('index.html', error = False)

@app.route('/insights', methods = ['GET'])
def display_insights():
    """
    A function to render the insights page.
    """
    
    # Read LGA polygon data
    lga_df = gpd.GeoDataFrame.from_postgis("select * from postgis.lga", con=pg_conn, geom_col="geometry")  
    lga_geojson_data = json.loads(lga_df.to_json())

    # Read accidents distribution by LGA data
    a_df = pd.read_sql_query('select * from postgis.accidents',con=pg_conn)
    accidents_df = a_df.groupby("LGA_NAME")['ACCIDENT_NO'].agg('count') \
        .rename('ACCIDENT_COUNT').reset_index() \
        .sort_values('ACCIDENT_COUNT', ascending = True).reset_index()

    # Creating the choropleth map
    choropleth_map = px.choropleth_mapbox(
        accidents_df,
        geojson = lga_geojson_data,
        locations = 'LGA_NAME',
        featureidkey = "properties.LGA_NAME",
        color = 'ACCIDENT_COUNT',
        color_continuous_scale = px.colors.sequential.Darkmint,
        range_color = [accidents_df['ACCIDENT_COUNT'].min(), accidents_df['ACCIDENT_COUNT'].max()],
        center = melbourne_coordinates,
        mapbox_style = "open-street-map",
        zoom = 8,
        labels = {'ACCIDENT_COUNT': '# Accidents',
                  'LGA_NAME': 'LGA Name'},
        hover_name = accidents_df['LGA_NAME'].apply(lambda x: x.capitalize()),
        hover_data = {'LGA_NAME': False},
        height = 800
    )

    # Serialise plotly graph to JSON
    choropleth_map_serialised = json.dumps(choropleth_map, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('insights.html', plot = choropleth_map_serialised)
