from abc import ABC, abstractmethod, abstractproperty


class AbstractCommand(ABC):
    @abstractmethod
    def execute(self, args: list[str] = list()) -> None:
        ...


class Command(AbstractCommand):
    @abstractproperty
    def doc(self) -> str:
        ...

    @abstractproperty
    def name(self) -> str:
        ...
