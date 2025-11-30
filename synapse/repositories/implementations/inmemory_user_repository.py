from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.user import User

class InMemoryUserRepository(AbstractRepository[User]):
    def __init__(self, initial_data: Optional[List[User]]=None):
        self._users = {u.id: u for u in (initial_data or [])}
        self._last_id = max(self._users.keys(), default=0)

    def add(self, entity: User) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._users[entity.id] = entity

    def get(self, entity_id: int) -> Optional[User]:
        return self._users.get(entity_id)

    def all(self) -> List[User]:
        return list(self._users.values())

    def update(self, entity: User) -> None:
        if entity.id in self._users:
            self._users[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._users.pop(entity_id, None)

    def get_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.email == email), None)
