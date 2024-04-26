import copy
from collections import defaultdict


class Envelope:
    """A wrapper for messages with additional badges.

    Attributes:
        message (object): The message to be wrapped.
        badges (defaultdict): A dictionary of badges associated with the message.

    Methods:
        wrap(message: object, badges: list): Wraps a message with badges in an envelope.
        with_badges(*badges): Returns a copy of the envelope with additional badges.
        without_badges(badge_fqcn): Returns a copy of the envelope without the specified badges.
        all(badge_fqcn=None): Returns all badges or badges of a specified type.
        without_badges_of_type(class_type): Returns a copy of the envelope without badges of a specified type.
    """
    def __init__(self, message: object, badges: list = None) -> None:
        """Initializes the Envelope with a message and optional badges.

        Args:
            message (object): The message to be wrapped.
            badges (list, optional): A list of badges to be associated with the message. Defaults to None.
        """
        self.message = message

        if badges is None:
            badges = []

        self.badges = defaultdict(list)

        for badge in badges:
            self.badges[type(badge)].append(badge)

    @classmethod
    def wrap(cls, message: object, badges: list):
        """Wraps a message with badges in an envelope.

        Args:
            message (object): The message to be wrapped.
            badges (list): A list of badges to be associated with the message.

        Returns:
            Envelope: The envelope containing the message and badges.
        """
        envelope = message if isinstance(message, Envelope) else cls(message)

        return envelope.with_badges(*badges)

    def with_badges(self, *badges):

        cloned = copy.deepcopy(self)

        for badge in badges:
            cloned.badges[type(badge)].append(badge)

        return cloned

    def without_badges(self, badge_fqcn):
        cloned = copy.deepcopy(self)

        cloned.badges.pop(badge_fqcn)

        return cloned

    def all(self, badge_fqcn=None):

        if None is not badge_fqcn:
            return self.badges[badge_fqcn] if self.badges[badge_fqcn] else []

        return self.badges

    def without_badges_of_type(self, class_type):
        cloned = copy.deepcopy(self)
        remove = [k for k in cloned.badges if k == class_type or issubclass(k, class_type)]
        for k in remove:
            del cloned.badges[k]

        return cloned
    
    def last(self, badge_fqcn):
        return self.badges.get(badge_fqcn, [])[-1] if badge_fqcn in self.badges else None


    def __eq__(self, other):
        return self is other
