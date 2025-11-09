import pytest
import time
import statistics
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_nfr_001_response_time():
    """NFR-001: 95% запросов ≤ 200ms"""
    endpoints_to_test = [
        "/api/v1/features",
        "/api/v1/votes",
        "/api/v1/health"
    ]

    response_times = []
    for endpoint in endpoints_to_test:
        for _ in range(100):  # 100 запросов на эндпоинт
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()

            assert response.status_code == 200
            response_time = (end_time - start_time) * 1000
            response_times.append(response_time)

    # Расчет 95 перцентиля
    p95 = statistics.quantiles(response_times, n=100)[94]
    assert p95 <= 200, f"NFR-001 Violation: p95 response time {p95:.2f}ms > 200ms"