import shutil
from pathlib import Path
from typing import List
import logging

class DriveConnector:
    """Placeholder connector that copies files from a local 'drive' folder."""

    def __init__(self, logger: logging.Logger, source_folder: Path):
        self.logger = logger
        self.source_folder = Path(source_folder)

    def download_files(self, required_files: List[str], destination: Path) -> None:
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        for file_name in required_files:
            src = self.source_folder / file_name
            dest = destination / file_name
            if src.exists():
                shutil.copy(src, dest)
                self.logger.info(f"Downloaded {file_name} to {dest}")
            else:
                self.logger.error(f"Missing file in source drive: {file_name}")
