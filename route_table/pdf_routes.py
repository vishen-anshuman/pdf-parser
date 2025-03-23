import logging
from typing import List

from fastapi import APIRouter, File, UploadFile, Query

from error.api_error import ServerError, BadRequestError
from handlers import pdf_handlers

router = APIRouter(prefix="/api/v1/pdf")


@router.post("/upload-pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise BadRequestError(
                message="Invalid file type. Only PDF files are allowed."
            )
        await file.close()
    logging.info(f"[/upload-pdfs/] Received {len(files)} files, processing...")
    try:
        return await pdf_handlers.upload_pdfs(files)
    except Exception as e:
        raise ServerError(
            message=f"Failed to upload files: {e}"
        )


@router.get("/retrieve/")
async def get_all_uploads(
        page: int = Query(1, alias="page", ge=1),
        page_size: int = Query(10, alias="page_size", ge=1)
):
    logging.info(f"[/retrieve/] Received  request for data of the pdfs uploaded...")
    try:
        return await pdf_handlers.get_all_uploads(page, page_size)
    except Exception as e:
        raise ServerError(
            message=f"Failed to retrieve data of the pdfs uploaded: {e}"
        )


@router.get("/retrieve/{upload_id}")
async def get_upload_by_id(upload_id: str):
    logging.info(f"[/retrieve/{upload_id}] Received request for getting pdf data for {upload_id}...")
    try:
        return await pdf_handlers.get_upload_by_id(upload_id)
    except Exception as e:
        raise ServerError(
            message=f"Failed to retrieve data of the pdfs uploaded: {e}"
        )
