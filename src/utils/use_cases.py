from abc import ABC, abstractmethod
from typing import Any, Union
from src.utils.executable import AbstractExecutable
from .types import TModel, TQS


class AbstractUseCase(AbstractExecutable, ABC):
    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    def execute(
        self, *args: object, **kwargs: object
    ) -> Union[TModel, TQS, Any, None]:
        pass
