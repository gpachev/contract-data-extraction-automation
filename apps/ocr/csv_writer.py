import pandas as pd
from typing import List, Dict, Any
from datetime import datetime

CSV_COLUMNS = [
    "Own Company Name",
    "Subcontractor Name",
    "Subcontractor Location",
    "Date of Contract",
    "End Date of Contract",
    "Is Non-compete Clause",
    "Non-compete Text",
    "Penalty Amount",
    "URL of Original Contract"
]

LLM_TO_CSV_MAP = {
    "OwnCompanyName": "Own Company Name",
    "SubcontractorName": "Subcontractor Name",
    "SubcontractorLocation": "Subcontractor Location",
    "DateOfContract": "Date of Contract",
    "EndDateOfContract": "End Date of Contract",
    "IsNonCompeteClause": "Is Non-compete Clause",
    "NonCompeteText": "Non-compete Text",
    "PenaltyAmount": "Penalty Amount",
    "URL of Original Contract": "URL of Original Contract"
}

CSV_FILENAME_TEMPLATE = "{timestamp}-contract_intelligence.csv"

def map_llm_to_csv(contract: Dict[str, Any]) -> Dict[str, Any]:
    mapped = {csv_col: "" for csv_col in CSV_COLUMNS}
    for llm_key, value in contract.items():
        csv_col = LLM_TO_CSV_MAP.get(llm_key)
        if csv_col:
            mapped[csv_col] = value
    return mapped

def write_contracts_to_csv(contracts: List[Dict[str, Any]], output_dir: str = ".") -> str:
    """
    Write contract data to a CSV file with the required columns and naming convention.
    Args:
        contracts (List[Dict[str, Any]]): List of contract data dicts.
        output_dir (str): Directory to write the CSV file to.
    Returns:
        str: Path to the written CSV file.
    """
    mapped_contracts = [map_llm_to_csv(c) for c in contracts]
    df = pd.DataFrame(mapped_contracts, columns=CSV_COLUMNS)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = CSV_FILENAME_TEMPLATE.format(timestamp=timestamp)
    output_path = f"{output_dir}/{filename}"
    df.to_csv(output_path, index=False)
    return output_path 