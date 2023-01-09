import geopandas
import json
import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from sql_queries import *
from shapely import area

# Loads variables from .env file into environment
load_dotenv() 

app = Flask(__name__)
url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)

@app.route('/', methods=['GET'])
def ping():
    return "Alive"

@app.route('/splits', methods=['POST'])
def splits():
    """
    The endpoint calculate split building limits with corresponding
    elevation given building limits and height plateaus.

    """

    building_limits_raw = request.form['building_limits']
    height_plateaus_raw = request.form['height_plateaus']

    # Convert geojson string to json
    try:
        building_limits_json = json.loads(building_limits_raw)
        height_plateaus_json = json.loads(height_plateaus_raw)
    except:
        return "Invalid input format, should be a valid json", 400

    # Check if splits already exist
    computed_splits = get_splits(building_limits_json, height_plateaus_json)
    if computed_splits != None:
        return computed_splits

    # Convert to GeoDataFrame
    try:
        building_limits_gdf = geopandas.GeoDataFrame.from_features(building_limits_json)
        height_plateaus_gdf = geopandas.GeoDataFrame.from_features(height_plateaus_json)
    except:
        return "Invalid input format, should be a valid geojson containing feature collection", 400

    # Verify geometries are non empty
    if building_limits_gdf.geometry.any() == None or height_plateaus_gdf.geometry.any() == None:
        return "Invalid input format, invalid 'geometry' property found", 400
    
    building_limits = geopandas.GeoSeries(building_limits_gdf.geometry)
    height_plateaus = geopandas.GeoSeries(height_plateaus_gdf.geometry)

    if has_overlaps(building_limits):
        return "Building limits have overlapping area", 400
    
    if has_overlaps(height_plateaus):
        return "Height plateaus have overlapping area", 400

    # Check if height plateaus fully cover building limits
    # Pad by epsilon to account for rounding errors
    if not height_plateaus.unary_union.buffer(1e-6).contains(building_limits.unary_union):
        return "Height plateaus do not fully cover building limits", 400

    split_building_limits = height_plateaus_gdf.overlay(building_limits_gdf, how = 'intersection')
    split_building_limits_json_string = split_building_limits.to_json()

    # Persist results
    write_splits(building_limits_json, height_plateaus_json, split_building_limits_json_string)

    return split_building_limits_json_string

# Verifies if any geometry in geo series has any overlap with any other
# geometry in the same geoseries
def has_overlaps(geo_series):
    union_area = area(geo_series.unary_union)
    sum_area = sum(geo_series.area)

    # Use epsilon to account for rounding errors
    eps = 1e-6
    return abs(union_area - sum_area) > eps

def write_splits(building_limits_json, height_plateaus_json, split_building_limits_json_string):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_SPLITS_TABLE)
            cursor.execute(INSERT_SPLITS, (json.dumps(building_limits_json), json.dumps(height_plateaus_json), split_building_limits_json_string))

    return split_building_limits_json_string

def get_splits(building_limits_json, height_plateaus_json):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_SPLITS, (json.dumps(building_limits_json), json.dumps(height_plateaus_json)))
            row = cursor.fetchone()
            if row == None or len(row) == 0:
                return None
            return row[0]
            