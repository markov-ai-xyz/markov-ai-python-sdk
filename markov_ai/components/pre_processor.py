import logging
from typing import Any, Dict, Optional
from ..service import post_json_data
from ..constants import MARKOV_AI_BASE_URL, MARKOV_AI_PARSE_ENDPOINT


class PreProcessor:
    """
    Component class representing a pre-processor.

    :param kwargs: Additional keyword arguments that can be dynamically assigned as attributes
    """

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)
        self.api_key = kwargs.get('api_key')

    def parse(self, markov_s3_key: str, resolution: str = "high_res") -> Optional[Dict[str, Any]]:
        """
        Parse an artifact from Markov's bucket.

        :param markov_s3_key: Markov-side S3 key, pointing to the object
        :param resolution: The resolution for evaluation
        :return: True if streaming was successful, False otherwise
        """
        url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_PARSE_ENDPOINT}"
        data = {
            "markov_s3_key": markov_s3_key,
            "kwargs": {
                "res": resolution
            }
        }
        headers = self._get_headers()

        response = post_json_data(url, data=data, headers=headers)
        return self._handle_response(response, "Parsing artifact")

    def _get_headers(self) -> Dict[str, str]:
        """Helper method to prepare the headers for API requests."""
        return {
            "X-API-Key": self.api_key
        }

    @staticmethod
    def _handle_response(response: Optional[Any], operation: str) -> Optional[Dict[str, Any]]:
        """Helper method to handle API responses."""
        if response and response.status_code == 200:
            logging.info(f"{operation} successful")
            return response.json()
        logging.error(f"{operation} failed: {response.text if response else 'No response'}")
        return None
