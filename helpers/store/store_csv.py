import csv
import logging
import os
from typing import Optional, Dict, List

import pandas as pd
from pydantic import BaseModel

from error.store_error import StoreInsertError, StoreFetchError
from helpers.store.store_provider import Database


class CSVDatabase(Database):
    """CSV-based database implementation."""

    def __init__(self, directory="csv_db"):
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def insert_query(self, table: str, row: BaseModel):
        try:
            file_path = os.path.join(self.directory, f"{table}.csv")
            file_exists = os.path.isfile(file_path)

            with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(row.dict().keys())
                writer.writerow(row.dict().values())
            logging.info(f"row {row} inserted in Table {table} in CSV Store")
        except OSError as e:
            logging.error(f"Could not into insert {table}.csv {row} in CSV Store: {e}")
            raise StoreInsertError(f"Could not into insert {table}.csv {row} in CSV Store")

    def fetch_results(self, table: str, primary_id: Optional[str] = None) -> Optional[List[Dict]]:
        try:
            file_path = os.path.join(self.directory, f"{table}.csv")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Table '{table}' does not exist.")

            df = pd.read_csv(file_path)

            if "Id" not in df.columns:
                raise ValueError(f"Table '{table}' does not have an 'Id' column.")
            if not primary_id:
                return df.to_dict(orient="records")
            record = df[df["Id"] == primary_id]
            logging.info(f"Data success fully fetched from table '{table}' in CSV Store")
            return record.to_dict(orient="records")[0] if not record.empty else None
        except OSError as e:
            logging.error(f"Could not into fetch {table}.csv {primary_id}: {e} form csv store")
            raise StoreFetchError("Could not fetch data from table '{table}' in CSV Store")
