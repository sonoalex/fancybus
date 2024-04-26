from dataclasses import dataclass


@dataclass
class ReceivedBadge:  # NonSendableStampInterface
    _transport_name: str

    @property
    def transport_name(self) -> str:
        return self._transport_name