import pytest
from src import app
from src import status

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_retrieve_an_existing_counter(self, client):
        testCounterName = 'test'
        client.post('/counters/'+testCounterName)
        response = client.get('/counters/'+testCounterName)

        assert response.status_code == status.HTTP_200_OK
        assert bytes('[{"'+testCounterName,'utf-8') in response.data
