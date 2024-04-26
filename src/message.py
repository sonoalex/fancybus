from dataclasses import dataclass

@dataclass
class Message:
    transports: list = None  # List of transports this message should use
