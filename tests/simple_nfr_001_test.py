#!/usr/bin/env python3
"""
Упрощенный тест NFR-001 без проблем импорта
"""
import time
import statistics
import requests


def test_nfr_001_performance():
    """NFR-001: Производительность - время ответа ≤ 200ms"""
    print("🧪 Testing NFR-001: Performance (Response time ≤ 200ms)")
    print("=" * 50)

    base_url = "http://localhost:8000"
    endpoints = [
        "/health",
        "/api/v1/features",
        "/api/v1/votes"
    ]

    all_response_times = []

    for endpoint in endpoints:
        print(f"📊 Testing {endpoint}...")
        response_times = []

        # Делаем 10 запросов для статистики
        for i in range(10):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                end_time = time.time()

                response_time = (end_time - start_time) * 1000  # в миллисекундах

                if response.status_code == 200:
                    response_times.append(response_time)
                    status = "✅"
                else:
                    status = "❌"

                print(f"  Request {i + 1}: {status} {response_time:.2f}ms (Status: {response.status_code})")

            except Exception as e:
                print(f"  Request {i + 1}: 💥 ERROR - {e}")

        # Анализируем результаты для эндпоинта
        if response_times:
            avg_time = statistics.mean(response_times)
            p95_time = statistics.quantiles(response_times, n=100)[94] if len(response_times) >= 5 else max(
                response_times)
            all_response_times.extend(response_times)

            print(f"  📈 {endpoint} Results:")
            print(f"    - Average: {avg_time:.2f}ms")
            print(f"    - 95th percentile: {p95_time:.2f}ms")
            print(f"    - Samples: {len(response_times)}/10")

            # Проверяем NFR-001 для этого эндпоинта
            if p95_time <= 200:
                print(f"    - NFR-001: ✅ PASS")
            else:
                print(f"    - NFR-001: ❌ FAIL (>{200}ms)")

        print()

    # Общий анализ
    if all_response_times:
        overall_avg = statistics.mean(all_response_times)
        overall_p95 = statistics.quantiles(all_response_times, n=100)[94]

        print("🎯 OVERALL PERFORMANCE RESULTS:")
        print("=" * 40)
        print(f"Total requests analyzed: {len(all_response_times)}")
        print(f"Average response time: {overall_avg:.2f}ms")
        print(f"95th percentile (p95): {overall_p95:.2f}ms")
        print(f"NFR-001 Threshold: ≤ 200ms")

        if overall_p95 <= 200:
            print("✅ NFR-001: PASS - Performance requirements met!")
            return True
        else:
            print("❌ NFR-001: FAIL - Performance requirements not met")
            return False
    else:
        print("❌ No successful requests to analyze")
        return False


if __name__ == "__main__":
    success = test_nfr_001_performance()
    exit(0 if success else 1)