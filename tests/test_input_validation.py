from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestInputValidation:
    """Тесты валидации ввода"""

    def test_empty_title_validation(self):
        """Негативный тест: пустой заголовок"""
        response = client.post(
            "/feature",
            json={
                "title": "",
                "link": "https://example.com",
                "price_estimate": 100.0,
                "votes": 0,
            },
        )
        assert response.status_code == 422
        error_data = response.json()
        assert "validation" in error_data["type"].lower()

    def test_negative_price_validation(self):
        """Негативный тест: отрицательная цена"""
        response = client.post(
            "/feature",
            json={
                "title": "Test Feature",
                "link": "https://example.com",
                "price_estimate": -10.0,
                "votes": 0,
            },
        )
        assert response.status_code == 422

    def test_negative_votes_validation(self):
        """Негативный тест: отрицательные голоса"""
        response = client.post(
            "/feature",
            json={
                "title": "Test Feature",
                "link": "https://example.com",
                "price_estimate": 100.0,
                "votes": -5,
            },
        )
        assert response.status_code == 422

    def test_long_title_validation(self):
        """Негативный тест: слишком длинный заголовок"""
        long_title = "A" * 201
        response = client.post(
            "/feature",
            json={
                "title": long_title,
                "link": "https://example.com",
                "price_estimate": 100.0,
                "votes": 0,
            },
        )
        assert response.status_code == 422

    def test_sql_injection_attempt(self):
        """Негативный тест: попытка SQL инъекции"""
        response = client.post(
            "/feature",
            json={
                "title": "Test'; DROP TABLE features; --",
                "link": "https://example.com",
                "price_estimate": 100.0,
                "votes": 0,
            },
        )
        assert response.status_code == 201

    def test_xss_attempt(self):
        """Негативный тест: попытка XSS"""
        response = client.post(
            "/feature",
            json={
                "title": "<script>alert('xss')</script>",
                "link": "javascript:alert(1)",
                "price_estimate": 100.0,
                "votes": 0,
            },
        )
        assert response.status_code in [201, 422]
