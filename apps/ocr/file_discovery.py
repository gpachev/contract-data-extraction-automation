import os
from typing import List

SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.png', '.jpeg'}

def discover_contract_files(root_dir: str) -> List[str]:
    """
    Recursively find all supported contract files in the given directory.
    Args:
        root_dir (str): The root directory to search.
    Returns:
        List[str]: List of absolute file paths to supported contract files.
    """
    contract_files: List[str] = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                contract_files.append(os.path.abspath(os.path.join(dirpath, filename)))
    return contract_files 