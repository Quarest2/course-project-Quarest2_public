import asyncio
import statistics
import time

import aiohttp
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


async def make_async_request(session, url):
    """Асинхронный запрос для тестирования пропускной способности"""
    start_time = time.time()
    async with session.get(url) as response:
        end_time = time.time()
        return {
            "status": response.status,
            "duration": (end_time - start_time) * 1000,
            "success": response.status == 200,
        }


async def test_nfr_002_throughput():
    """NFR-002: Упрощенная проверка пропускной способности"""
    base_url = "http://localhost:8000"  # Запустите приложение перед тестом
    endpoint = "/api/v1/health"

    async with aiohttp.ClientSession() as session:
        # Делаем 100 параллельных запросов
        tasks = [make_async_request(session, base_url + endpoint) for _ in range(100)]
        results = await asyncio.gather(*tasks)

        successful_requests = sum(1 for r in results if r["success"])
        durations = [r["duration"] for r in results if r["success"]]

        # Проверяем что можем обработать много параллельных запросов
        success_rate = successful_requests / len(results)
        avg_duration = statistics.mean(durations) if durations else 0

        print(f"Success rate: {success_rate:.1%}")
        print(f"Average duration: {avg_duration:.2f}ms")
        print(f"Successful requests: {successful_requests}/{len(results)}")

        assert success_rate >= 0.95, f"NFR-002: Success rate too low: {success_rate}"
        assert (
            avg_duration <= 200
        ), f"NFR-001: Average duration too high: {avg_duration}ms"


def test_nfr_001_response_time():
    """NFR-001: Проверка времени ответа для основных эндпоинтов"""
    endpoints = ["/api/v1/health", "/api/v1/features", "/api/v1/votes"]

    for endpoint in endpoints:
        response_times = []
        for _ in range(50):  # 50 запросов на эндпоинт
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()

            if response.status_code == 200:
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)

        if response_times:
            p95 = statistics.quantiles(response_times, n=100)[94]
            print(f"{endpoint}: p95 = {p95:.2f}ms")
            assert p95 <= 200, f"NFR-001 Violation for {endpoint}: p95 = {p95:.2f}ms"
