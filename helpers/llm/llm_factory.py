import logging

from error.llm_error import LLMFactoryError
from helpers.llm.llm_gemini import GoogleGemini
from helpers.llm.llm_provider import LLMProvider


class LLMFactory:
    providers = {
        "google_gemini": GoogleGemini,
    }

    @staticmethod
    def get_provider(provider_name: str) -> LLMProvider:
        provider_class = LLMFactory.providers.get(provider_name.lower())
        if not provider_class:
            logging.error(f"Unknown provider for LLM {provider_name}")
            raise LLMFactoryError(f"LLM provider '{provider_name}' is not supported.")
        return provider_class()
