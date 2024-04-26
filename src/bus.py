
from typing import Callable, List

from src.envelope import Envelope
from src.handlers import MessageHandler
from src.middleware import Middleware
from src.message import Message



class FancyBus:
  """A bus system that handles messages with optional middleware.

  Attributes:
    message_handler (MessageHandler): The handler for messages.
    middleware (List[Middleware]): A list of middleware instances.

  Methods:
    register_handler(message: Message, handler: Callable): Registers a handler for a message type.
    dispatch(message: Message): Dispatches a message to the appropriate handler(s).
    add_middleware(middleware_instance: Middleware): Adds a middleware instance to the bus.
  """

  def __init__(self, message_handler: MessageHandler, middleware: List[Middleware] = None):
    """Initializes the FancyBus with a message handler and optional middleware.

    Args:
      message_handler (MessageHandler): The handler for messages.
      middleware (List[Middleware], optional): A list of middleware instances. Defaults to None.
    """
    self.message_handler = message_handler
    self.middleware = middleware or []

  def register_handler(self, message: Message, handler: Callable):
    """Registers a handler for a message type.

    Args:
      message (Message): The type of message to register the handler for.
      handler (Callable): The handler to register.
    """
    self.message_handler.register(message, handler)

  def dispatch(self, message: Message, badges: List = None):
    """Dispatches a message to the appropriate handler(s).

    If middleware is present, it is applied in the order it was added.

    Args:
      message (Message): The message to dispatch.

    Returns:
      The result of the handler(s) for the message type.
    """
    badges = badges or []
    envelope = Envelope.wrap(message, badges)

    if not self.middleware:
      return self.message_handler.handle(envelope)

    def build_chain():
      current = self.message_handler.handle
      for middleware_instance in reversed(self.middleware):
        current = middleware_instance(current)
      return current

    middleware_chain = build_chain()
    return middleware_chain(envelope)

  def add_middleware(self, middleware_instance: Middleware):
    """Adds a middleware instance to the bus.

    Args:
      middleware_instance (Middleware): The middleware instance to add.
    """
    self.middleware.append(middleware_instance)