import logging
import os
import re
import sys
from enum import Enum
from typing import Optional

import apacai

APACAI_LOG = os.environ.get("APACAI_LOG")

logger = logging.getLogger("apacai")

__all__ = [
    "log_info",
    "log_debug",
    "log_warn",
    "logfmt",
]

api_key_to_header = (
    lambda api, key: {"Authorization": f"Bearer {key}"}
    if api in (ApiType.OPEN_AI, ApiType.AZURE_AD)
    else {"api-key": f"{key}"}
)


class ApiType(Enum):
    AZURE = 1
    OPEN_AI = 2
    AZURE_AD = 3

    @staticmethod
    def from_str(label):
        if label.lower() == "azure":
            return ApiType.AZURE
        elif label.lower() in ("azure_ad", "azuread"):
            return ApiType.AZURE_AD
        elif label.lower() in ("open_ai", "apacai"):
            return ApiType.OPEN_AI
        else:
            raise apacai.error.InvalidAPIType(
                "The API type provided in invalid. Please select one of the supported API types: 'azure', 'azure_ad', 'open_ai'"
            )


def _console_log_level():
    if apacai.log in ["debug", "info"]:
        return apacai.log
    elif APACAI_LOG in ["debug", "info"]:
        return APACAI_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def log_warn(message, **params):
    msg = logfmt(dict(message=message, **params))
    print(msg, file=sys.stderr)
    logger.warn(msg)


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into ascii.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


def get_object_classes():
    # This is here to avoid a circular dependency
    from apacai.object_classes import OBJECT_CLASSES

    return OBJECT_CLASSES


def convert_to_apacai_object(
    resp,
    api_key=None,
    api_version=None,
    organization=None,
    engine=None,
    plain_old_data=False,
):
    # If we get a ApacAIResponse, we'll want to return a ApacAIObject.

    response_ms: Optional[int] = None
    if isinstance(resp, apacai.apacai_response.ApacAIResponse):
        organization = resp.organization
        response_ms = resp.response_ms
        resp = resp.data

    if plain_old_data:
        return resp
    elif isinstance(resp, list):
        return [
            convert_to_apacai_object(
                i, api_key, api_version, organization, engine=engine
            )
            for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(
        resp, apacai.apacai_object.ApacAIObject
    ):
        resp = resp.copy()
        klass_name = resp.get("object")
        if isinstance(klass_name, str):
            klass = get_object_classes().get(
                klass_name, apacai.apacai_object.ApacAIObject
            )
        else:
            klass = apacai.apacai_object.ApacAIObject

        return klass.construct_from(
            resp,
            api_key=api_key,
            api_version=api_version,
            organization=organization,
            response_ms=response_ms,
            engine=engine,
        )
    else:
        return resp


def convert_to_dict(obj):
    """Converts a ApacAIObject back to a regular dict.

    Nested ApacAIObjects are also converted back to regular dicts.

    :param obj: The ApacAIObject to convert.

    :returns: The ApacAIObject as a dict.
    """
    if isinstance(obj, list):
        return [convert_to_dict(i) for i in obj]
    # This works by virtue of the fact that ApacAIObjects _are_ dicts. The dict
    # comprehension returns a regular dict and recursively applies the
    # conversion to each value.
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    else:
        return obj


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def default_api_key() -> str:
    if apacai.api_key_path:
        with open(apacai.api_key_path, "rt") as k:
            api_key = k.read().strip()
            if not api_key.startswith("sk-"):
                raise ValueError(f"Malformed API key in {apacai.api_key_path}.")
            return api_key
    elif apacai.api_key is not None:
        return apacai.api_key
    else:
        raise apacai.error.AuthenticationError(
            "No API key provided. You can set your API key in code using 'apacai.api_key = <API-KEY>', or you can set the environment variable APACAI_API_KEY=<API-KEY>). If your API key is stored in a file, you can point the apacai module at it with 'apacai.api_key_path = <PATH>'. You can generate API keys in the APACAI web interface. See https://platform.apacai.com/account/api-keys for details."
        )
