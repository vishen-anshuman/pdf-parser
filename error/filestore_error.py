class FilestoreError(Exception):
    def __init__(self, message: str):
        super().__init__(f"FilestoreError : {message}")

class FilestoreFactoryError(FilestoreError):
    def __init__(self, message: str):
        super().__init__(f"FilestoreProviderError : {message}")

class FilestoreDownloadError(FilestoreError):
    def __init__(self, message: str):
        super().__init__(message)

class FilestoreUploadError(FilestoreError):
    def __init__(self, message: str):
        super().__init__(message)