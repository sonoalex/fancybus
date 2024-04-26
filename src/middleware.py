import os
from typing import Callable
import logging

from src.message import Message
from src.transports import RabbitMQTransport, SNSTransport, Transport

class Middleware:
    def __init__(self, next_middleware: Callable[[Message], Message] = None):
        self.next_middleware = next_middleware

    def handle(self, message: Message) -> Message:
        if self.next_middleware:
            return self.next_middleware(message)
        
        return message  

from typing import Optional, List


class SendMessageMiddleware(Middleware):
    def __init__(self, next_middleware: Middleware = None):
        super().__init__(next_middleware)

    def handle(self, message: Message):

        transports = message.transports  
        successfully_sent = False 

        for transport_type in transports:
            transport = get_transport_instance(transport_type)  

            if transport:
                try:
                    transport.send(message)
                    successfully_sent = True  
                except Exception as e:
                    print(f"Error sending to {transport_type}: {e}")  

        if successfully_sent: 
            return

        return self.next(message) if self.next else message

import json

def load_configuration(path: str = "config.json"):
    if not os.path.exists(path):
        return {}
    
    with open(path) as f:
        return json.load(f)


def get_transport_instance(transport_type: str) -> Optional[Transport]:
    config = load_configuration()

    transport_config = config.get(transport_type)
    if not transport_config:
        return None

    transport_map = {
        "rabbitmq": RabbitMQTransport,
        "sns": SNSTransport
    }

    transport_cls = transport_map.get(transport_type)
    return transport_cls(**transport_config)


class LoggingMiddleware(Middleware):
    def handle(self, message: Message) -> Message:
        logging.info(f"Handling message: {message}")
        result = self.next_middleware(message) 
        logging.info(f"Finished handling message. Result: {result}")
        return result

