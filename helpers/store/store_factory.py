import logging

from error.store_error import StoreFactoryError
from helpers.store.store_csv import CSVDatabase
from helpers.store.store_provider import Database


class DatabaseFactory:
    """Factory class to create database provider instances."""

    providers = {
        "csv": CSVDatabase,
    }

    @staticmethod
    def get_provider(provider_name: str, **kwargs) -> Database:
        """Returns an instance of the requested database provider."""
        provider_class = DatabaseFactory.providers.get(provider_name.lower())
        if not provider_class:
            logging.error(f"Unknown database provider '{provider_name}'")
            raise StoreFactoryError(f"Database provider '{provider_name}' is not supported.")
        return provider_class(**kwargs)
