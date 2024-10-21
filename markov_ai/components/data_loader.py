import json
import logging
import mimetypes
from pathlib import Path
from typing import Any, Dict, Optional
from ..service import get_json_data, post_json_data, post_multipart_data
from ..constants import (
    MARKOV_AI_BASE_URL,
    MARKOV_AI_LOCAL_UPLOAD_ENDPOINT,
    MARKOV_AI_STREAM_ENDPOINT,
    MARKOV_AI_STREAM_ASYNC_ENDPOINT,
    MARKOV_AI_STREAM_STATUS_ENDPOINT
)


class DataLoader:
    """
    Component class representing a data loader.

    :param kwargs: Additional keyword arguments that can be dynamically assigned as attributes
    """

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)
        self.api_key = kwargs.get('api_key')

    def upload(self, file_path: str) -> bool:
        """
        Upload a file to the Markov AI service.

        :param file_path: Path to the file to be uploaded
        :return: True if upload was successful, False otherwise
        """
        if not self._is_valid_file(file_path):
            return False

        try:
            source: Path = Path(file_path)
            with source.open("rb") as file:
                mime_type, _ = mimetypes.guess_type(source.name)
                if mime_type is None:
                    mime_type = "application/octet-stream"

                fields = {
                    "file": (source.name, file, mime_type)
                }
                headers = self._get_headers()

                response = post_multipart_data(
                    f"{MARKOV_AI_BASE_URL}{MARKOV_AI_LOCAL_UPLOAD_ENDPOINT}",
                    fields=fields,
                    headers=headers,
                )

                return self._handle_response(response, "File upload")

        except IOError as e:
            logging.error(f"An error occurred while reading the file: {e}")
            return False

    def stream(self, pre_signed_url: str) -> bool:
        """
        Stream data from a pre-signed URL.

        :param pre_signed_url: The pre-signed URL to stream from
        :return: True if streaming was successful, False otherwise
        """
        url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_STREAM_ENDPOINT}"
        data = {"pre_signed_url": pre_signed_url}
        headers = self._get_headers()

        response = post_json_data(url, data=data, headers=headers)
        return self._handle_response(response, "Synchronous data streaming")

    def stream_async(self, pre_signed_url: str) -> Optional[str]:
        """
        Initiate asynchronous streaming from a pre-signed URL.

        :param pre_signed_url: The pre-signed URL to stream from
        :return: Task ID if successful, None otherwise
        """
        url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_STREAM_ASYNC_ENDPOINT}"
        data = {"pre_signed_url": pre_signed_url}
        headers = self._get_headers()

        response = post_json_data(url, data=data, headers=headers)
        if self._handle_response(response, "Async streaming initiation"):
            return response.json().get('task_id')
        return None

    def get_stream_status(self, task_id) -> str:
        """
        Get the status of an asynchronous streaming task.

        :param task_id: The ID of the task to check
        :return: The status of the task
        """
        url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_STREAM_STATUS_ENDPOINT}"
        headers = self._get_headers()

        response = get_json_data(url, postfix=task_id, headers=headers)
        if self._handle_response(response, "Stream status check"):
            return response.json().get('status', 'Unknown')
        return "Failed to retrieve status"

    def _get_headers(self) -> Dict[str, str]:
        """Helper method to prepare the headers for API requests."""
        return {
            "X-API-Key": self.api_key
        }

    @staticmethod
    def _is_valid_file(file_path: str) -> bool:
        """Helper method to validate the file before upload."""
        path = Path(file_path)
        if not path.exists():
            logging.error(f"File not found: {file_path}")
            return False
        if not path.is_file():
            logging.error(f"Not a file: {file_path}")
            return False
        return True

    @staticmethod
    def _handle_response(response: Optional[Any], operation: str) -> bool:
        """Helper method to handle API responses."""
        if response and response.status_code == 200:
            logging.info(f"{operation} successful")
            return True
        logging.error(f"{operation} failed: {response.text if response else 'No response'}")
        return False
