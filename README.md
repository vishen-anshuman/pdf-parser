## Application Summary

This application is designed to process and analyze PDF resumes. Here's a breakdown of its structure and functionality:

**Core Functionality:**

* **PDF Handling:**
    * The `handlers/pdf_handlers.py` module manages the primary logic for processing PDF files.
    * **API Controllers (Routes):** Routes for PDF processing are defined in `route_table/pdf_routes.py`. This module acts as the API controller, defining the endpoints and mapping them to the handler functions.
* **Data Extraction & Analysis:**
    * **OCR (Optical Character Recognition):** The `helpers/ocr` directory contains modules for extracting text from PDFs. It utilizes a factory pattern (`ocr_factory.py`) to choose between different OCR providers (e.g., `ocr_llama.py`).
    * **LLM (Large Language Model):** The `helpers/llm` directory handles natural language processing tasks. It uses a factory pattern (`llm_factory.py`) to select LLMs (e.g., `llm_gemini.py`) for analyzing extracted text.
* **Data Storage:**
    * The `helpers/store` directory manages data persistence. It uses a factory pattern (`store_factory.py`) to choose storage mechanisms (e.g., `store_csv.py`).
    * The application can store data into csv files, as shown by the `csv/sample.csv` file.
* **File Storage:**
    * The `helpers/filestore` directory handles file storage operations. It uses a factory pattern (`filestore_factory.py`) to choose different file storage providers (e.g., `filestore_local.py`).
    * Uploaded PDF files are stored in the `uploads/pdf` directory.
* **Data Modeling:**
    * `models/model_resume.py` defines the data model for resume information.
* **Error Handling:**
    * The `error` directory contains custom error classes for different components (API, filestore, LLM, OCR, store).
* **Main Application:**
    * `main.py` serves as the entry point for the application.
* **Testing:**
    * `test_main.http` can be used to test the api.
* **Dependencies:**
    * `requirement.txt` lists the application's Python dependencies.

**Key Design Patterns:**

* **Factory Pattern:** Used extensively in `helpers` directories (OCR, LLM, Store, Filestore) to provide flexibility and abstraction for choosing different implementations.
* **MVC (Model-View-Controller) Architectural Pattern (Partial):** Although not a full MVC implementation, the application demonstrates a separation of concerns:
    * **Model:** `models/model_resume.py`
    * **Controller:** `route_table/pdf_routes.py`
    * **View:** (Implicitly handled by the API responses, no explicit view layer is present).

**In essence, this application provides a modular and extensible framework for processing PDF resumes, extracting relevant information, analyzing it using LLMs, and storing the results. The `route_table` directory contains the API controllers that handle incoming requests and direct them to the appropriate processing logic.**

# Project Directory Structure

## Root Directory
- `README.md`
- `csv/`
  - `sample.csv`
- `error/`
  - `api_error.py`
  - `filestore_error.py`
  - `llm_error.py`
  - `ocr_error.py`
  - `store_error.py`
- `handlers/`
  - `pdf_handlers.py`
- `helpers/`
  - `filestore/`
    - `filestor_provicer.py`
    - `filestore_factory.py`
    - `filestore_local.py`
  - `llm/`
    - `llm_factory.py`
    - `llm_gemini.py`
    - `llm_provider.py`
  - `ocr/`
    - `ocr_factory.py`
    - `ocr_llama.py`
    - `ocr_provider.py`
  - `store/`
    - `store_csv.py`
    - `store_factory.py`
    - `store_provider.py`
- `main.py`
- `models/`
  - `model_resume.py`
- `requirement.txt`
- `route_table/`
  - `pdf_routes.py`
- `test_main.http`
- `uploads/`
  - `pdf/`




