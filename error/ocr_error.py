class OCRError(Exception):
    def __init__(self, message: str):
        super().__init__(f"OCRError : {message}")

class OCRFactoryError(OCRError):
    def __init__(self, message: str):
        super().__init__(f"OCRFactoryError : {message}")

class OCRUploadError(OCRError):
    def __init__(self, message: str):
        super().__init__(message)

class OCRDownloadError(OCRError):
    def __init__(self, message: str):
        super().__init__(message)
