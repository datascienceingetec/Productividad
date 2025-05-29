import pandas as pd

class ReportGenerator:
    def __init__(self, logger=None) -> None:
        self.logger = logger

    def save_report(self, df: pd.DataFrame, output_filename: str) -> pd.DataFrame:
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        if self.logger:
            self.logger.info(f"Final table saved to {output_filename}")
        return df
    
    def save_to_drive(self, drive_connector, output_filename: str) -> None:
        # drive_connector.upload_file(output_filename)
        pass