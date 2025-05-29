# automated_processing.py - Script for automated productivity data processing

import os
import json
import datetime
import logging
import shutil

# Attempt to import local classes. These need to be actual classes in the respective files.
try:
    from .calculate_productivity import CalculateProductivity
    from .clean_main_file import CleanMainFile
except ImportError:
    # This is a fallback if the classes are not yet defined or are not in the expected location.
    # For the script to fully function, these classes must be correctly implemented and importable.
    logging.warning("Could not import CalculateProductivity or CleanMainFile. Using placeholders. "
                    "Functionality will be limited.")

    # Placeholder classes if actual imports fail (for basic script structure to run)
    class CleanMainFile:
        def __init__(self, base_path, year, month, emails_to_delete_list, logger_instance, main_excel_file_name):
            self.base_path = base_path
            self.year = year
            self.month = month
            self.emails_to_delete = emails_to_delete_list
            self.logger = logger_instance
            self.main_excel_file_name = main_excel_file_name
            self.input_path = os.path.join(self.base_path, f"{self.year}-{self.month}")
            self.cleaned_file_path = os.path.join(self.input_path, "data_cleaned.xlsx")
            self.logger.info(f"CleanMainFile (Placeholder) initialized for path: {self.input_path}")

        def clear_data(self):
            self.logger.info(f"Simulating data cleaning for {self.main_excel_file_name} in path: {self.input_path}")
            # Create a dummy cleaned file if it doesn't exist
            if not os.path.exists(self.cleaned_file_path):
                try:
                    with open(self.cleaned_file_path, 'w') as f:
                        f.write("Dummy cleaned data from placeholder CleanMainFile")
                    self.logger.info(f"Placeholder CleanMainFile created dummy {self.cleaned_file_path}")
                except IOError as e:
                    self.logger.error(f"Placeholder CleanMainFile I/O error creating dummy file: {e}")
                    raise
            return self.cleaned_file_path

    class CalculateProductivity:
        def __init__(self, base_path, year, month, coefficients, logger_instance):
            self.base_path = base_path
            self.year = year
            self.month = month
            self.coefficients = coefficients
            self.logger = logger_instance
            self.input_path = os.path.join(self.base_path, f"{self.year}-{self.month}")
            self.logger.info(f"CalculateProductivity (Placeholder) initialized for path: {self.input_path}")
            # Check for INFORME_PERSONAL.xlsx as per design
            employee_info_path = os.path.join(self.input_path, "INFORME_PERSONAL.xlsx")
            if not os.path.exists(employee_info_path):
                self.logger.error(f"Placeholder CalculateProductivity: INFORME_PERSONAL.xlsx missing at {employee_info_path}")
                raise FileNotFoundError(f"INFORME_PERSONAL.xlsx missing at {employee_info_path}")


        def calculate_productivity(self):
            self.logger.info(f"Simulating daily productivity calculation (Placeholder) for path: {self.input_path}")
            try:
                with open(os.path.join(self.input_path, "productivity_by_day.xlsx"), 'w') as f:
                    f.write("Dummy daily productivity data from placeholder")
            except IOError as e:
                self.logger.error(f"Placeholder CalculateProductivity I/O error creating dummy daily file: {e}")
                raise

        def final_table(self):
            self.logger.info(f"Simulating final table generation (Placeholder) for path: {self.input_path}")
            try:
                with open(os.path.join(self.input_path, "final_table_with_results.xlsx"), 'w') as f:
                    f.write("Dummy final table data from placeholder")
            except IOError as e:
                self.logger.error(f"Placeholder CalculateProductivity I/O error creating dummy final table: {e}")
                raise

# Global logger instance
logger = None

def load_configuration(config_file_path="automation_config.json"):
    """Loads configuration from a JSON file."""
    try:
        # Adjust path to be relative to this script's location if config is in the same dir
        script_dir = os.path.dirname(__file__)
        abs_config_path = os.path.join(script_dir, config_file_path)
        
        with open(abs_config_path, 'r') as f:
            config = json.load(f)
        
        # Basic validation
        required_top_level_keys = ["input_base_path", "log_file_path", "processed_files_log_path", "required_files", "EMAILS_TO_DELETE", "COEFFICIENTS"]
        if not all(k in config for k in required_top_level_keys):
            raise ValueError(f"Essential top-level configuration keys are missing from {abs_config_path}. Required: {required_top_level_keys}")
        if not isinstance(config["required_files"], dict) or not "main_excel_file_raw_name" in config["required_files"]:
            raise ValueError("Configuration error: 'required_files' must be a dictionary and contain 'main_excel_file_raw_name'.")
        return config
    except FileNotFoundError:
        if logger:
            logger.error(f"CRITICAL: Configuration file {abs_config_path} not found.")
        else:
            print(f"CRITICAL: Configuration file {abs_config_path} not found.")
        raise
    except json.JSONDecodeError:
        if logger:
            logger.error(f"CRITICAL: Configuration file {abs_config_path} is not valid JSON.")
        else:
            print(f"CRITICAL: Configuration file {abs_config_path} is not valid JSON.")
        raise
    except ValueError as ve:
        if logger:
            logger.error(f"CRITICAL: Configuration error: {ve}")
        else:
            print(f"CRITICAL: Configuration error: {ve}")
        raise

