import threading
import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_nfr_002_throughput():
    """NFR-002: Поддержка ≥ 1000 RPS"""
    successful_requests = 0
    total_requests = 1000
    errors = 0

    def make_request():
        nonlocal successful_requests, errors
        try:
            response = client.get("/api/v1/health")
            if response.status_code == 200:
                successful_requests += 1
        except:
            errors += 1

    # Запускаем 1000 запросов параллельно
    threads = []
    start_time = time.time()

    for i in range(total_requests):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time
    rps = total_requests / duration

    assert rps >= 1000, f"NFR-002 Violation: {rps:.2f} RPS < 1000 RPS"
    assert errors / total_requests < 0.01, "Error rate too high"
