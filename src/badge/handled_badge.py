from dataclasses import dataclass
from typing import Any

from src.badge.badgeable import Badgeable


@dataclass
class HandledBadge(Badgeable):
    _result: Any
    _handler_name: str

    @property
    def result(self) -> Any:
        return self._result

    @property
    def handler_name(self) -> str:
        return self._handler_name