def setup_logging(log_file_path_from_config, log_level_str): # Add default for log_level_str
    """Initializes file and console logging."""
    global logger
    logger = logging.getLogger("AutomatedProcessing")
    
    try:
        numeric_level = getattr(logging, log_level_str.upper())
    except AttributeError:
        numeric_level = logging.INFO
        if logger.hasHandlers(): # Check if handlers are already set (e.g. by placeholder warning)
            for handler in logger.handlers[:]: logger.removeHandler(handler) # Clear existing handlers
        logger.addHandler(logging.StreamHandler()) # Temp handler for this message
        logger.warning(f"Invalid log level '{log_level_str}'. Defaulting to INFO.")
        if logger.handlers: logger.removeHandler(logger.handlers[0]) # Remove temp handler


    logger.setLevel(numeric_level)
    logger.handlers = [] # Clear any pre-existing handlers from placeholder warnings etc.

    # Create directory for log file if it doesn't exist
    log_dir = os.path.dirname(log_file_path_from_config)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as e:
            # Cannot create log directory, fall back to console only
            console_handler_fallback = logging.StreamHandler()
            console_formatter_fallback = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler_fallback.setFormatter(console_formatter_fallback)
            logger.addHandler(console_handler_fallback)
            logger.error(f"Could not create log directory {log_dir}: {e}. Logging to console only.")
            return logger

    # File handler
    try:
        file_handler = logging.FileHandler(log_file_path_from_config, mode='a')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except IOError as e:
        logger.error(f"Failed to set up file logger at {log_file_path_from_config}: {e}. Will log to console only.")


    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def has_been_processed(folder_identifier, processed_log_file):
    """Checks the log to see if a folder/identifier was successfully processed."""
    try:
        if not os.path.exists(processed_log_file):
            return False
        with open(processed_log_file, "r") as f:
            for line in f:
                if folder_identifier in line and "SUCCESS" in line:
                    return True
        return False
    except Exception as e:
        if logger:
            logger.error(f"Error checking processed log {processed_log_file}: {e}")
        else:
            print(f"Error checking processed log {processed_log_file}: {e}")
        return False # Safer to assume not processed if log is unreadable

def update_processed_log(folder_identifier, status, log_file): # Ensure log_file path is absolute or correctly relative
    """Appends a record to the processed files log."""
    try:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        timestamp = datetime.datetime.now().isoformat()
        with open(log_file, "a") as f:
            f.write(f"{timestamp} | {folder_identifier} | {status}\n")
    except Exception as e:
        if logger:
            logger.error(f"Failed to update processed log {log_file}: {e}")
        else:
            print(f"CRITICAL: Failed to update processed log {log_file}: {e}")

def are_all_input_files_present(path_to_check, required_files_dict):
    """Checks if all specified initial input files (from the values of the dict) exist in the given path."""
    if not isinstance(required_files_dict, dict):
        if logger:
            logger.error("Configuration error: required_files is not a dictionary.")
        return False

    all_required_filenames = list(required_files_dict.values())
    if logger:
        logger.debug(f"Checking for required files in {path_to_check}: {all_required_filenames}")
    
    missing_files = []
    for file_name in all_required_filenames:
        if not file_name: # Handle potential null/empty filenames in config
            logger.warning("Skipping check for an empty filename in required_files config.")
            continue
        if not os.path.exists(os.path.join(path_to_check, file_name)):
            missing_files.append(file_name)
    
    if missing_files:
        if logger:
            logger.error(f"Missing required initial input files in {path_to_check}: {', '.join(missing_files)}. HU-AUTO-001")
        return False
    
    if logger:
        logger.info(f"All {len(all_required_filenames)} required initial input files are present in {path_to_check}.")
    return True

