import pytest
from src.bus import MessageHandler, FancyBus
from src.message import Message

import pytest
from src.bus import MessageHandler, FancyBus
from src.message import Message

@pytest.fixture
def test_message():
    class TestMessage(Message):
        value = "Some data"
    return TestMessage()


@pytest.fixture(scope="function")
def message_handler():
    yield MessageHandler()

@pytest.fixture(scope="function")
def bus(message_handler):
    yield FancyBus(message_handler)

@pytest.fixture
def test_handler():
    def handler(msg):
        return "handled"
    return handler

class TestFancyBus:
    def test_register_handler(self, bus, test_handler, test_message):
        
        bus.register_handler(test_message, test_handler)
        assert type(test_message) in bus.message_handler.handlers
        assert test_handler in bus.message_handler.handlers[type(test_message)]

    def test_dispatch_without_middleware(self, bus, test_handler, test_message):
        bus.register_handler(test_message, test_handler)
        result = bus.dispatch(test_message)
        assert result == "handled"

    def test_dispatch_with_middleware(self, bus, test_handler, test_message):
        def middleware(next_handler):
            return lambda msg: "middleware " + next_handler(msg)
        bus.register_handler(test_message, test_handler)
        bus.add_middleware(middleware)
        result = bus.dispatch(test_message)
        assert result == "middleware handled"

    def test_add_middleware(self, bus):
        def middleware(next_handler):
            return lambda msg: "middleware " + next_handler(msg)
        bus.add_middleware(middleware)
        assert middleware in bus.middleware 

    def test_dispatch_with_multiple_middlewares(self, bus, test_handler, test_message):
        def middleware1(next_handler):
            return lambda msg: "middleware1 " + next_handler(msg)
        def middleware2(next_handler):
            return lambda msg: "middleware2 " + next_handler(msg)
        bus.register_handler(test_message, test_handler)
        bus.add_middleware(middleware1)
        bus.add_middleware(middleware2)

        result = bus.dispatch(test_message)
        assert result == "middleware1 middleware2 handled"
