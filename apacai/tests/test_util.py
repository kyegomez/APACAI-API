import json
from tempfile import NamedTemporaryFile

import pytest

import apacai
from apacai import util


@pytest.fixture(scope="function")
def api_key_file():
    saved_path = apacai.api_key_path
    try:
        with NamedTemporaryFile(prefix="apacai-api-key", mode="wt") as tmp:
            apacai.api_key_path = tmp.name
            yield tmp
    finally:
        apacai.api_key_path = saved_path


def test_apacai_api_key_path(api_key_file) -> None:
    print("sk-foo", file=api_key_file)
    api_key_file.flush()
    assert util.default_api_key() == "sk-foo"


def test_apacai_api_key_path_with_malformed_key(api_key_file) -> None:
    print("malformed-api-key", file=api_key_file)
    api_key_file.flush()
    with pytest.raises(ValueError, match="Malformed API key"):
        util.default_api_key()


def test_key_order_apacai_object_rendering() -> None:
    sample_response = {
        "id": "chatcmpl-7NaPEA6sgX7LnNPyKPbRlsyqLbr5V",
        "object": "chat.completion",
        "created": 1685855844,
        "model": "gpt-3.5-turbo-0301",
        "usage": {"prompt_tokens": 57, "completion_tokens": 40, "total_tokens": 97},
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas. It was the first time that the World Series was played at a neutral site because of the COVID-19 pandemic.",
                },
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }

    oai_object = util.convert_to_apacai_object(sample_response)
    # The `__str__` method was sorting while dumping to json
    assert list(json.loads(str(oai_object)).keys()) == list(sample_response.keys())
