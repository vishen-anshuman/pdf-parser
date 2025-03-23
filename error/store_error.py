class StoreError(Exception):
    def __init__(self, message: str):
        super().__init__(f"StoreError : {message}")


class StoreFactoryError(StoreError):
    def __init__(self, message: str):
        super().__init__(f"StoreFactoryError : {message}")


class StoreInsertError(StoreError):
    def __init__(self, message: str):
        super().__init__(message)


class StoreFetchError(StoreError):
    def __init__(self, message: str):
        super().__init__(message)
