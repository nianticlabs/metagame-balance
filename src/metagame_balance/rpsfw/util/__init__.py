import abc


class MetaData(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def clear_stats(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_metadata(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def evaluate(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_win_probs(self):
        raise NotImplementedError