def get_credentials(config):
    """Placeholder for credential handling."""
    credential_path = config.get("credential_file_path") # This key should be in automation_config.json
    if credential_path and os.path.exists(credential_path):
        # Simulate loading credentials if file exists
        if logger:
            logger.info(f"Simulating credential load from {credential_path}.")
        return {"token": "dummy_token_from_file"} # Placeholder
    else:
        if logger:
            logger.warning(f"Credential file path not configured or not found: {credential_path}. Using placeholder credentials.")
        return {"token": "placeholder_token_no_real_access"}

def scan_and_process_folder(current_period_path, year_str, month_str, config):
    """Scans a given folder, validates its contents, and processes if conditions are met."""
    folder_identifier = f"{year_str}-{month_str}" # Used for logging processed status
    processed_log_file = config["processed_files_log_path"]

    logger.info(f"Scanning folder: {current_period_path} for period {folder_identifier}")

    if has_been_processed(folder_identifier, processed_log_file):
        logger.info(f"Period {folder_identifier} (path: {current_period_path}) has already been marked as successfully processed. Skipping.")
        return

    # Get the dictionary of required files
    required_files_dict = config.get("required_files")
    if not isinstance(required_files_dict, dict) or not required_files_dict.get("main_excel_file_raw_name"):
        logger.error("Configuration error: 'required_files' dictionary is missing or 'main_excel_file_raw_name' is not defined within it. Cannot validate inputs.")
        update_processed_log(folder_identifier, "FAILED_CONFIG_ERROR_REQUIRED_FILES", processed_log_file)
        return
    
    # The are_all_input_files_present function now expects the dictionary of all required files.
    if not are_all_input_files_present(current_period_path, required_files_dict):
        logger.error(f"Halting processing for {folder_identifier} due to missing initial input files. HU-AUTO-001")
        update_processed_log(folder_identifier, "FAILED_MISSING_FILES", processed_log_file)
        return

    credentials = get_credentials(config)
    if not credentials: # Assuming get_credentials logs its own errors/warnings
        logger.error(f"Halting processing for {folder_identifier} due to credential issues.")
        update_processed_log(folder_identifier, "FAILED_CREDENTIALS", processed_log_file)
        return
    
    # Base path for CleanMainFile and CalculateProductivity should be the one containing year-month folders
    # current_period_path is effectively input_base_path/year-month/
    # So, input_base_path is os.path.dirname(current_period_path) if current_period_path is specific.
    # However, the design implies classes take the specific period path. Let's adjust.
    # The classes should expect the direct path to the YYYY-MM folder.
    
    try:
        logger.info(f"Starting data cleaning for {folder_identifier} in {current_period_path}")
        cleaner = CleanMainFile(
            base_path=os.path.dirname(current_period_path), # This should be input_base_path
            year=year_str,
            month=month_str,
            emails_to_delete_list=config.get("EMAILS_TO_DELETE", []),
            logger_instance=logger,
            main_excel_file_name=config['required_files']['main_excel_file_raw_name']
        )
        cleaned_file_actual_path = cleaner.clear_data()
        
        if not cleaned_file_actual_path or not os.path.exists(cleaned_file_actual_path):
            logger.error(f"Data cleaning failed or did not produce the cleaned file at the expected location: {cleaned_file_actual_path}. Halting for {folder_identifier}.")
            update_processed_log(folder_identifier, "FAILED_CLEANING_OUTPUT_MISSING", processed_log_file)
            return
        logger.info(f"Data cleaning successful for {folder_identifier}. Cleaned file: {cleaned_file_actual_path}")

        logger.info(f"Starting productivity calculation for {folder_identifier} in {current_period_path}")
        calculator = CalculateProductivity(
            base_path=os.path.dirname(current_period_path), # This should be input_base_path
            year=year_str,
            month=month_str,
            coefficients=config.get("COEFFICIENTS", {}),
            logger_instance=logger
        )
        calculator.calculate_productivity()
        calculator.final_table()
        logger.info(f"Productivity calculation successful for {folder_identifier}.")

        # Optional: Manage output files (e.g., copy to output_base_path)
        if config.get("output_base_path"):
            manage_output_files(current_period_path, config["output_base_path"], folder_identifier, logger)

        update_processed_log(folder_identifier, "SUCCESS", processed_log_file)
        logger.info(f"Successfully processed period {folder_identifier} at path {current_period_path}.")

    except FileNotFoundError as fnf_error: # Specifically for INFORME_PERSONAL.xlsx or other critical files for classes
        logger.error(f"Critical file not found during processing of {folder_identifier}: {fnf_error}", exc_info=True)
        update_processed_log(folder_identifier, f"FAILED_FILE_NOT_FOUND_ERROR: {fnf_error}", processed_log_file)
    except Exception as e:
        logger.error(f"An unexpected error occurred during processing of {folder_identifier}: {e}", exc_info=True)
        update_processed_log(folder_identifier, f"FAILED_UNEXPECTED_ERROR: {e}", processed_log_file)

