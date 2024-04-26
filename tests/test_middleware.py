import logging
import pytest
from src.middleware import Middleware, LoggingMiddleware
from src.bus import Message

@pytest.fixture
def message():
    return Message()

@pytest.fixture
def next_middleware():
    return lambda message: "next_middleware handled"

class TestMiddleware:
    def test_handle_without_next_middleware(self, message):
        middleware = Middleware()
        result = middleware.handle(message)
        assert result == message

    def test_handle_with_next_middleware(self, message, next_middleware):
        middleware = Middleware(next_middleware)
        result = middleware.handle(message)
        assert result == "next_middleware handled"

class TestLoggingMiddleware:
    def test_handle(self, message, next_middleware, caplog):
        caplog.set_level(logging.INFO)
        middleware = LoggingMiddleware(next_middleware)
        result = middleware.handle(message)
        assert "Handling message:" in caplog.text
        assert "Finished handling message. Result:" in caplog.text
        assert result == "next_middleware handled"