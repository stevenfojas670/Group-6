"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
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

    # Steven Fojas
    def minecraft_counter(self, client):
        # Creates a counter on the minecraft endpoint

        result = client.post('/minecraft/steve')
        assert result.status_code == status.HTTP_201_CREATED

    #Jacob Kasbohm
    def prevent_duplicate_counters(self, client):
        """It should prevent duplicate counters"""

        # Create first counter
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

        # Try creating the same counter again
        result = client.post('/counters/foo')
        
        # Assert that the status code returned is 409 (Conflict)
        assert result.status_code == status.HTTP_409_CONFLICT
        assert result.json == {"error": "Counter foo already exists"}

    def test_retrieve_an_existing_counter(self, client):
        testCounterName = 'test'
        client.post('/counters/'+testCounterName)
        response = client.get('/counters/'+testCounterName)

        assert response.status_code == status.HTTP_200_OK
        assert bytes('[{"'+testCounterName,'utf-8') in response.data

    def test_prevent_updating_non_existent_counter(self, client):
        # This test should not increment a counter that doesn't exist
        counter = client.put('/counters/non_existent_counter')
        # Assert that we get a 409 error from the PUT request
        assert counter.status_code == status.HTTP_409_CONFLICT

    #eli rosales
    def test_delete_a_counter(self, client):
        """It should delete a counter"""
        counter = client.delete('/counters/foo')
        assert counter.status_code == status.HTTP_404_NOT_FOUND

    # Jesse Ortega
    def test_prevent_deletion_non_existent_counter(self, client):
        # This test should attempt to delete a counter that doesn't exist
        counter = client.delete('/counters/non_existent_counter')
        # Assert that we get a 409 error from the DELETE request
        assert counter.status_code == status.HTTP_409_CONFLICT

    #Ernesto Dones
    def test_reset_all_counter(self, client):
        #creating dummy counters for the test
        client.post('/counters/foo')    
        client.post('/counters/fooo')
        client.post('/counters/foooo')

        #here we will call the function (in account.py) that 
        #clear the tokens 
        response = client.post('/counters/reset')
        #if this errors then we out
        assert response.status_code == status.HTTP_200_OK

        #if this "Counters reseted" string exist in the response body
        #then we know our fucntion was executed, else we must error out
        assert bytes("Counters reseted", "utf-8") in response.data

        #we know the fucntion in account.py executed, now we need to retrieve the counters to 
        #make sure they actually were erased 
        response = client.get('/counters/')

        #the response.data message should be empty cuz now all the counters has been reseted
        assert bytes("", "utf-8") in response.data



