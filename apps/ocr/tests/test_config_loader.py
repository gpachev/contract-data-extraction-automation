import os
import pytest
from unittest.mock import patch
from apps.ocr.config_loader import get_config, Config
from dotenv import set_key


def test_get_config_success(tmp_path, monkeypatch):
    with patch("apps.ocr.config_loader.load_dotenv", lambda: None):
        env_file = tmp_path / ".env"
        env_content = "CONTRACTS_INPUT_PATH=/contracts\nGEMINI_API_KEY=abc123\n"
        env_file.write_text(env_content)
        monkeypatch.setenv("CONTRACTS_INPUT_PATH", "/contracts")
        monkeypatch.setenv("GEMINI_API_KEY", "abc123")
        config = get_config()
        assert isinstance(config, Config)
        assert config.contracts_input_path == "/contracts"
        assert config.gemini_api_key == "abc123"


def test_get_config_missing_contracts_input_path(monkeypatch):
    with patch("apps.ocr.config_loader.load_dotenv", lambda: None):
        monkeypatch.delenv("CONTRACTS_INPUT_PATH", raising=False)
        monkeypatch.setenv("GEMINI_API_KEY", "abc123")
        with pytest.raises(ValueError, match="CONTRACTS_INPUT_PATH is not set"):
            get_config()


def test_get_config_missing_gemini_api_key(monkeypatch):
    with patch("apps.ocr.config_loader.load_dotenv", lambda: None):
        monkeypatch.setenv("CONTRACTS_INPUT_PATH", "/contracts")
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
            get_config() 