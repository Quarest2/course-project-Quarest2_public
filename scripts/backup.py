#!/usr/bin/env python3
"""
Простой скрипт бэкапа для NFR-008
"""
import json
from datetime import datetime
from pathlib import Path


def create_backup():
    """Создание бэкапа данных"""
    backup_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups") / backup_time
    backup_dir.mkdir(parents=True, exist_ok=True)

    # В реальном приложении здесь будет бэкап базы данных
    # Сейчас создаем файл с метаданными
    backup_info = {
        "timestamp": backup_time,
        "backup_type": "manual",
        "version": "1.0.0",
        "description": "Feature Votes API Backup",
    }

    with open(backup_dir / "backup_info.json", "w") as f:
        json.dump(backup_info, f, indent=2)

    print(f"✅ Backup created: {backup_dir}")
    return backup_dir


if __name__ == "__main__":
    create_backup()
