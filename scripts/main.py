import json
import os
import tempfile
from pathlib import Path
from productivity_data_cleaner import GoogleProductivityDataCleaner
from data_processor import DataProcessor
from report_generator import ReportGenerator
from logger_util import setup_logger, close_logger
from drive_connector import DriveConnector
from file_validator import FileValidator

def load_parameters() -> dict:
    params_path = Path(__file__).parent / "initial_parameters.json"
    with open(params_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main() -> None:
    params = load_parameters()

    emails_to_delete = params["EMAILS_TO_DELETE"]
    year = params["YEAR"]
    month = params["MONTH"]
    year_month = f"{year}-{str(month).zfill(2)}"
    coefficients = params["COEFFICIENTS"]
    required_files = params["REQUIRED_FILES"]
    file_names = [required_files[key]["name"] for key in required_files]

    source_drive = Path(os.getenv("SOURCE_DRIVE", "scripts/sample_data"))
    logger = setup_logger('.log')

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmp_path = Path(tmpdirname)
        logger.info("Starting productivity script")

        connector = DriveConnector(logger, source_drive)
        connector.download_files(file_names, tmp_path)

        validator = FileValidator(list(required_files.values()), logger)
        if not validator.validate_files(tmp_path, validate_columns=False):
            logger.error("Validation failed. Exiting.")
            close_logger(logger)
            return False
        
        # Use tmp_path with trailing separator for existing classes
        work_path = str(tmp_path) + os.sep
        productivity_filename = required_files.get("productivity")['name']
        cleaner = GoogleProductivityDataCleaner(work_path, productivity_filename, year, month, emails_to_delete, logger)
        cleaned_data = cleaner.clean_data()
        logger.info(f"Cleaned google productivity data saved to {cleaned_data}")

        data_processor = DataProcessor(work_path, required_files, year, month, coefficients, logger)
        data_processor.calculate_productivity()
        results = data_processor.get_results()

        report_generator = ReportGenerator(logger)
        report_generator.save_report(results,'reporte_productividad_'+year_month+'.xlsx')

        logger.info("Processing completed")
        close_logger(logger)

if __name__ == "__main__":
    main()
