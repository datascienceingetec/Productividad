from pathlib import Path
import logging
import pandas as pd

class FileValidator:
    def __init__(self, files: list, logger: logging.Logger):
        self.files = files
        self.logger = logger

    def check_presence(self, folder: Path) -> dict:
        folder = Path(folder)
        presence = {}

        for file_info in self.files:
            file_name = file_info["name"]
            file_path = folder / file_name
            file_exists = file_path.exists()
            presence[file_name] = file_exists

            if not file_exists:
                self.logger.error(f"Required file missing: {file_name}")
            else:
                self.logger.info(f"Found file: {file_name}")

        return presence

    def check_format(self, folder: Path) -> dict:
        folder = Path(folder)
        format_checks = {}

        for file_info in self.files:
            file_name = file_info["name"]
            expected_format = file_info["format"]
            file_path = folder / file_name

            if not file_path.exists():
                format_checks[file_name] = False
                continue

            actual_format = file_path.suffix[1:].lower()
            is_correct_format = (actual_format == expected_format.lower())
            format_checks[file_name] = is_correct_format

            if not is_correct_format:
                self.logger.error(f"Incorrect format for {file_name}: expected .{expected_format}, got .{actual_format}")
            else:
                self.logger.info(f"Validated format for {file_name}")

        return format_checks

    def check_columns(self, folder: Path) -> dict:
        folder = Path(folder)
        column_checks = {}

        for file_info in self.files:
            file_name = file_info["name"]
            file_path = folder / file_name
            required_columns = set(column.lower() for column in file_info["columns"])

            if not file_path.exists():
                column_checks[file_name] = False
                continue

            try:
                if file_info["format"] == 'csv':
                    df = pd.read_csv(file_path, nrows=1)
                else:
                    df = pd.read_excel(file_path, nrows=1)

                actual_columns = set(column.lower() for column in df.columns)
                missing_columns = required_columns - actual_columns

                if missing_columns:
                    self.logger.error(f"Missing columns in {file_name}: {', '.join(missing_columns)}")
                    column_checks[file_name] = False
                else:
                    self.logger.info(f"Validated columns in {file_name}")
                    column_checks[file_name] = True

            except Exception as e:
                self.logger.error(f"Error reading {file_name}: {str(e)}")
                column_checks[file_name] = False

        return column_checks

    def validate_files(self, folder: Path, validate_columns: bool = True) -> dict:
        validation_results = {
            'presence': self.check_presence(folder),
            'columns': self.check_columns(folder)
        }

        if validate_columns:
            validation_results['format'] = self.check_format(folder)

        all_passed = all(
            all(results.values()) for results in validation_results.values()
        )
        validation_results['all_valid'] = all_passed

        if all_passed:
            self.logger.info("All files validated successfully")
        else:
            self.logger.error("Validation failed for one or more files")

        return all_passed