def manage_output_files(source_folder_period, output_base_path_config, year_month_str_identifier, logger_instance):
    """Copies key output files to a centralized output location."""
    destination_folder = os.path.join(output_base_path_config, year_month_str_identifier)
    try:
        os.makedirs(destination_folder, exist_ok=True)
    except OSError as e:
        logger_instance.error(f"Could not create output directory {destination_folder}: {e}. Skipping file copy.")
        return

    files_to_copy = ["data_cleaned.xlsx", "productivity_by_day.xlsx", "final_table_with_results.xlsx"]
    
    for file_name in files_to_copy:
        source_file = os.path.join(source_folder_period, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        try:
            if os.path.exists(source_file):
                shutil.copy2(source_file, destination_file)
                logger_instance.info(f"Copied {source_file} to {destination_file}")
            else:
                logger_instance.warning(f"Output file {source_file} not found for copying.")
        except Exception as e:
            logger_instance.error(f"Failed to copy {source_file} to {destination_file}: {e}")

def main_auto_processing():
    global logger 
    # Initial minimal logger for config loading issues
    pre_config_logger = logging.getLogger("PreConfigAutomatedProcessing")
    pre_config_logger.addHandler(logging.StreamHandler())
    pre_config_logger.setLevel(logging.INFO)

    try:
        config = load_configuration() # Uses default "automation_config.json"
    except Exception as e:
        pre_config_logger.critical(f"Failed to load configuration. Script cannot proceed: {e}")
        # Log to a default processed_log if possible, to indicate major failure
        # This path needs to be known or hardcoded if config doesn't load
        # Ensure __file__ is available (it is in normal script execution)
        script_dir_for_fallback = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
        fallback_processed_log = os.path.join(script_dir_for_fallback, "logs", "processed_folders.txt")
        update_processed_log("SYSTEM_CONFIG_LOAD_FAILURE", f"FAILED_CONFIG_LOAD: {e}", fallback_processed_log)
        return

    logger = setup_logging(config["log_file_path"], config.get("logging_level", "INFO"))
    if not logger: # setup_logging could fail if log dir is unwritable
        pre_config_logger.critical("Logger setup failed. Script cannot proceed.")
        # Attempt to log this major failure
        script_dir_for_fallback = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
        fallback_processed_log = os.path.join(script_dir_for_fallback, "logs", "processed_folders.txt")
        update_processed_log("SYSTEM_LOGGING_FAILURE", "FAILED_LOGGER_SETUP", fallback_processed_log)
        return

    logger.info("Automated processing script started.")
    logger.debug(f"Configuration loaded: {json.dumps(config, indent=4)}")

    if config.get("run_for_current_date", True):
        now = datetime.datetime.now()
        current_year_str = str(now.year)
        current_month_str = str(now.month).zfill(2)
    else:
        current_year_str = str(config.get("specific_year", ""))
        current_month_str = str(config.get("specific_month", "")).zfill(2)
        if not current_year_str or not config.get("specific_month"): # Check original month value before zfill
            logger.error("Configuration error: specific_year or specific_month not provided or invalid when run_for_current_date is false.")
            update_processed_log("SYSTEM_DATE_CONFIG_ERROR", "FAILED_INVALID_DATE_CONFIG", config["processed_files_log_path"])
            return
            
    logger.info(f"Targeting processing for period: {current_year_str}-{current_month_str}")

    current_processing_folder_name = f"{current_year_str}-{current_month_str}"
    current_period_input_path = os.path.join(config["input_base_path"], current_processing_folder_name)

    if not os.path.isdir(current_period_input_path):
        logger.warning(f"Input folder {current_period_input_path} does not exist. Nothing to process for {current_year_str}-{current_month_str}.")
        update_processed_log(f"{current_year_str}-{current_month_str}", "FAILED_INPUT_FOLDER_NOT_FOUND", config["processed_files_log_path"])
    else:
        scan_and_process_folder(current_period_input_path, current_year_str, current_month_str, config)

    logger.info("Automated processing script finished.")

if __name__ == "__main__":
    main_auto_processing()
```
