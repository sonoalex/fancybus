
from collections import defaultdict
from typing import Callable, Type

from src.envelope import Envelope
from src.exceptions import HandlerIsNotCallable, HandlerNotFound
from src.message import Message


class MessageHandler:
  def __init__(self):
    self.handlers = defaultdict(list)

  def register(self, message_class: Type[Message], handler: Callable):

    if not callable(handler):
      raise HandlerIsNotCallable(
        f"register() second argument must be a callable, got '{type(handler)}"
      )

    self.handlers[type(message_class)].append(handler)

  def handle(self, envelope: Envelope):
    handlers = self.handlers.get(type(envelope.message))

    if handlers:
      result = [handler(envelope.message) for handler in handlers]
      return result if len(result) > 1 else result[0]

    raise HandlerNotFound(f"No handler registered for message {type(envelope.message)}")