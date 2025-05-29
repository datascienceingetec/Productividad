"""Utilities to download required files from a Google Drive folder."""

import io
import shutil
from pathlib import Path
from typing import Dict, List
import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class DriveConnector:
    """Connects to a Google Drive folder and downloads required files."""

    def __init__(self, logger: logging.Logger, credentials_file: Path, folder_id: str) -> None:
        self.logger = logger
        self.credentials_file = Path(credentials_file)
        self.folder_id = folder_id
        self.service = None

    def authenticate(self) -> None:
        """Authenticate using a service account JSON credentials file."""
        scopes = ["https://www.googleapis.com/auth/drive.readonly"]
        creds = service_account.Credentials.from_service_account_file(
            str(self.credentials_file), scopes=scopes
        )
        self.service = build("drive", "v3", credentials=creds)

    def list_files(self, folder_id: str) -> Dict[str, str]:
        """Return a mapping of file names to their ids within a folder."""
        query = f"'{folder_id}' in parents and trashed=false"
        results = (
            self.service.files()
            .list(q=query, fields="files(id,name)")
            .execute()
        )
        return {f["name"]: f["id"] for f in results.get("files", [])}

    def download_file(self, file_id: str, destination: Path) -> None:
        """Download a file identified by file_id to destination."""
        request = self.service.files().get_media(fileId=file_id)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with io.FileIO(destination, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        self.logger.info(f"Downloaded {destination.name} to {destination}")

    def download_files(self, required_files: List[str], destination: Path) -> None:
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        if not self.service:
            self.authenticate()
        files = self.list_files(self.folder_id)
        for file_name in required_files:
            file_id = files.get(file_name)
            dest = destination / file_name
            if file_id:
                self.download_file(file_id, dest)
            else:
                self.logger.error(f"Missing file in source drive: {file_name}")

