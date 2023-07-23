import pickle

import pytest

import apacai

EXCEPTION_TEST_CASES = [
    apacai.InvalidRequestError(
        "message",
        "param",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    apacai.error.AuthenticationError(),
    apacai.error.PermissionError(),
    apacai.error.RateLimitError(),
    apacai.error.ServiceUnavailableError(),
    apacai.error.SignatureVerificationError("message", "sig_header?"),
    apacai.error.APIConnectionError("message!", should_retry=True),
    apacai.error.TryAgain(),
    apacai.error.Timeout(),
    apacai.error.APIError(
        message="message",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    apacai.error.ApacAIError(),
]


class TestExceptions:
    @pytest.mark.parametrize("error", EXCEPTION_TEST_CASES)
    def test_exceptions_are_pickleable(self, error) -> None:
        assert error.__repr__() == pickle.loads(pickle.dumps(error)).__repr__()
