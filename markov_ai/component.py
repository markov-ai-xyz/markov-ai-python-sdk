import logging
import mimetypes
from pathlib import Path
from typing import Any
from .service import make_post_request
from .constants import MARKOV_AI_BASE_URL, MARKOV_AI_UPLOAD_ENDPOINT, MAX_FILE_SIZE


class Component:
    """
    A base class representing a component within a pipeline.

    :param name: The name of the component
    :param source: The file path or resource source associated with the component
    :param kwargs: Additional keyword arguments that can be dynamically assigned as attributes
    """

    def __init__(self, name: str, source: str, **kwargs: Any) -> None:
        self.name = name
        self.source: Path = Path(source)
        self.__dict__.update(kwargs)

    def handle_file_selection(self) -> bool:
        """
        Checks if the selected file exists and if its size is within the allowed limit.
        """
        if not self.source.exists():
            logging.error("File not found")
            return False

        if self.source.stat().st_size > MAX_FILE_SIZE:
            logging.error(f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024} MB")
            return False

        return True

    def run(self, api_key: str) -> bool:
        """
        Upload the file to the API if it meets the size criteria.

        :param api_key: API key for authentication
        :return: True if upload was successful, False otherwise
        """
        if not self.handle_file_selection():
            return False

        try:
            with self.source.open("rb") as file:
                mime_type, _ = mimetypes.guess_type(self.source.name)
                if mime_type is None:
                    mime_type = "application/octet-stream"

                form_data = {"file": (self.source.name, file, mime_type)}
                headers = {"Authorization": f"Bearer {api_key}"}

                response = make_post_request(
                    f"{MARKOV_AI_BASE_URL}{MARKOV_AI_UPLOAD_ENDPOINT}",
                    files=form_data,
                    headers=headers,
                )

                if response and response.status_code == 200:
                    logging.info("File uploaded successfully")
                    return True
                else:
                    logging.error(
                        f"Failed to upload file. Status code: "
                        f"{response.status_code if response else 'No response'}"
                    )
                    return False

        except IOError as e:
            logging.error(f"An error occurred while reading the file: {e}")
            return False
