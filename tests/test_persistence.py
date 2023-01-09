from app import app, connection
from sql_queries import *

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
    
    row_count = getRowCount()

    # Test that a computation is persisted
    response = client.post("/splits", data = data)
    assert response.status_code == 200
    assert getRowCount() == row_count + 1

    # Test that same computation is not persisted as a new row
    response2 = client.post("/splits", data = data)
    assert response2.status_code == 200
    assert getRowCount() == row_count + 1

def getRowCount():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_ROWS)
            row = cursor.fetchone()
            if row == None or len(row) == 0:
                return 0
            return row[0]
