import os
from datetime import datetime
from typing import Optional

LOG_FILENAME_TEMPLATE = "{timestamp}-company-intelligence.log"

class ContractLogger:
    def __init__(self, log_dir: str = "."):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        self.log_path = os.path.join(log_dir, LOG_FILENAME_TEMPLATE.format(timestamp=timestamp))
        self._log_file = open(self.log_path, "a", encoding="utf-8")

    def log_status(self, status: str, file_path: str, reason: Optional[str] = None) -> None:
        if status == "Success":
            line = f"Success - {file_path}"
        elif status == "Failed" and reason:
            line = f"Failed - {reason} - {file_path}"
        else:
            line = f"Failed - Unknown Error - {file_path}"
        self._log_file.write(line + "\n")
        self._log_file.flush()

    def log_skipped(self, file_path: str, reason: Optional[str] = None) -> None:
        if reason:
            line = f"Skipped - {reason} - {file_path}"
        else:
            line = f"Skipped - {file_path}"
        self._log_file.write(line + "\n")
        self._log_file.flush()

    def close(self):
        self._log_file.close()

    def get_log_path(self) -> str:
        return self.log_path 