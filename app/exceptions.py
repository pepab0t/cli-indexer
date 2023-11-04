class IndexerException(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self):
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.message}')"


class ArgumentException(IndexerException):
    pass


class MissingCommandException(IndexerException):
    pass


class InvalidCommandException(IndexerException):
    pass
