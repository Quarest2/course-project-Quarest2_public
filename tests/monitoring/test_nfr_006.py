import logging
import json
from app.services.monitoring import logger


def test_nfr_006_structured_logging():
    """NFR-006: Структурированные логи"""

    # Перехватываем логи
    log_records = []

    class LogHandler(logging.Handler):
        def emit(self, record):
            log_records.append(self.format(record))

    handler = LogHandler()
    logger.logger.addHandler(handler)

    # Генерируем тестовый лог
    test_message = "Test structured log"
    logger.info(test_message, correlation_id="test-123", user_id=1)

    # Проверяем структуру
    assert len(log_records) > 0
    log_data = json.loads(log_records[-1])

    required_fields = ['timestamp', 'level', 'message', 'correlation_id']
    for field in required_fields:
        assert field in log_data, f"Missing field in structured log: {field}"

    assert log_data['correlation_id'] == "test-123"