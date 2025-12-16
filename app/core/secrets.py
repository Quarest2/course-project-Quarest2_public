"""Secrets management implementation (ADR-002)"""

import logging
import os
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class SecretsManager:
    """Centralized secrets management with security controls"""

    def __init__(self):
        self._cache: Dict[str, str] = {}
        self._secrets_logged = False
        self._forbidden_patterns = [
            r'password\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
            r'secret\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
            r'token\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
            r'api[_-]?key\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
            r'jwt\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
        ]

    def get_secret(self, key: str, default: Optional[str] = None) -> str:
        """Get secret from environment variables with security checks"""
        if key in self._cache:
            return self._cache[key]

        value = os.getenv(key)

        if value is None:
            if default is not None:
                value = default
                self._log_secret_access(key, "used_default")
            else:
                self._log_secret_access(key, "not_found")
                raise ValueError(
                    f"Secret '{self._mask_key(key)}' not found in environment"
                )
        else:
            self._log_secret_access(key, "found")

        self._validate_secret(key, value)

        self._cache[key] = value

        return value

    def get_jwt_secret(self) -> str:
        """Get JWT signing key with length validation"""
        secret = self.get_secret("JWT_SECRET_KEY")
        if len(secret) < 32:
            logger.warning(
                f"JWT secret is too short: {len(secret)} chars (recommended: >= 32)"
            )
        return secret

    def get_db_password(self) -> str:
        """Get database password"""
        return self.get_secret("DB_PASSWORD")

    def get_encryption_key(self) -> bytes:
        """Get encryption key with length validation"""
        key_str = self.get_secret("ENCRYPTION_KEY")
        if len(key_str) < 32:
            raise ValueError(
                f"Encryption key too short: {len(key_str)} chars (required: >= 32)"
            )
        return key_str.encode()

    def mask_secret(self, secret: str, visible_chars: int = 2) -> str:
        """Mask secret for logging"""
        if not secret or len(secret) <= visible_chars * 3:
            return "***"
        return secret[:visible_chars] + "***" + secret[-visible_chars:]

    def mask_data_for_logs(self, data: Any) -> Any:
        """Recursively mask secrets in any data structure for logging"""
        if isinstance(data, str):
            return self._mask_string(data)
        elif isinstance(data, dict):
            return {k: self.mask_data_for_logs(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.mask_data_for_logs(item) for item in data]
        else:
            return data

    def _mask_key(self, key: str) -> str:
        """Mask secret key name for logging"""
        parts = key.split("_")
        if len(parts) > 1:
            return f"{parts[0][:1]}...{parts[-1][:1]}"
        return key[:3] + "..." if len(key) > 6 else "***"

    def _mask_string(self, text: str) -> str:
        """Mask any secrets found in string"""
        masked = text
        for pattern in self._forbidden_patterns:
            masked = re.sub(
                pattern,
                lambda m: self.mask_secret(m.group(0)),
                masked,
                flags=re.IGNORECASE,
            )
        return masked

    def _log_secret_access(self, key: str, status: str):
        """Log secret access without exposing the value"""
        if not self._secrets_logged:
            masked_key = self._mask_key(key)
            logger.info(f"Secret access: {masked_key} - {status}")

    def _validate_secret(self, key: str, value: str):
        """Validate secret for common issues"""
        if not value or value.strip() == "":
            logger.error(f"Secret '{self._mask_key(key)}' is empty")

        if len(value) < 8 and "key" in key.lower():
            logger.warning(
                f"Secret '{self._mask_key(key)}' is too short: {len(value)} chars"
            )

        common_defaults = ["password", "secret", "changeme", "123456", "admin"]
        if value.lower() in common_defaults:
            logger.error(f"Secret '{self._mask_key(key)}' uses default/weak value")

    def detect_secrets_in_code(self, filepath: str) -> list:
        """Detect potential secrets in code files (for CI/CD)"""
        detected = []
        try:
            with open(filepath, "r") as f:
                content = f.read()

                for pattern in self._forbidden_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        detected.append(
                            {
                                "file": filepath,
                                "pattern": pattern,
                                "matches": len(matches),
                            }
                        )
        except Exception as e:
            logger.error(f"Error scanning {filepath}: {e}")

        return detected


secrets_manager = SecretsManager()
