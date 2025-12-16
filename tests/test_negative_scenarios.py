"""Negative scenario tests for secure coding practices (ADR-001, ADR-002, ADR-003)"""

import pytest
from fastapi.testclient import TestClient

from app.core.currency_utils import CurrencyNormalizer
from app.core.datetime_utils import DateTimeNormalizer
from app.core.secrets import SecretsManager
from app.main import app

client = TestClient(app)

class TestNegativeScenarios:
    """Test negative scenarios for security and robustness"""

    def test_large_file_upload_attempt(self):
        """Test handling of extremely large file upload attempt"""
        large_payload = {
            "title": "x" * 10000,
            "notes": "x" * 100000,
            "price_estimate": 100.0,
        }

        response = client.post("/feature", json=large_payload)

        assert response.status_code == 422
        assert response.headers["content-type"] == "application/problem+json"

        error_data = response.json()
        assert error_data["status"] == 422
        assert "validation" in error_data["type"].lower()

    def test_path_traversal_attempt(self):
        """Test handling of path traversal attempts"""
        traversal_payload = "../../../etc/passwd" + "x" * 200

        response = client.post("/feature", json={"title": traversal_payload})

        assert response.status_code == 422
        error_data = response.json()
        assert "validation" in error_data["type"].lower()

    def test_sql_injection_attempt(self):
        """Test handling of SQL injection attempts"""
        sql_payload = "'; DROP TABLE feature; --" + "x" * 200

        response = client.post("/feature", json={"title": sql_payload})

        assert response.status_code == 422
        error_data = response.json()
        assert "validation" in error_data["type"].lower()

    def test_xss_attempt(self):
        """Test handling of XSS attempts"""
        xss_payload = "<script>alert('xss')</script>" + "x" * 200

        response = client.post("/feature", json={"title": xss_payload})

        assert response.status_code == 422
        error_data = response.json()
        assert "validation" in error_data["type"].lower()

    def test_secrets_in_logs_prevention(self):
        """Test that secrets are masked in logs"""
        manager = SecretsManager()

        secret_patterns = [
            "password=secret123",
            "secret_key=abc123def456",
            "api_key=sk-1234567890abcdef",
        ]

        for pattern in secret_patterns:
            masked = manager.mask_secret(pattern)
            assert "***" in masked
            assert pattern not in masked

    def test_currency_injection_attempts(self):
        """Test handling of malicious currency inputs"""
        malicious_currency_inputs = [
            "'; DROP TABLE features; --",
            "<script>alert('xss')</script>",
            "../../../etc/passwd",
        ]

        for malicious_input in malicious_currency_inputs:
            with pytest.raises(Exception):
                CurrencyNormalizer.normalize_amount(malicious_input, "USD")

    def test_datetime_injection_attempts(self):
        """Test handling of malicious datetime inputs"""
        malicious_datetime_inputs = [
            "'; DROP TABLE features; --",
            "<script>alert('xss')</script>",
            "2025-13-45T25:70:80Z",
        ]

        for malicious_input in malicious_datetime_inputs:
            with pytest.raises(Exception):
                DateTimeNormalizer.parse_iso(malicious_input)

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON"""
        malformed_json_payloads = [
            '{"title": "test", "price": }',
            '{"title": "test", "price": 100',
            '{"title": "test", "price": 100,}',
        ]

        for payload in malformed_json_payloads:
            response = client.post(
                "/feature", data=payload, headers={"Content-Type": "application/json"}
            )

            assert response.status_code == 422
            assert response.headers["content-type"] == "application/problem+json"
