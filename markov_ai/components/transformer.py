import logging
from typing import Any, Dict, Optional
from ..service import post_json_data
from ..constants import MARKOV_AI_BASE_URL, MARKOV_AI_EMBEDDINGS_ENDPOINT,MARKOV_AI_REF_EMBEDDING_ENDPOINT


class Transformer:
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)
        self.api_key = kwargs.get('api_key')


    def generate_ref_embedding(self, markov_s3_key: str) -> Optional[Dict[str, Any]]:
            """
            :param markov_s3_key: Markov-side S3 key, pointing to the object.
            :return: Response from the /process endpoint.
            """
            url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_REF_EMBEDDING_ENDPOINT}"
            data = {
                "markov_s3_key": markov_s3_key,
            }

            headers = self._get_headers()
            response = post_json_data(url, data=data, headers=headers)
            return self._handle_response(response, "Processed S3 file successfully")

    def generate_embedding(self, input:str) -> Optional[Dict[str,any]]:
        """
        :param input: Input text for generating embeddings.
        :return: Response from the /process endpoint.
        """
        url = f"{MARKOV_AI_BASE_URL}{MARKOV_AI_EMBEDDINGS_ENDPOINT}"
        data = {
            "input": input,
        }

        headers = self._get_headers()
        response = post_json_data(url, data=data, headers=headers)
        return self._handle_response(response, "Generated embeddings successfully")
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
