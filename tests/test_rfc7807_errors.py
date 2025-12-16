import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRFC7807ErrorFormat:
    """Test RFC 7807 Problem Details format implementation"""

    def test_validation_error_format(self):
        """Test validation error returns RFC 7807 format"""
        response = client.post(
            "/feature",
            json={
                "title": "",
                "price_estimate": -100.0,
                "link": "https://example.com",
            },
        )

        assert response.status_code == 422
        assert response.headers["content-type"] == "application/problem+json"

        error_data = response.json()

        assert "type" in error_data
        assert "title" in error_data
        assert "status" in error_data
        assert "detail" in error_data
        assert "correlation_id" in error_data
        assert "timestamp" in error_data

        assert error_data["status"] == 422
        assert "validation" in error_data["type"].lower()

    def test_not_found_error_format(self):
        """Test not found error returns RFC 7807 format"""
        response = client.get("/feature/99999")

        assert response.status_code == 404
        assert response.headers["content-type"] == "application/problem+json"

        error_data = response.json()

        assert error_data["type"] is not None
        assert error_data["title"] is not None
        assert error_data["status"] == 404
        assert error_data["detail"] is not None
        assert error_data["correlation_id"] is not None
        assert error_data["timestamp"] is not None

    def test_correlation_id_presence(self):
        """Test that correlation_id is present in all error responses"""
        response = client.get("/feature/99999")

        error_data = response.json()
        correlation_id = error_data["correlation_id"]

        uuid.UUID(correlation_id)

        assert "X-Correlation-ID" in response.headers
        assert response.headers["X-Correlation-ID"] == correlation_id

    def test_negative_scenario_large_payload(self):
        """Test error handling with extremely large payload"""
        large_title = "x" * 1000

        response = client.post(
            "/feature",
            json={
                "title": large_title,
                "price_estimate": 100.0,
                "link": "https://example.com"
            }
        )

        assert response.status_code == 422
        assert response.headers["content-type"] == "application/problem+json"

        error_data = response.json()
        assert error_data["status"] == 422
        assert "validation" in error_data["type"].lower()

    def test_negative_scenario_invalid_json(self):
        """Test error handling with malformed JSON"""
        response = client.post(
            "/feature",
            data="invalid json{",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422
        assert response.headers["content-type"] == "application/problem+json"

        error_data = response.json()
        assert error_data["status"] == 422

    def test_successful_request_has_correlation_id(self):
        """Test that successful requests also have correlation_id header"""
        response = client.post(
            "/feature",
            json={
                "title": "Test Feature",
                "price_estimate": 100.0,
                "link": "https://example.com",
                "votes": 0
            }
        )

        assert "X-Correlation-ID" in response.headers
        correlation_id = response.headers["X-Correlation-ID"]

        uuid.UUID(correlation_id)

        print(f"✓ Successful request correlation_id: {correlation_id}")