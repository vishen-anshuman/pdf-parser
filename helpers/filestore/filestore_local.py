import logging
import os
import shutil
from typing import Dict

from error.filestore_error import FilestoreUploadError
from helpers.filestore.filestor_provicer import FileStore


class LocalFileStore(FileStore):
    def __init__(self, base_path: str = "uploads"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def upload_file(self, file_path: str, destination: str) -> Dict:
        try:
            dest_path = os.path.join(self.base_path, destination)
            shutil.copy(file_path, dest_path)
            logging.info(f"Uploaded {file_path} to {dest_path} in local store")
            return {"provider": "local", "file_path": dest_path}
        except OSError as e:
            logging.error(f"Could not upload {file_path} to {destination}: {e} from local store")
            raise FilestoreUploadError(f"File {file_path} cannot be uploaded to {destination} in localstore: {e}")

    def get_file_url(self, file_name: str) -> str:
        """Returns the local file path."""
        return os.path.join(self.base_path, file_name)
