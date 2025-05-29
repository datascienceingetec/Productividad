from pathlib import Path
from typing import List
import logging

class FileValidator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def check_presence(self, folder: Path, required_files: List[str]) -> bool:
        folder = Path(folder)
        all_present = True
        for name in required_files:
            file_path = folder / name
            if not file_path.exists():
                self.logger.error(f"Required file missing: {name}")
                all_present = False
            else:
                self.logger.info(f"Validated presence of {name}")
        return all_present
