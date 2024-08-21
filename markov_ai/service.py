import requests
import logging
from typing import Optional


def make_post_request(
    url: str, files: dict, headers: dict
) -> Optional[requests.Response]:
    """
    Make a POST request to the specified URL with the given files and headers.

    :param url: The endpoint URL to which the request will be sent.
    :param files: A dictionary containing the files to be uploaded.
    :param headers: A dictionary containing request headers.
    :return: The response object, or None if an error occurs.
    """
    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None
