import logging

from error.filestore_error import FilestoreFactoryError
from helpers.filestore.filestor_provicer import FileStore
from helpers.filestore.filestore_local import LocalFileStore


class FileStoreFactory:
    """Factory class to create file storage provider instances."""

    providers = {
        "local": LocalFileStore,
    }

    @staticmethod
    def get_provider(provider_name: str, **kwargs) -> FileStore:
        """Returns an instance of the requested file storage provider."""
        provider_class = FileStoreFactory.providers.get(provider_name.lower())
        if not provider_class:
            logging.error(f"File storage provider {provider_name} not found.")
            raise FilestoreFactoryError(f"File storage provider '{provider_name}' is not supported.")
        return provider_class(**kwargs)
