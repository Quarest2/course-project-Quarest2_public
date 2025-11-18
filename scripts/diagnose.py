#!/usr/bin/env python3
"""
Диагностика проблем приложения
"""
import os
import sys
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔧 Application Diagnostics")
print("=" * 50)
print(f"Project root: {project_root}")
print(f"Python path: {sys.executable}")
print(f"Working directory: {os.getcwd()}")

# Проверяем импорты
print("\n📦 Checking imports...")
try:
    from app.main import app

    print("✅ app.main import: SUCCESS")
except Exception as e:
    print(f"❌ app.main import: FAILED - {e}")
    sys.exit(1)

try:

    print("✅ app.routers.features import: SUCCESS")
except Exception as e:
    print(f"❌ app.routers.features import: FAILED - {e}")
    sys.exit(1)

try:

    print("✅ app.services.monitoring import: SUCCESS")
except Exception as e:
    print(f"❌ app.services.monitoring import: FAILED - {e}")
    sys.exit(1)

try:

    print("✅ app.schemas.feature import: SUCCESS")
except Exception as e:
    print(f"❌ app.schemas.feature import: FAILED - {e}")
    sys.exit(1)

# Проверяем что приложение можно создать
print("\n🚀 Testing application creation...")
try:
    from fastapi.testclient import TestClient

    client = TestClient(app)
    print("✅ TestClient creation: SUCCESS")

    # Тестируем корневой эндпоинт
    response = client.get("/")
    print(f"✅ Root endpoint test: {response.status_code}")

    # Тестируем health endpoint
    response = client.get("/health")
    print(f"✅ Health endpoint test: {response.status_code}")

except Exception as e:
    print(f"❌ Application test: FAILED - {e}")
    sys.exit(1)

print("\n🎉 All diagnostics passed! Application should work correctly.")
print("💡 Run: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
