def check_nfr_001_performance(self):
    """NFR-001: Производительность"""
    if not APP_AVAILABLE:
        return "SKIP - App not available"

    try:
        # Тестируем health endpoint
        endpoint = "/api/v1/health"
        response_times = []

        for i in range(10):
            start = time.time()
            response = client.get(endpoint)
            end = time.time()

            print(f"Request {i + 1}: Status {response.status_code}, Time: {(end - start) * 1000:.2f}ms")

            if response.status_code == 200:
                response_times.append((end - start) * 1000)
            else:
                print(f"  Response: {response.text}")

        if response_times:
            if len(response_times) >= 5:
                p95 = statistics.quantiles(response_times, n=100)[94]
            else:
                p95 = max(response_times)

            status = "PASS" if p95 <= 200 else "FAIL"
            return f"{status} (p95: {p95:.2f}ms, samples: {len(response_times)}/10)"
        else:
            return "FAIL - No successful requests (check if app is running)"

    except Exception as e:
        return f"ERROR: {str(e)}"


def check_nfr_002_throughput(self):
    """NFR-002: Пропускная способность"""
    if not APP_AVAILABLE:
        return "SKIP - App not available"

    try:
        successful = 0
        total = 10

        for i in range(total):
            try:
                response = client.get("/api/v1/health")
                if response.status_code == 200:
                    successful += 1
                    print(f"Request {i + 1}: ✅ Success")
                else:
                    print(f"Request {i + 1}: ❌ Failed (Status: {response.status_code})")
            except Exception as e:
                print(f"Request {i + 1}: 💥 Exception: {e}")

        success_rate = successful / total
        status = "PASS" if success_rate >= 0.95 else "FAIL"
        return f"{status} ({successful}/{total} requests, rate: {success_rate:.1%})"
    except Exception as e:
        return f"ERROR: {str(e)}"