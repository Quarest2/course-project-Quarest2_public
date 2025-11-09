#!/usr/bin/env python3
"""
Исправленный тест всех эндпоинтов приложения
"""
import requests
import json

BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # seconds


def test_endpoint(method, path, payload=None):
    """Тестирование отдельного эндпоинта"""
    try:
        url = BASE_URL + path
        print(f"Testing {method} {url}...")

        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=payload, timeout=TIMEOUT)
        else:
            print(f"❌ Unknown method: {method}")
            return False

        print(f"   {method} {path}: {response.status_code}")

        if response.status_code not in [200, 201]:
            print(f"   Response: {response.text}")

        return response.status_code in [200, 201]

    except requests.exceptions.Timeout:
        print(f"❌ {method} {path}: TIMEOUT after {TIMEOUT}s")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {path}: CONNECTION REFUSED")
        return False
    except Exception as e:
        print(f"❌ {method} {path}: ERROR - {e}")
        return False


def main():
    """Тестирование всех эндпоинтов"""
    print("🔍 Testing all API endpoints...")
    print(f"BASE_URL: {BASE_URL}")
    print("=" * 50)

    endpoints = [
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/api/v1/features"),
        ("GET", "/api/v1/features/1"),
        ("GET", "/api/v1/votes"),
        ("POST", "/api/v1/votes", {"feature_id": 1, "user_id": "test_user"}),
    ]

    results = []
    for endpoint in endpoints:
        method = endpoint[0]
        path = endpoint[1]
        payload = endpoint[2] if len(endpoint) > 2 else None

        success = test_endpoint(method, path, payload)
        results.append((f"{method} {path}", success))
        print()  # пустая строка между тестами

    print("\n📊 Test Results:")
    print("=" * 50)
    for endpoint, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {endpoint}")

    total_success = sum(1 for _, success in results if success)
    success_rate = total_success / len(results) * 100
    print(f"\n🎯 Success rate: {total_success}/{len(results)} ({success_rate:.1f}%)")

    if success_rate == 100:
        print("🎉 All endpoints are working correctly!")
    elif success_rate == 0:
        print("💡 Application might not be running.")
    else:
        print("⚠️  Some endpoints need attention")

    return success_rate == 100


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)