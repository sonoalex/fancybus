import abc


class Badgeable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def result(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handler_name(self):
        raise NotImplementedError
