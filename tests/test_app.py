import pytest

from app import create_app


@pytest.fixture
def client():
    """Configures application for testing"""
    application = create_app(testing=True)
    application.config["TESTING"] = True
    client = application.test_client()

    yield client


def test_routes(client):
    """Test basic app routing functionality"""
    response = client.get("/")
    assert response.status_code == 200
    response = client.get("/about")
    assert response.status_code == 200
    response = client.get("/api")
    assert response.status_code == 200
    response = client.get("/invalid_url")
    assert response.status_code == 302
