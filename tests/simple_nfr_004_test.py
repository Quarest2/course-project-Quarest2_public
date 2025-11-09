# !/usr/bin/env python3
"""
Тест NFR-004: Безопасность данных
"""
import requests


def test_nfr_004_security():
    """NFR-004: Безопасность данных"""
    print("🔒 Testing NFR-004: Data Security")
    print("=" * 50)

    base_url = "http://localhost:8000"

    # Тест 1: Security headers
    print("1. Testing Security Headers...")
    response = requests.get(f"{base_url}/health")

    security_headers = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Strict-Transport-Security': None,  # Должен присутствовать
    }

    missing_headers = []
    for header, expected_value in security_headers.items():
        if header in response.headers:
            if expected_value and response.headers[header] != expected_value:
                print(f"   ❌ {header}: Wrong value")
            else:
                print(f"   ✅ {header}: Present")
        else:
            print(f"   ❌ {header}: Missing")
            missing_headers.append(header)

    # Тест 2: SQL injection protection
    print("\n2. Testing SQL Injection Protection...")
    sql_payloads = [
        "1; DROP TABLE users; --",
        "' OR '1'='1",
        "'; SELECT * FROM users; --"
    ]

    sql_vulnerabilities = 0
    for payload in sql_payloads:
        try:
            response = requests.get(f"{base_url}/api/v1/features?search={payload}", timeout=5)
            if response.status_code == 500:
                print(f"   ❌ SQLi vulnerability: {payload}")
                sql_vulnerabilities += 1
            else:
                print(f"   ✅ SQLi protected: {payload}")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")

    # Тест 3: Input validation
    print("\n3. Testing Input Validation...")
    invalid_inputs = [
        {"feature_id": -1},
        {"feature_id": 0},
        {"feature_id": "invalid"},
    ]

    validation_issues = 0
    for invalid_input in invalid_inputs:
        try:
            response = requests.post(f"{base_url}/api/v1/votes", json=invalid_input, timeout=5)
            if response.status_code not in [400, 422]:  # Should be validation error
                print(f"   ❌ Missing validation: {invalid_input}")
                validation_issues += 1
            else:
                print(f"   ✅ Proper validation: {invalid_input}")
        except Exception as e:
            print(f"   ⚠️  Error: {e}")

    # Итоги
    print("\n📊 NFR-004 SECURITY RESULTS:")
    print("=" * 40)
    print(f"Security Headers: {len(security_headers) - len(missing_headers)}/{len(security_headers)}")
    print(f"SQL Injection Protection: {len(sql_payloads) - sql_vulnerabilities}/{len(sql_payloads)}")
    print(f"Input Validation: {len(invalid_inputs) - validation_issues}/{len(invalid_inputs)}")

    if not missing_headers and sql_vulnerabilities == 0 and validation_issues == 0:
        print("✅ NFR-004: PASS - Security requirements met!")
        return True
    else:
        print("❌ NFR-004: FAIL - Security issues detected")
        return False


if __name__ == "__main__":
    success = test_nfr_004_security()
    exit(0 if success else 1)