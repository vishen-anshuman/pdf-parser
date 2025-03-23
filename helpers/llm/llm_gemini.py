import json
import logging
import re
from typing import Dict

import requests

from error.llm_error import LLMParseError, LLMError, LLMAPIError
from helpers.llm.llm_provider import LLMProvider

GOOGLE_API_KEY = ""


def clean_text(data: str) -> Dict[str, str]:
    try:
        if data is None:
            return {}
        data_str = data["candidates"][0]["content"]["parts"][0]["text"]
        clean_str = re.sub(r'```json\n|\n```', '', data_str).strip()
        json_data = json.loads(clean_str)
        return json_data
    except (KeyError, IndexError) as e:
        logging.error(f"Error while parsing gemini json response: {e}")
        raise LLMParseError(f"Error while parsing json: {e}")


class GoogleGemini(LLMProvider):

    def extract_information(self, text: str, query: str) -> Dict:
        try:
            prompt = f"""{query} {text}"""
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                logging.info(f"Prompt response successfully fetched from the gemini")
                return clean_text(data)
        except LLMError as e:
            logging.error(f"Error while parsing gemini response: {e}")
            raise e
        except Exception as e:
            logging.error(f"Error while parsing json: {e}")
            raise LLMAPIError(f"Error fetching prompt response form gemini: {e}")
