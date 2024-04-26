from abc import ABC, abstractmethod
from dataclasses import asdict
import json
from typing import Optional
import pika
import redis

from src.message import Message

class Transport(ABC):
    @abstractmethod
    def send(self, message: Message):
        pass


class RabbitMQTransport(Transport):
    def __init__(self, connection_string: str, queue_name: str, exchange_name: str):
        self.connection_string = connection_string
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self._connection = None
        self._channel = None

    def connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(self.connection_string))
        self._channel = self._connection.channel()

    def disconnect(self):
        if self._channel:
            self._channel.close()
        if self._connection:
            self._connection.close()

    def send(self, message: Message):
        self.connect()  # Ensure connection before sending
        try:
            # Assuming your message data is in the `message.data` attribute
            self._channel.basic_publish(exchange=self.exchange_name, routing_key=self.queue_name, body=json.dumps(asdict(message)))
        except Exception as e:
            print(f"Error sending message to RabbitMQ: {e}")
        finally:
            self.disconnect()  # Close connection after sending



class SNSTransport(Transport):
    def __init__(self, aws_credentials, topic_arn):
        # ... code to initialize AWS SNS client ...
        ...

    def send(self, message: Message):
        # ... code to send a message via AWS SNS ... 
        ...


class RedisTransport(Transport):
    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db
        self._redis = None

    def connect(self):
        self._redis = redis.Redis(host=self.host, port=self.port, db=self.db)

    def disconnect(self):
        if self._redis:
            self._redis.close()

    def send(self, message: Message):
        self.connect()  # Ensure connection before sending
        try:
            self._redis.publish(asdict(message))
        except Exception as e:
            print(f"Error sending message to Redis: {e}")
        finally:
            self.disconnect()  # Close connection after sending

