"""
Сервис мониторинга и логирования для NFR-006
"""
import logging
import json
import time
import uuid
from contextlib import contextmanager
from typing import Dict, Any, Optional


class StructuredLogger:
    """Структурированный логгер для NFR-006"""

    def __init__(self, name: str = "quarest"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Настройка форматера для JSON логов
        formatter = logging.Formatter(
            json.dumps({
                'timestamp': '%(asctime)s',
                'level': '%(levelname)s',
                'logger': '%(name)s',
                'message': '%(message)s',
                'correlation_id': '%(correlation_id)s',
                'module': '%(module)s',
                'function': '%(funcName)s'
            }),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Обработчик для файла
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _log(self, level: int, message: str, correlation_id: Optional[str] = None, **kwargs):
        """Базовый метод логирования"""
        extra = {'correlation_id': correlation_id or str(uuid.uuid4())}
        extra.update(kwargs)
        self.logger.log(level, message, extra=extra)

    def info(self, message: str, correlation_id: Optional[str] = None, **kwargs):
        """Информационное сообщение"""
        self._log(logging.INFO, message, correlation_id, **kwargs)

    def error(self, message: str, correlation_id: Optional[str] = None, **kwargs):
        """Сообщение об ошибке"""
        self._log(logging.ERROR, message, correlation_id, **kwargs)

    def warning(self, message: str, correlation_id: Optional[str] = None, **kwargs):
        """Предупреждение"""
        self._log(logging.WARNING, message, correlation_id, **kwargs)

    def debug(self, message: str, correlation_id: Optional[str] = None, **kwargs):
        """Отладочное сообщение"""
        self._log(logging.DEBUG, message, correlation_id, **kwargs)


# Глобальный экземпляр логгера
logger = StructuredLogger()


@contextmanager
def track_performance(operation: str, correlation_id: Optional[str] = None):
    """
    Контекстный менеджер для трекинга производительности (NFR-001)

    Args:
        operation: Название операции для логирования
        correlation_id: ID для трассировки запроса
    """
    start_time = time.time()
    corr_id = correlation_id or str(uuid.uuid4())

    try:
        logger.info(f"Starting operation: {operation}",
                    correlation_id=corr_id,
                    operation=operation)
        yield corr_id
    except Exception as e:
        logger.error(f"Operation failed: {operation}",
                     correlation_id=corr_id,
                     operation=operation,
                     error=str(e),
                     error_type=type(e).__name__)
        raise
    finally:
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # ms

        logger.info(f"Operation completed: {operation}",
                    correlation_id=corr_id,
                    operation=operation,
                    duration_ms=round(duration, 2))

        # Логируем предупреждение если операция заняла слишком много времени (NFR-001)
        if duration > 200:
            logger.warning(f"Performance alert: {operation} took {duration:.2f}ms",
                           correlation_id=corr_id,
                           duration_ms=round(duration, 2),
                           threshold_ms=200,
                           exceeded_by=round(duration - 200, 2))


def setup_logging():
    """Настройка логирования для приложения"""
    # Эта функция может быть вызвана в main.py
    return logger