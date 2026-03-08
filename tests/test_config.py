"""Unit tests for core configuration module."""

import os
from unittest.mock import patch

import pytest


def test_settings_default_values() -> None:
    """Test that settings have sensible defaults."""
    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "test"}, clear=False):
        from core.config import Settings

        settings = Settings()
        assert settings.api_base_url == "https://api.acedata.cloud"
        assert settings.default_model == "doubao-seedance-1-0-pro-250528"
        assert settings.default_resolution == "720p"
        assert settings.default_ratio == "16:9"
        assert settings.default_duration == 5
        assert settings.request_timeout == 1800.0
        assert settings.server_name == "seedance"
        assert settings.transport == "stdio"


def test_settings_from_environment() -> None:
    """Test that settings are loaded from environment variables."""
    env_vars = {
        "ACEDATACLOUD_API_TOKEN": "my-token",
        "ACEDATACLOUD_API_BASE_URL": "https://custom.api.com",
        "SEEDANCE_DEFAULT_MODEL": "doubao-seedance-1-5-pro-251215",
        "SEEDANCE_DEFAULT_RESOLUTION": "1080p",
        "SEEDANCE_DEFAULT_RATIO": "9:16",
        "SEEDANCE_DEFAULT_DURATION": "10",
        "SEEDANCE_REQUEST_TIMEOUT": "300",
        "MCP_SERVER_NAME": "my-seedance",
        "LOG_LEVEL": "DEBUG",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        from core.config import Settings

        settings = Settings()
        assert settings.api_token == "my-token"
        assert settings.api_base_url == "https://custom.api.com"
        assert settings.default_model == "doubao-seedance-1-5-pro-251215"
        assert settings.default_resolution == "1080p"
        assert settings.default_ratio == "9:16"
        assert settings.default_duration == 10
        assert settings.request_timeout == 300.0
        assert settings.server_name == "my-seedance"
        assert settings.log_level == "DEBUG"


def test_settings_is_configured() -> None:
    """Test the is_configured property."""
    from core.config import Settings

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": ""}, clear=False):
        settings = Settings()
        assert not settings.is_configured

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": "valid-token"}, clear=False):
        settings = Settings()
        assert settings.is_configured


def test_settings_validate_missing_token() -> None:
    """Test that validation fails without API token."""
    from core.config import Settings

    with patch.dict(os.environ, {"ACEDATACLOUD_API_TOKEN": ""}, clear=False):
        settings = Settings()
        with pytest.raises(ValueError, match="ACEDATACLOUD_API_TOKEN"):
            settings.validate()
