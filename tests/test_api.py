import json
from .utils import contains_all

def test_building_limits_equal_to_height_plateaus(client):
    response = client.post("/splits", data={
        "building_limits": """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1, 0],
                            [3, 0],
                            [3, 1],
                            [1, 1],
                            [1, 0]
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
                            [1, 0],
                            [3, 0],
                            [3, 1],
                            [1, 1],
                            [1, 0]
                        ]
                    ]
                }
            }]
        }"""
    })
    assert response.status_code == 200

    features = json.loads(response.data.decode('utf-8'))['features']
    assert len(features) == 1
    assert features[0]['properties']['elevation'] == 1.25
    assert contains_all(features[0]['geometry']['coordinates'][0], [[1, 0],[3, 0],[3, 1],[1, 1],[1, 0]])

def test_2_height_plateaus_cover_1_building_limit(client):
    response = client.post("/splits", data={
        "building_limits": """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [1, 0],
                            [3, 0],
                            [3, 1],
                            [1, 1],
                            [1, 0]
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
                            [0, 0],
                            [2, 0],
                            [2, 1],
                            [0, 1],
                            [0, 0]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "elevation": 0.75
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [2, 0],
                            [4, 0],
                            [4, 1],
                            [2, 1],
                            [2, 0]
                        ]
                    ]
                }
            }]
        }"""
    })
    assert response.status_code == 200

    features = json.loads(response.data.decode('utf-8'))['features']
    assert len(features) == 2

    assert features[0]['properties']['elevation'] == 1.25
    assert contains_all(features[0]['geometry']['coordinates'][0], [[1, 0],[2, 0],[2, 1],[1, 1],[1, 0]])

    assert features[1]['properties']['elevation'] == 0.75
    assert contains_all(features[1]['geometry']['coordinates'][0], [[2, 0],[3, 0],[3, 1],[2, 1],[2, 0]])

def test_1_height_plateau_covers_2_building_limits(client):
    response = client.post("/splits", data={
        "building_limits": """{
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0, 0],
                            [1, 0],
                            [1, 3],
                            [0, 3],
                            [0, 0]
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [2, 1],
                            [3, 1],
                            [3, 2],
                            [2, 2],
                            [2, 1]
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
                    "elevation": 0.5
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [0, 0],
                            [4, 0],
                            [4, 3],
                            [0, 3],
                            [0, 0]
                        ]
                    ]
                }
            }]
        }"""
    })
    assert response.status_code == 200

    features = json.loads(response.data.decode('utf-8'))['features']
    assert len(features) == 2

    assert features[0]['properties']['elevation'] == 0.5
    assert contains_all(features[0]['geometry']['coordinates'][0], [[0, 0],[1, 0],[1, 3],[0, 3],[0, 0]])

    assert features[1]['properties']['elevation'] == 0.5
    assert contains_all(features[1]['geometry']['coordinates'][0], [[2, 1],[3, 1],[3, 2],[2, 2],[2, 1]])
