import json
from app import app, connection, get_splits
from sql_queries import *
from .utils import contains_all

def test_existing_computation_written_once(client):
    data = {
        "building_limits": """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 0],
                            [30, 0],
                            [30, 10],
                            [10, 10],
                            [10, 0]
                        ]
                    ]
                }
            }]
        }""",
        "height_plateaus": """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {
                    "elevation": 1.25
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 0],
                            [30, 0],
                            [30, 10],
                            [10, 10],
                            [10, 0]
                        ]
                    ]
                }
            }]
        }"""
    }
    
    row_count = get_row_count()

    # Test that a computation is persisted
    response = client.post("/splits", data = data)
    assert response.status_code == 200
    assert get_row_count() == row_count + 1

    # Test that same computation is not persisted as a new row
    response2 = client.post("/splits", data = data)
    assert response2.status_code == 200
    assert get_row_count() == row_count + 1

def test_correct_computation_is_persisted(client):
    building_limits = """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 0],
                            [30, 0],
                            [30, 10],
                            [10, 10],
                            [10, 0]
                        ]
                    ]
                }
            }]
        }"""
    height_plateaus = """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {
                    "elevation": 1.25
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 0],
                            [30, 0],
                            [30, 10],
                            [10, 10],
                            [10, 0]
                        ]
                    ]
                }
            }]
        }"""
    data = {
        "building_limits": building_limits,
        "height_plateaus": height_plateaus,
    }

    response = client.post("/splits", data = data)
    assert response.status_code == 200
    
    persisted_computation = get_splits(json.loads(building_limits), json.loads(height_plateaus))
    assert persisted_computation['type'] == 'FeatureCollection'
    
    features = persisted_computation['features'] 
    assert len(features) == 1
    assert features[0]['properties']['elevation'] == 1.25
    assert contains_all(features[0]['geometry']['coordinates'][0], [[10, 0],[30, 0],[30, 10],[10, 10],[10, 0]])

def get_row_count():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_ROWS)
            row = cursor.fetchone()
            if row == None or len(row) == 0:
                return 0
            return row[0]
