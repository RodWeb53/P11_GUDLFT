import pytest

from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


clubs_data = [{'name': 'Test Club 1', 'email': 'test@test.com', 'points': '12'},
              {'name': 'Test Club 2', 'email': 'test2@test.com', 'points': '13'}]
