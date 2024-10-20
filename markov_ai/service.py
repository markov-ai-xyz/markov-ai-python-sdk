import json
import requests
import logging
import traceback
from typing import Optional, Dict, Any
from requests_toolbelt import MultipartEncoder
from urllib.parse import urljoin


def post_multipart_data(
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


def post_json_data(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Optional[requests.Response]:
    """
    Make a POST request to the specified URL with the given data and headers.

    :param url: The endpoint URL to which the request will be sent.
    :param data: A dictionary containing the data to be sent in the request body.
    :param headers: A dictionary containing request headers.
    :return: The response object, or None if an error occurs.
    """
    try:
        if headers is None:
            headers = {}

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        if hasattr(e, 'response'):
            logging.error(f"Response status code: {e.response.status_code}")
            logging.error(f"Response text: {e.response.text}")
        logging.error(traceback.format_exc())
        return None


def get_json_data(
    base_url: str,
    postfix: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Optional[requests.Response]:
    """
    Make a GET request to the specified URL with an optional postfix, parameters, and headers.

    :param base_url: The base endpoint URL to which the request will be sent.
    :param postfix: An optional string to be appended to the base URL.
    :param params: A dictionary containing the query parameters to be sent in the request.
    :param headers: A dictionary containing request headers.
    :return: The response object, or None if an error occurs.
    """
    try:
        if headers is None:
            headers = {}

        url = base_url
        if postfix:
            url = urljoin(url, str(postfix))

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        if hasattr(e, 'response'):
            logging.error(f"Response status code: {e.response.status_code}")
            logging.error(f"Response text: {e.response.text}")
        logging.error(traceback.format_exc())
        return None
