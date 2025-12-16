"""Tests for secrets management (ADR-002)"""

import os
from unittest.mock import patch

import pytest

from app.core.secrets import SecretsManager


class TestSecretsManagement:
    """Test secrets manager functionality"""

    def test_get_secret_success(self):
        """Test successful secret retrieval"""
        with patch.dict(os.environ, {"TEST_SECRET": "test_value"}):
            manager = SecretsManager()
            result = manager.get_secret("TEST_SECRET")
            assert result == "test_value"

    def test_get_secret_with_default(self):
        """Test secret retrieval with default value"""
        manager = SecretsManager()
        result = manager.get_secret("MISSING_SECRET", default="default_value")
        assert result == "default_value"

    def test_get_secret_missing(self):
        """Test error when secret is missing"""
        manager = SecretsManager()
        with pytest.raises(ValueError) as exc_info:
            manager.get_secret("MISSING_SECRET")

        error_msg = str(exc_info.value)
        assert "not found" in error_msg.lower()
        assert "MISSING_SECRET" not in error_msg

    def test_mask_secret_short(self):
        """Test masking of short secrets"""
        manager = SecretsManager()
        result = manager.mask_secret("short")
        assert result == "***"

    def test_mask_secret_long(self):
        """Test masking of long secrets"""
        manager = SecretsManager()
        result = manager.mask_secret("very_long_secret_key_12345")
        assert result == "ve***45"

    def test_mask_secret_custom_length(self):
        """Test masking with custom visible characters"""
        manager = SecretsManager()
        result = manager.mask_secret("my_secret_password", visible_chars=4)
        assert result == "my_s***word"

    def test_negative_scenario_empty_secret(self):
        """Test error handling with empty secret value"""
        with patch.dict(os.environ, {"EMPTY_SECRET": ""}):
            manager = SecretsManager()
            # Пустой секрет должен пройти (возвращает пустую строку)
            # но залогировать ошибку
            result = manager.get_secret("EMPTY_SECRET", default="")
            assert result == ""

    def test_get_jwt_secret(self):
        """Test JWT secret retrieval"""
        with patch.dict(os.environ, {"JWT_SECRET_KEY": "jwt_secret_123"}):
            manager = SecretsManager()
            result = manager.get_jwt_secret()
            assert result == "jwt_secret_123"

    def test_get_db_password(self):
        """Test database password retrieval"""
        with patch.dict(os.environ, {"DB_PASSWORD": "db_pass_456"}):
            manager = SecretsManager()
            result = manager.get_db_password()
            assert result == "db_pass_456"

    def test_get_encryption_key(self):
        """Test encryption key retrieval"""
        with patch.dict(os.environ, {"ENCRYPTION_KEY": "32_char_encryption_key_123456789012"}):
            manager = SecretsManager()
            result = manager.get_encryption_key()
            assert isinstance(result, bytes)
            assert len(result) >= 32

    def test_secrets_manager_singleton(self):
        """Test that secrets_manager is a singleton instance"""
        from app.core.secrets import secrets_manager
        assert isinstance(secrets_manager, SecretsManager)

        import app.core.secrets as secrets_module
        assert secrets_manager is secrets_module.secrets_manager

    def test_mask_data_for_logs_string(self):
        """Test masking secrets in strings for logs"""
        manager = SecretsManager()

        test_string = "Connection string: password=supersecret; user=admin"
        masked = manager.mask_data_for_logs(test_string)

        assert "password=supersecret" not in masked
        assert "***" in masked