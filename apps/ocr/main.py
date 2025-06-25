import os
from config_loader import get_config
from file_discovery import discover_contract_files
from docx_extractor import extract_docx_text
from gemini_client import extract_contract_data
from csv_writer import write_contracts_to_csv
from logger import ContractLogger
from typing import List, Dict, Any

SUPPORTED_DOCX = ".docx"
SUPPORTED_OTHER = {".pdf", ".png", ".jpeg"}

def main():
    config = get_config()
    print(f"Loaded config. Searching for contracts in: {config.contracts_input_path}")
    files = discover_contract_files(config.contracts_input_path)
    print(f"Found {len(files)} contract files.")
    results: List[Dict[str, Any]] = []
    logger = ContractLogger()
    try:
        for idx, file_path in enumerate(files, 1):
            ext = os.path.splitext(file_path)[1].lower()
            print(f"[{idx}/{len(files)}] Processing: {file_path}")
            try:
                if ext == SUPPORTED_DOCX:
                    text = extract_docx_text(file_path)
                    if not text:
                        print(f"  [ERROR] Could not extract text from DOCX: {file_path}")
                        logger.log_status("Failed", file_path, reason="DOCX Conversion Error")
                        continue
                    data = extract_contract_data(
                        gemini_api_key=config.gemini_api_key,
                        contract_text=text
                    )
                elif ext in SUPPORTED_OTHER:
                    data = extract_contract_data(
                        gemini_api_key=config.gemini_api_key,
                        contract_file_path=file_path
                    )
                else:
                    print(f"  [SKIP] Unsupported file type: {file_path}")
                    logger.log_skipped(file_path, reason="Unsupported Format")
                    continue
                if data is None:
                    print(f"  [ERROR] Gemini extraction failed: {file_path}")
                    logger.log_status("Failed", file_path, reason="Gemini API Error")
                    continue
                data["URL of Original Contract"] = file_path
                results.append(data)
                print(f"  [OK] Extraction successful.")
                logger.log_status("Success", file_path)
            except Exception as e:
                print(f"  [ERROR] Exception: {e}")
                logger.log_status("Failed", file_path, reason="Unknown Error")
        print(f"\nExtraction complete. {len(results)} contracts processed successfully.")
        csv_path = write_contracts_to_csv(results)
        print(f"CSV file written to: {csv_path}")
        print(f"Log file written to: {logger.get_log_path()}")
    finally:
        logger.close()

if __name__ == "__main__":
    main() 