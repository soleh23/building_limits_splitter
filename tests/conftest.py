import pytest
from app import app, connection
from sql_queries import *

@pytest.fixture()
def client():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ALL)

    yield app.test_client()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ALL)
