#!/usr/bin/env python3
"""
Безопасный запуск приложения с проверкой порта
"""
import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def kill_process_on_port(port=8000):
    """Убить процесс на указанном порту"""
    try:
        # Находим PID процесса на порту
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"🛑 Killing process {pid} on port {port}")
                    subprocess.run(["kill", "-9", pid])
                    time.sleep(1)
            return True
        else:
            print(f"✅ Port {port} is free")
            return False
    except Exception as e:
        print(f"⚠️  Could not check port {port}: {e}")
        return False


def start_application(port=8000):
    """Запуск FastAPI приложения"""
    print(f"🚀 Starting FastAPI application on port {port}...")

    # Сначала освобождаем порт
    kill_process_on_port(port)

    try:
        # Запускаем uvicorn как Python модуль
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0",
            "--port", str(port)
        ],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)

        # Даем приложению время на запуск
        print(f"⏳ Waiting for application to start on port {port}...")
        time.sleep(3)

        # Проверяем что приложение запустилось
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ Application started successfully on port {port}!")
                print(f"📡 API available at: http://localhost:{port}")
                print(f"📚 Docs available at: http://localhost:{port}/docs")
                return process
            else:
                print(f"❌ Application not healthy. Status: {response.status_code}")
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
            except:
                pass
            process.terminate()
            return None

    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return None


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid port: {sys.argv[1]}, using default 8000")

    process = start_application(port)

    if process:
        print(f"\n💡 Application is running on http://localhost:{port}")
        print("   Press Ctrl+C to stop")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping application...")
            process.terminate()