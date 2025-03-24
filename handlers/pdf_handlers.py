import asyncio
import logging
import os
from typing import List, Dict, Any, Coroutine, Optional
from uuid import uuid4

from fastapi import UploadFile
from pydantic import BaseModel

from error.api_error import APIError
from error.filestore_error import FilestoreFactoryError
from error.llm_error import LLMFactoryError
from error.ocr_error import OCRFactoryError
from error.store_error import StoreFactoryError
from helpers.filestore.filestore_factory import FileStoreFactory
from helpers.llm.llm_factory import LLMFactory
from helpers.llm.llm_provider import LLMProvider
from helpers.ocr.ocr_factory import OCRFactory
from helpers.ocr.ocr_provider import OCRProvider
from helpers.store.store_factory import DatabaseFactory
from helpers.store.store_provider import Database
from models.model_resume import ResumeModel

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def upload_pdfs(files: List[UploadFile]) -> Dict:
    uploaded_list = []
    try:
        filestore_provider = FileStoreFactory.get_provider(provider_name="local")
        ocr_provider = OCRFactory.get_provider(provider_name="llama")
        llm_provider = LLMFactory.get_provider(provider_name="google_gemini")
        database_provider = DatabaseFactory.get_provider(provider_name="csv")
    except {FilestoreFactoryError, OCRFactoryError, LLMFactoryError, StoreFactoryError} as e:
        raise e
    for file in files:
        try:
            unique_id = str(uuid4())
            uploaded_file_path, file_path = await __upload_to_filestore(file, filestore_provider, unique_id)
            logging.info(f"[/upload-pdfs/] Uploaded to filestore :: {file_path}")
            if os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Deleted: {file_path}")
            await file.close()
        except Exception as e:
            logging.error(f"[/upload-pdfs/] Failed to upload file for {file.filename} : {e}")
            raise e
        # DO OCR
        file_info = {"id": unique_id, "file_name": uploaded_file_path}
        uploaded_list.append(file_info)
    asyncio.create_task(__process_uploads(ocr_provider, llm_provider, database_provider, uploaded_list))
    logging.info(f"[/upload-pdfs/] Uploaded {len(uploaded_list)} files")
    return {"uploaded_files": uploaded_list}


async def get_all_uploads(page: int, page_size: int) -> Coroutine[Any, Any, Any]:
    try:
        data_base = DatabaseFactory.get_provider(provider_name="csv")
        data = data_base.fetch_results("resume_text", "")
        logging.info(f"[/get-all-uploads/] Fetched data from database, {data}")
        return data
    except Exception as e:
        logging.error(f"[/get-all-uploads/] Failed to fetch data: {e}")
        raise e


async def get_upload_by_id(upload_id: str) -> Optional[Coroutine[Any, Any, dict]]:
    try:
        data_base = DatabaseFactory.get_provider(provider_name="csv")
        data = data_base.fetch_results("resume_text", upload_id)
        logging.info(f"[/get_upload_by_id/] Fetched data from database, for id {upload_id}: {data}")
        return data
    except Exception as e:
        logging.error(f"[/get-all-uploads/] Failed to fetch data: for id {upload_id} {e}")


## Private functions
async def __upload_to_filestore(file, filestore_provider, unique_id):
    new_file_name = f"{unique_id}_{file.filename}"
    try:
        file_path = os.path.join(UPLOAD_DIR, new_file_name)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        uploaded_file_path = filestore_provider.upload_file(file_path, destination=f"pdf/{new_file_name}").get("file_path")
        logging.info(f"[__upload_to_filestore] Uploaded to filestore, {file_path}")
        os.remove(file_path)
        f.close()
        return uploaded_file_path, file_path
    except OSError as e:
        logging.error(f"File {new_file_name} could not be uploaded due to OS error: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error occurred while uploading {new_file_name}: {e}", exc_info=True)


async def __process_uploads(ocr_provider: OCRProvider,
                            llm_provider: LLMProvider,
                            data_base: Database,
                            uploaded_filepaths: []) -> None:
    for uploaded_filepath in uploaded_filepaths:
        try:
            ocr_id = await ocr_provider.extract_text(uploaded_filepath["file_name"])
            ocr_text = await ocr_provider.fetch_text(ocr_id)
            relevant_data = llm_provider.extract_information(text=ocr_text, query=resume_prompt)
            data_base.insert_query("resume_text", __convert_to_model(relevant_data, uploaded_filepath["id"]))
            logging.info(f"[/__process_uploads/] Data Processed for the file , {uploaded_filepath}")
        except APIError as e:
            logging.error(f"[/process-upload/] Failed to extract data: API Error for {uploaded_filepath} {e}")
        except Exception as e:
            logging.error(f"[/process-upload/] Processing failed the file: for {uploaded_filepath} {e}")


def __convert_to_model(data: Dict, primary_id: str) -> BaseModel:
    data.setdefault("Id", primary_id)
    return ResumeModel.model_validate(data)


resume_prompt = """
        Extract the following details from the given resume text:
        - Full Name
        - Highest Education Degree
        - Work Experience (years + relevant roles)
        - Profession/Job Title
        - A concise Profile Summary

        Provide the output in JSON format with these fields: Name, Education, Experience, Profession, ProfileSummary.

        Resume Text:
        """
