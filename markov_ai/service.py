import json
import requests
import logging
import traceback
from typing import Optional, Dict, Any
from requests_toolbelt import MultipartEncoder


def make_post_request(
    url: str,
    fields: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Optional[requests.Response]:
    """
    Make a POST request to the specified URL with the given files and headers.

    :param url: The endpoint URL to which the request will be sent.
    :param fields: A dictionary containing the files to be uploaded.
    :param headers: A dictionary containing request headers.
    :return: The response object, or None if an error occurs.
    """
    try:
        if headers is None:
            headers = {}

        multipart_data = MultipartEncoder(fields=fields)
        headers['Content-Type'] = multipart_data.content_type

        response = requests.post(url, data=multipart_data, headers=headers)
        response.raise_for_status()
        return response

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        if hasattr(e, 'response'):
            logging.error(f"Response status code: {e.response.status_code}")
            logging.error(f"Response text: {e.response.text}")
        logging.error(traceback.format_exc())
        return None
