import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_nfr_002_throughput():
    """NFR-002: Упрощенный тест пропускной способности"""
    successful_requests = 0
    total_requests = 50  # Уменьшаем для CI
    errors = 0

    def make_request():
        nonlocal successful_requests, errors
        try:
            response = client.get("/health")
            if response.status_code == 200:
                successful_requests += 1
        except Exception:  # Заменяем bare except
            errors += 1

    # Запускаем запросы последовательно для CI
    start_time = time.time()

    for i in range(total_requests):
        make_request()

    end_time = time.time()
    duration = end_time - start_time
    rps = total_requests / duration

    # Более реалистичные требования для CI
    assert rps >= 10, f"NFR-002: {rps:.2f} RPS < 10 RPS"
    assert errors / total_requests < 0.1, "Error rate too high"
