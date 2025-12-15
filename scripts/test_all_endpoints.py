#!/usr/bin/env python3
"""
Тестирование всех эндпоинтов приложения
"""

import requests

BASE_URL = "http://localhost:8000"


def test_endpoint(method, path, payload=None):
    """Тестирование отдельного эндпоинта"""
    try:
        url = BASE_URL + path
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=payload)
        else:
            print(f"❌ Unknown method: {method}")
            return False

        print(f"{method} {path}: {response.status_code}")
        if response.status_code not in [200, 201]:
            print(f"   Response: {response.text}")

        return response.status_code in [200, 201]

    except Exception as e:
        print(f"❌ Error testing {method} {path}: {e}")
        return False


def main():
    """Тестирование всех эндпоинтов"""
    print("🔍 Testing all API endpoints...")
    print("BASE_URL:", BASE_URL)

    endpoints = [
        ("GET", "/"),
        ("GET", "/health"),
        ("GET", "/api/v1/features"),
        ("GET", "/api/v1/features/1"),
        ("GET", "/api/v1/votes"),
        ("POST", "/api/v1/votes", {"feature_id": 1}),
    ]

    results = []
    for endpoint in endpoints:
        method = endpoint[0]
        path = endpoint[1]
        payload = endpoint[2] if len(endpoint) > 2 else None

        success = test_endpoint(method, path, payload)
        results.append((f"{method} {path}", success))

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
    else:
        print("⚠️  Some endpoints need attention")


if __name__ == "__main__":
    main()
