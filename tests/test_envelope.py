import pytest
from src.badge.badgeable import Badgeable
from src.badge.handled_badge import HandledBadge
from src.badge.received_badge import ReceivedBadge
from src.envelope import Envelope
from src.message import Message


class DummyBadge(Badgeable):
    def result(self):
        pass

    def handler_name(self):
        pass

class GreetMessage(Message):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class GreetMessageHandler:
    def __call__(self, message: GreetMessage):
        return f"Hello, {message.name}!"


class TestEnvelope:
    def test_constructor(self):
        badge = ReceivedBadge('transport')
        message = GreetMessage('Hello')
        badges = [badge]
        envelope = Envelope(message, badges)

        assert message == envelope.message
        assert type(badge) in envelope.all()
        assert badge == envelope.all()[type(badge)][0]

    def test_with_badges_returns_new_instance(self):
        message = GreetMessage('Hello')
        envelope = Envelope(message)

        assert envelope.with_badges(ReceivedBadge('transport')) != envelope
        print(envelope.with_badges(ReceivedBadge('transport')).all())

    def test_without_badges_returns_new_instance(self):
        message = GreetMessage('Hello')
        received_badge = ReceivedBadge('transport1')
        handled_badge = HandledBadge('Fake Result', 'test')
        badges = [received_badge, ReceivedBadge('transport2'), handled_badge]
        envelope = Envelope(message, badges)
        new_envelope = envelope.without_badges(type(received_badge))

        assert new_envelope != envelope
        assert len(new_envelope.all(type(received_badge))) == 0
        assert len(new_envelope.all(type(handled_badge))) == 1

    def test_without_badges_of_type(self):
        message = GreetMessage('Hello')
        received_badge= ReceivedBadge('transport1')
        handled_badge = HandledBadge('Fake Result', 'test')
        dummy_badge = DummyBadge()
        badges = [received_badge, ReceivedBadge('transport2'), handled_badge, dummy_badge]
        envelope = Envelope(message, badges)
        new_envelope = envelope.without_badges_of_type(Badgeable)

        assert len(new_envelope.all()) == 1


    def test_last(self):
        message = GreetMessage('Hello')
        received_badge = ReceivedBadge('transport1')
        received_badge2 = ReceivedBadge('transport2')
        handled_badge = HandledBadge('Fake Result', 'test')
        badges = [received_badge, received_badge2 , handled_badge]
        envelope = Envelope(message, badges)

        assert envelope.last(ReceivedBadge) == received_badge2
        assert envelope.last(HandledBadge) == handled_badge
        assert envelope.last(DummyBadge) == None
