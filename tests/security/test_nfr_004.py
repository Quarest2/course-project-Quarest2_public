from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestNFR004Security:
    """NFR-004: Безопасность данных"""

    def test_sql_injection_protection(self):
        """Защита от SQL injection"""
        sql_injection_payloads = [
            "1; DROP TABLE features; --",
            "' OR '1'='1",
            "'; EXEC sp_msforeachtable 'DROP TABLE ?'; --",
        ]

        for payload in sql_injection_payloads:
            response = client.get(f"/api/v1/features?search={payload}")
            # Не должно быть 500 ошибок - признак успешной инъекции
            assert (
                response.status_code != 500
            ), f"SQL injection vulnerability: {payload}"

    def test_tls_headers(self):
        """Проверка security headers"""
        response = client.get("/api/v1/health")

        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Strict-Transport-Security": None,  # Должен присутствовать
        }

        for header, expected_value in security_headers.items():
            assert header in response.headers, f"Missing security header: {header}"
            if expected_value:
                assert response.headers[header] == expected_value
