import pytest
from src.envelope import Envelope
from src.handlers import MessageHandler
from src.exceptions import HandlerIsNotCallable, HandlerNotFound
from src.message import Message 

class TestMessageHandler:

    @pytest.fixture
    def message_handler(self):
        yield MessageHandler()

    @pytest.fixture
    def test_message(self):
        class TestMessage(Message):
            value = "Some data"
        return TestMessage()

    @pytest.fixture
    def another_message(self):
        class AnotherMessage(Message):
            data = {"key": "value"}
        return AnotherMessage()

    def test_handle_message_success(self, message_handler, test_message):
        def test_handler(message: Message):
            return "Test Result"
        envelope = Envelope(test_message)
        message_handler.register(test_message, test_handler)
        result = message_handler.handle(envelope)
        assert result == "Test Result"

    def test_handle_message_missing_handler(self, message_handler):
        class UnknownMessage(Message):
            pass

        with pytest.raises(HandlerNotFound):
            message_handler.handle(Envelope(UnknownMessage()))

    def test_register_non_callable_handler(self, message_handler):
        with pytest.raises(HandlerIsNotCallable):
            message_handler.register(Message, 123)  

    def test_handle_multiple_handlers(self, message_handler, test_message):
        results = []

        def handler1(message):
            results.append("Handler 1")

        def handler2(message):
            results.append("Handler 2")

        message_handler.register(test_message, handler1)
        message_handler.register(test_message, handler2)

        message_handler.handle(Envelope(test_message))
        assert results == ["Handler 1", "Handler 2"] 
