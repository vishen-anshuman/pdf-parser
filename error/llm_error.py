class LLMError(Exception):
    def __init__(self, message: str):
        super().__init__(f"LLMError : {message}")

class LLMFactoryError(LLMError):
    def __init__(self, message: str):
        super().__init__(f"LLMFactoryError : {message}")

class LLMAPIError(LLMError):
    def __init__(self, message: str):
        super().__init__(message)

class LLMParseError(LLMError):
    def __init__(self, message: str):
        super().__init__(message)
