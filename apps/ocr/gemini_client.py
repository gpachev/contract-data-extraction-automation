from typing import Optional, Dict, Any, Annotated
from pydantic import BaseModel, StringConstraints
import google.genai as genai
import os
import json

# The prompt and schema should match the PRD
GEMINI_PROMPT = (
    "You are an expert contract analyst. Your task is to meticulously extract specific data points from the provided legal contract. "
    "Your response MUST be a JSON object that strictly adheres to the provided schema.\n\n"
    "**Extract the following information:**\n"
    "1. Own Company Name\n2. Subcontractor Name\n3. Subcontractor Location\n4. Date of Contract (YYYY-MM-DD)\n5. End Date of Contract (YYYY-MM-DD, omit if missing)\n6. Is Non-compete Clause (true/false)\n7. Non-compete Text (if present)\n8. Penalty Amount (if present)\n\n"
    "If a field (other than IsNonCompeteClause) is not found, do not include that key in the final JSON output.\n"
    "Your output must be only the JSON object.\n\n"
    "**Contract Content for Analysis:**\n"
    "[INSERT CONTRACT CONTENT HERE]"
)

GEMINI_SCHEMA = {
    "type": "object",
    "properties": {
        "OwnCompanyName": {"type": "string"},
        "SubcontractorName": {"type": "string"},
        "SubcontractorLocation": {"type": "string"},
        "DateOfContract": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"},
        "EndDateOfContract": {"type": "string", "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"},
        "IsNonCompeteClause": {"type": "boolean"},
        "NonCompeteText": {"type": "string"},
        "PenaltyAmount": {"type": "string", "pattern": r"^[A-Z]{3} (\\d{1,3}( \\d{3})*|\\d+)$"}
    },
    "required": [
        "OwnCompanyName", "SubcontractorName", "SubcontractorLocation", "DateOfContract", "IsNonCompeteClause"
    ],
    "additionalProperties": False
}

class GeminiContractSchema(BaseModel):
    OwnCompanyName: str
    SubcontractorName: str
    SubcontractorLocation: str
    DateOfContract: Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    EndDateOfContract: Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")] = None
    IsNonCompeteClause: bool
    NonCompeteText: Optional[str] = None
    PenaltyAmount: Annotated[str, StringConstraints(pattern=r"^[A-Z]{3} (\d{1,3}( \d{3})*|\d+)$")] = None


def extract_contract_data(
    gemini_api_key: str,
    *,
    contract_text: Optional[str] = None,
    contract_file_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Sends contract text or file to Google Gemini and returns the extracted data as a dict.
    Args:
        gemini_api_key (str): Gemini API key.
        contract_text (Optional[str]): Text content for DOCX contracts.
        contract_file_path (Optional[str]): File path for PDF/PNG/JPEG contracts.
    Returns:
        Optional[Dict[str, Any]]: Extracted contract data, or None if extraction fails.
    """

    try:
        if contract_text:
            prompt = GEMINI_PROMPT.replace("[INSERT CONTRACT CONTENT HERE]", contract_text)
        elif contract_file_path:
            with open(contract_file_path, "rb") as f:
                file_data = f.read()
            prompt = GEMINI_PROMPT.replace("[INSERT CONTRACT CONTENT HERE]", "(see attached file)")
        else:
            raise ValueError("Either contract_text or contract_file_path must be provided.")
        # Parse JSON from Gemini response
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config={
                "response_mime_type": "application/json",
                # "response_schema": GeminiContractSchema
            },
            contents=prompt
        )
        return json.loads(response.candidates[0].content.parts[0].text)
    except Exception as e:
        # Optionally log the error here
        return None

def _guess_mime_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return "application/pdf"
    if ext == ".png":
        return "image/png"
    if ext == ".jpeg" or ext == ".jpg":
        return "image/jpeg"
    return "application/octet-stream" 