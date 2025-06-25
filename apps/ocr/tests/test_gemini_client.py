import pytest
from unittest.mock import patch, MagicMock
from apps.ocr.gemini_client import extract_contract_data

def mock_gemini_response(json_data):
    mock_part = MagicMock()
    mock_part.text = json_data  # Should be a JSON string
    mock_content = MagicMock()
    mock_content.parts = [mock_part]
    mock_candidate = MagicMock()
    mock_candidate.content = mock_content
    mock_response = MagicMock()
    mock_response.candidates = [mock_candidate]
    return mock_response

@patch("apps.ocr.gemini_client.genai")
def test_extract_contract_data_text(mock_genai):
    # Mock the Gemini API response
    expected = {"OwnCompanyName": "A", "IsNonCompeteClause": False}
    mock_response = mock_gemini_response('{"OwnCompanyName": "A", "IsNonCompeteClause": false}')
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client
    result = extract_contract_data(
        gemini_api_key="fake-key",
        contract_text="Sample contract text"
    )
    assert result == expected
    mock_client.models.generate_content.assert_called()

@patch("apps.ocr.gemini_client.genai")
def test_extract_contract_data_file(mock_genai, tmp_path):
    # Create a fake file
    file_path = tmp_path / "sample.pdf"
    file_path.write_bytes(b"PDF content")
    expected = {"OwnCompanyName": "B", "IsNonCompeteClause": True}
    mock_response = mock_gemini_response('{"OwnCompanyName": "B", "IsNonCompeteClause": true}')
    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response
    mock_genai.Client.return_value = mock_client
    result = extract_contract_data(
        gemini_api_key="fake-key",
        contract_file_path=str(file_path)
    )
    assert result == expected
    mock_client.models.generate_content.assert_called()

@patch("apps.ocr.gemini_client.genai")
def test_extract_contract_data_error(mock_genai):
    mock_genai.Client.side_effect = Exception("API error")
    result = extract_contract_data(
        gemini_api_key="fake-key",
        contract_text="Sample contract text"
    )
    assert result is None 