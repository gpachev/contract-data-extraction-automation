import os
import pandas as pd
from apps.ocr.csv_writer import write_contracts_to_csv, CSV_COLUMNS

def test_write_contracts_to_csv(tmp_path):
    contracts = [
        {
            "OwnCompanyName": "A",
            "SubcontractorName": "B",
            "SubcontractorLocation": "C",
            "DateOfContract": "2024-07-01",
            "IsNonCompeteClause": True,
            "URL of Original Contract": "/path/to/file.pdf"
        },
        {
            "OwnCompanyName": "X",
            "SubcontractorName": "Y",
            "SubcontractorLocation": "Z",
            "DateOfContract": "2024-07-02",
            "EndDateOfContract": "2024-12-31",
            "IsNonCompeteClause": False,
            "NonCompeteText": "None",
            "PenaltyAmount": "USD 10 000",
            "URL of Original Contract": "/path/to/file2.pdf"
        }
    ]
    output_path = write_contracts_to_csv(contracts, output_dir=str(tmp_path))
    print(f"Output path: {output_path}")
    assert os.path.exists(output_path)
    df = pd.read_csv(output_path)
    # Check columns and order
    assert list(df.columns) == CSV_COLUMNS
    # Check values and blanks
    assert df.iloc[0]["Own Company Name"] == "A"
    assert pd.isna(df.iloc[0]["End Date of Contract"])
    assert df.iloc[1]["Penalty Amount"] == "USD 10 000" 