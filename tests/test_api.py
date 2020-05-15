import time

import pytest
from flask import json

from app import create_app

API_KEY = "3ekTxXeyh6cb5fJGkGt0bgFhHtwUy0ov"


@pytest.fixture
def client():
    """Configures application for testing"""
    application = create_app(testing=True)
    application.config["TESTING"] = True
    client = application.test_client()

    yield client


def test_valid_api(client):
    """Tests basic valid API functionality"""
    ticker = "AAPL"
    timestamp = time.time()

    response = client.get(f"/api/1.0/{ticker}?key={API_KEY}")
    data = json.loads(response.data)

    assert data["ticker"] == ticker
    assert data["timestamp"] >= timestamp  # timestamp should at least be greater
    assert response.content_type == "application/json"


def test_invalid_ticker(client):
    """Tests basic invalid API functionality"""
    ticker = "invalid_ticker"
    timestamp = time.time()

    response = client.get(f"/api/1.0/{ticker}?key={API_KEY}")
    data = json.loads(response.data)

    assert "error" in data
    assert data["ticker"] == ticker
    assert data["timestamp"] >= timestamp  # timestamp should at least be greater


def test_invalid_key(client):
    """Tests basic invalid API functionality"""
    ticker = "invalid_ticker"
    timestamp = time.time()

    response = client.get(f"/api/1.0/{ticker}?key=bad-key")
    data = json.loads(response.data)

    assert "error" in data
    assert data["timestamp"] >= timestamp  # timestamp should at least be greater
