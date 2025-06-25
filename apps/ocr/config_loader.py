from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass(frozen=True)
class Config:
    contracts_input_path: str
    gemini_api_key: str


def get_config() -> Config:
    """
    Loads CONTRACTS_INPUT_PATH and GEMINI_API_KEY from .env file.
    Raises ValueError if any required variable is missing.
    Returns:
        Config: Dataclass with loaded configuration.
    """
    load_dotenv()
    contracts_input_path = os.getenv("CONTRACTS_INPUT_PATH")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not contracts_input_path:
        raise ValueError("CONTRACTS_INPUT_PATH is not set in .env")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")
    return Config(
        contracts_input_path=contracts_input_path,
        gemini_api_key=gemini_api_key,
    ) 