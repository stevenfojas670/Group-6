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

    def test_reset_counters(self, client):
        """This is a test case for the counters/reset endpoint. It should reset all counters.
        I think I need to check that it resets everything in the COUNTERS dictionary defined above."""

        # Create some counters. More than one bc I wanna check if I can reset ALL counters
        client.post('/counters/hehe')
        client.post('/counters/haha')

        # I wanted to check that the counters are created, but id need to wait for another student to implement that
        '''result_he = client.get('/counters/hehe')
        result_ha = client.get('/counters/haha')
        # First verify counters were created
        assert result_he.status_code == 200
        assert result_ha.status_code == 200'''

        # Test the counter reset function
        result_reset = client.post('/counters/reset')
        # Assuming OK status code for successful reset
        assert result_reset.status_code == status.HTTP_200_OK

        # Can't check with .get() because I don't have access to it
        # Try to create the counters again. This won't work if they weren't reset
        result_new_he = client.post('/counters/hehe')
        result_new_ha = client.post('/counters/haha')

        # Ensure the creation succeeds (201 Created), meaning they were reset
        assert result_new_he.status_code == status.HTTP_201_CREATED
        assert result_new_ha.status_code == status.HTTP_201_CREATED

        # Clear the counters again, so it doesn't mess with anyone else's tests
        client.post('/counters/reset')

