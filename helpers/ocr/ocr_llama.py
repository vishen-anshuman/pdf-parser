import logging
import os

import requests

from error.ocr_error import OCRUploadError, OCRDownloadError
from helpers.ocr.ocr_provider import OCRProvider

LLAMA_PARSER_API_KEY = ""

LLAMA_PARSER_UPLOAD_API_URL = "https://api.cloud.llamaindex.ai/api/v1/parsing/upload"

LLAMA_PARSER_RESULT_TEXT = "https://api.cloud.llamaindex.ai/api/v1/parsing/job"


def upload_file_to_llama(path: str):
    logging.info(f"Uploading {path} to Llama...")

    headers = {
        "Authorization": f"Bearer {LLAMA_PARSER_API_KEY}",
        "Accept": "application/json"
    }

    file = open(path, "rb")
    try:
        files = {
            "file": (os.path.basename(file.name), file, "application/pdf")
        }
        response = requests.post(LLAMA_PARSER_UPLOAD_API_URL, headers=headers, files=files)
    except Exception as error:
        logging.error(f"Error uploading {path} to Llama: {error}")
        raise OCRUploadError(f"Error uploading {path} to Llama: {error}")
    finally:
        file.close()

    if response.status_code == 200:
        logging.info(f"Uploaded {path} to Llama successfully.")
        return response.json()["id"]
    else:
        logging.error(f"Getting non 200 response from llama : {response.status_code}")
        raise OCRUploadError("Error getting non 200 response from llama")


def get_llama_parsing_result(job_id: str) -> str:
    url = f"{LLAMA_PARSER_RESULT_TEXT}/{job_id}/result/text"
    headers = {
        "Authorization": f"Bearer {LLAMA_PARSER_API_KEY}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
    except Exception as error:
        logging.error(f"Error IN getting data from Llama for job_id : {job_id}: {error}")
        raise OCRDownloadError(f"Error getting {url}: {error}")

    if response.status_code == 200:
        logging.info(f"Getting data from llama for {job_id} successfully.")
        return response.json()
    else:
        logging.error(f"Getting non 200 response from llama for {job_id} : {response.status_code}")
        raise OCRDownloadError(f"Getting non 200 response from llama for{job_id}: {response.status_code}")


class LlamaParserOCR(OCRProvider):

    async def extract_text(self, file_path: str) -> str:
        return upload_file_to_llama(file_path)

    async def fetch_text(self, extract_id: str) -> str:
        return get_llama_parsing_result(extract_id)
