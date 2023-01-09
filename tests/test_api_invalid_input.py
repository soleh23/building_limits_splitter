def test_height_plateaus_dont_cover_building_limits(client):
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
                            [0, 0],
                            [0, 1],
                            [1, 1],
                            [1, 0]
                        ]
                    ]
                }
            }]
        }"""
    })
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Height plateaus do not fully cover building limits"

def test_building_limits_with_overlapping_area(client):
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
                            [2, 0],
                            [2, 2],
                            [0, 2],
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
                            [0, 0],
                            [1, 0],
                            [1, 1],
                            [0, 1],
                            [0, 0]
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
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Building limits have overlapping area"
