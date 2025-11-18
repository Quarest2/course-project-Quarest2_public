from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_nfr_005_input_validation():
    """NFR-005: Валидация входных данных"""

    # Тест невалидных данных
    invalid_payloads = [
        {"feature_id": ""},  # Пустое поле
        {"feature_id": "a" * 1000},  # Слишком длинное
        {"feature_id": "<script>alert('xss')</script>"},  # XSS
        {"user_id": -1},  # Отрицательное значение
    ]

    for payload in invalid_payloads:
        response = client.post("/api/v1/vote", json=payload)
        # Должна быть ошибка валидации (422 или 400)
        assert response.status_code in [
            400,
            422,
        ], f"Missing validation for payload: {payload}"

        # Проверяем что ошибка содержит детали
        assert "detail" in response.json()
