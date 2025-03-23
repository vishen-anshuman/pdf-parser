import logging

from error.ocr_error import OCRFactoryError
from helpers.ocr.ocr_llama import LlamaParserOCR
from helpers.ocr.ocr_provider import OCRProvider


class OCRFactory:
    """Factory class to create OCR provider instances."""

    providers = {
        "llama": LlamaParserOCR
    }

    @staticmethod
    def get_provider(provider_name: str) -> OCRProvider:
        """Returns an instance of the requested OCR provider."""
        provider_class = OCRFactory.providers.get(provider_name.lower())
        if not provider_class:
            logging.error(f"Unknown OCR provider '{provider_name}'")
            raise OCRFactoryError(f"OCR provider '{provider_name}' is not supported.")
        return provider_class()
