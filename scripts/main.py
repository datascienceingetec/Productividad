import json
import os
import tempfile
from pathlib import Path

from scripts.clean_main_file import CleanMainFile
from scripts.calculate_productivity import CalculateProductivity
from scripts.logger_util import setup_logger
from scripts.drive_connector import DriveConnector
from scripts.file_validator import FileValidator

REQUIRED_FILES = [
    "Productividad_Google.xlsx",
    "Autodesk.xlsx",
    "Meetings.xlsx",
    "chats_source.csv",
    "VPN.csv",
    "INFORME_PERSONAL.xlsx",
]


def load_parameters() -> dict:
    params_path = Path(__file__).parent / "initial_parameters.json"
    with open(params_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    params = load_parameters()

    emails_to_delete = params["EMAILS_TO_DELETE"]
    year = params["YEAR"]
    month = params["MONTH"]
    coefficients = params["COEFFICIENTS"]

    source_drive = Path(os.getenv("SOURCE_DRIVE", "./drive"))

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_path = Path(tmpdirname)
        logger = setup_logger(str(tmp_path / "log.txt"))

        logger.info("Starting productivity script")

        connector = DriveConnector(logger, source_drive)
        connector.download_files(REQUIRED_FILES, tmp_path)

        validator = FileValidator(logger)
        if not validator.check_presence(tmp_path, REQUIRED_FILES):
            logger.error("Validation failed. Exiting.")
            return

        # Use tmp_path with trailing separator for existing classes
        work_path = str(tmp_path) + os.sep

        cleaner = CleanMainFile(work_path, year, month, emails_to_delete, logger)
        cleaner.clear_data()

        productivity = CalculateProductivity(work_path, year, month, coefficients, logger)
        productivity.calculate_productivity()
        productivity.final_table()

        logger.info("Processing completed")


if __name__ == "__main__":
    main()
