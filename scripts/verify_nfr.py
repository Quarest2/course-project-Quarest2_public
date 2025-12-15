#!/usr/bin/env python3
"""
Скрипт проверки соответствия всех NFR требований
"""
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Запуск всех NFR тестов"""
    print("🔍 Starting NFR Compliance Verification...")

    test_modules = [
        "tests/performance/test_nfr_001.py",
        "tests/performance/test_nfr_002.py",
        "tests/security/test_nfr_004.py",
        "tests/validation/test_nfr_005.py",
        "tests/monitoring/test_nfr_006.py",
    ]

    results = {}

    for test_module in test_modules:
        if Path(test_module).exists():
            print(f"\n📋 Running {test_module}...")
            try:
                result = subprocess.run(
                    ["pytest", test_module, "-v", "--tb=short"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                results[test_module] = result.returncode == 0
                print("✅ PASS" if result.returncode == 0 else "❌ FAIL")

            except subprocess.TimeoutExpired:
                print("⏰ TIMEOUT")
                results[test_module] = False
        else:
            print(f"📁 Missing: {test_module}")
            results[test_module] = False

    return results


def generate_report(results):
    """Генерация отчета о соответствии"""
    print("\n" + "=" * 50)
    print("📊 NFR COMPLIANCE REPORT")
    print("=" * 50)

    nfr_mapping = {
        "test_nfr_001": "NFR-001: Производительность",
        "test_nfr_002": "NFR-002: Пропускная способность",
        "test_nfr_004": "NFR-004: Безопасность данных",
        "test_nfr_005": "NFR-005: Валидация данных",
        "test_nfr_006": "NFR-006: Логирование",
    }

    passed = 0
    total = len(results)

    for test_file, success in results.items():
        nfr_name = "Unknown"
        for key, value in nfr_mapping.items():
            if key in test_file:
                nfr_name = value
                break

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {nfr_name}")
        if success:
            passed += 1

    print("=" * 50)
    compliance_rate = (passed / total) * 100
    print(f"Overall Compliance: {compliance_rate:.1f}% ({passed}/{total})")

    if compliance_rate >= 80:
        print("🎉 Project meets NFR requirements!")
        return True
    else:
        print("⚠️  Project needs improvement for NFR compliance")
        return False


if __name__ == "__main__":
    results = run_tests()
    success = generate_report(results)
    sys.exit(0 if success else 1)
