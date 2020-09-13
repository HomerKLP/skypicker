# Vendor
from requests.exceptions import ConnectionError, Timeout
from json.decoder import JSONDecodeError
from rest_framework.exceptions import APIException
import requests
import logging

logger = logging.getLogger(__name__)


def perform_request(url: str, params: dict) -> dict:
    """Выполнить запрос во внешний сервис"""
    try:
        r = requests.get(url, params).json()
    except (ConnectionError, Timeout, JSONDecodeError) as e:
        logger.error("can't perform request: " + str(e))
        raise APIException(str(e), code='400;CANT_PERFORM_REQUEST')
    else:
        return r
