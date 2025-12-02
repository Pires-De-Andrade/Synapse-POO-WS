from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def all(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass
