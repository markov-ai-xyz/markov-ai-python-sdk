# DEPRECATED: This file is no longer actively maintained and may be removed in future versions.
# Please refer to the latest documentation for the current implementation.

import json
import logging
import mimetypes
from pathlib import Path
from typing import Any
from .service import post_multipart_data
from .constants import MARKOV_AI_BASE_URL, MARKOV_AI_UPLOAD_ENDPOINT, MAX_FILE_SIZE
from .destination import Destination


class Component:
    """
    DEPRECATED: A base class representing a component within a pipeline.

    This class is deprecated and will be removed in a future release.
    Please use the updated implementation as specified in the current documentation.

    :param name: The name of the component
    :param source: The file path or resource source associated with the component
    :param kwargs: Additional keyword arguments that can be dynamically assigned as attributes
    """

    def __init__(self, name: str, source: str, **kwargs: Any) -> None:
        logging.warning("DeprecationWarning: The Component class is deprecated and will be removed in a future version.")
        self.name = name
        self.source: Path = Path(source)
        self.__dict__.update(kwargs)

    def handle_file_selection(self) -> bool:
        """
        DEPRECATED: Checks if the selected file exists and if its size is within the allowed limit.
        """
        logging.warning("DeprecationWarning: handle_file_selection method is deprecated.")
        if not self.source.exists():
            logging.error("File not found")
            return False

        if self.source.stat().st_size > MAX_FILE_SIZE:
            logging.error(f"File size exceeds {MAX_FILE_SIZE / 1024 / 1024} MB")
            return False

        return True

    def run(self, api_key: str, destination: Destination) -> bool:
        """
        DEPRECATED: Upload the file to the API if it meets the size criteria.

        :param api_key: API key for authentication
        :param destination: A valid database destination, either for Neo4j or AWS Neptune, to be used in the pipeline
        :return: True if upload was successful, False otherwise
        """
        logging.warning("DeprecationWarning: run method is deprecated.")
        if not self.handle_file_selection():
            return False

        try:
            with self.source.open("rb") as file:
                mime_type, _ = mimetypes.guess_type(self.source.name)
                if mime_type is None:
                    mime_type = "application/octet-stream"

                data = destination.to_dict()
                fields = {
                    "data": json.dumps(data),
                    "file": (self.source.name, file, mime_type)
                }
                headers = {"Authorization": f"Bearer {api_key}"}

                response = post_multipart_data(
                    f"{MARKOV_AI_BASE_URL}{MARKOV_AI_UPLOAD_ENDPOINT}",
                    fields=fields,
                    headers=headers,
                )

                if response and response.status_code == 200:
                    logging.info("File uploaded successfully")
                    return True
                return False

        except IOError as e:
            logging.error(f"An error occurred while reading the file: {e}")
            return False
