#!/usr/bin/env python3
"""
Скрипт для запуска приложения перед тестированием
"""
import subprocess
import sys
import time
from pathlib import Path

import requests

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def start_application():
    """Запуск FastAPI приложения"""
    print("🚀 Starting FastAPI application...")

    try:
        # Запускаем uvicorn как Python модуль
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",
            ],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Даем приложению время на запуск
        print("⏳ Waiting for application to start (5 seconds)...")
        time.sleep(5)

        # Проверяем что приложение запустилось
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=10)
            if response.status_code == 200:
                print("✅ Application started successfully!")
                print("📡 API available at: http://localhost:8000")
                print("📚 Docs available at: http://localhost:8000/docs")
                return process
            else:
                print(f"❌ Application not healthy. Status: {response.status_code}")
                print(f"Response: {response.text}")
                process.terminate()
                return None
        except requests.RequestException as e:
            print(f"❌ Application not responding: {e}")
            # Попробуем прочитать stderr для диагностики
            try:
                stderr_output = process.stderr.read()
                if stderr_output:
                    print("STDERR Output:")
                    print(stderr_output)
            except Exception:
                pass
            process.terminate()
            return None

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return None


def stop_application(process):
    """Остановка приложения"""
    if process:
        print("🛑 Stopping application...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Application stopped")


def check_application():
    """Проверка что приложение работает"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Application is running")
            return True
        else:
            print(f"❌ Application not healthy. Status: {response.status_code}")
            return False
    except requests.RequestException:
        print("❌ Application is not running")
        return False


if __name__ == "__main__":
    print("FastAPI Application Manager")

    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            process = start_application()
            if process:
                print("\n💡 Application is running in background.")
                print("   Use 'python scripts/start_app.py stop' to stop it.")
                print("   Or run 'python scripts/start_app.py test' to run tests.")
        elif sys.argv[1] == "stop":
            # Для остановки нужно найти процесс uvicorn
            print("🔍 Looking for running uvicorn processes...")
            try:
                subprocess.run(["pkill", "-f", "uvicorn"])
                print("✅ Stopped uvicorn processes")
            except Exception:
                print("❌ Failed to stop processes")
        elif sys.argv[1] == "test":
            process = start_application()
            if process:
                try:
                    # Даем дополнительное время для полного запуска
                    time.sleep(2)

                    # Запускаем тесты
                    print("\n🧪 Running NFR compliance tests...")
                    subprocess.run([sys.executable, "scripts/check_nfr_compliance.py"])

                    print("\n🔍 Testing all endpoints...")
                    subprocess.run([sys.executable, "scripts/test_all_endpoints.py"])

                finally:
                    stop_application(process)
        elif sys.argv[1] == "status":
            check_application()
    else:
        print("Usage: python scripts/start_app.py [start|stop|test|status]")
        print("\nCommands:")
        print("  start  - Start the application")
        print("  stop   - Stop the application")
        print("  test   - Start app, run tests, then stop app")
        print("  status - Check if application is running")
