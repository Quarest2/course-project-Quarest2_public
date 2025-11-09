#!/usr/bin/env python3
"""
Простой скрипт для запуска приложения
"""
import uvicorn
import sys
from pathlib import Path

# Добавляем корень проекта в Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("🚀 Starting FastAPI application...")
    print("📡 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )