from abc import ABC, abstractmethod, abstractproperty


class AbstractCommand(ABC):
    @abstractproperty
    def doc(self) -> str:
        ...

    @abstractproperty
    def name(self) -> str:
        ...

    @abstractmethod
    def execute(self, args: list[str] = list()) -> None:
        ...


class Command(AbstractCommand):
    @abstractmethod
    def parse_args(self, args: list[str]):
        ...
