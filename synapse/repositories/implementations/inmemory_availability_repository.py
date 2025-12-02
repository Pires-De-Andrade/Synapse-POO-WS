from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.availability import Availability

class InMemoryAvailabilityRepository(AbstractRepository[Availability]):
    def __init__(self, initial_data: Optional[List[Availability]]=None):
        self._availabilities = {a.id: a for a in (initial_data or [])}
        self._last_id = max(self._availabilities.keys(), default=0)

    def add(self, entity: Availability) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._availabilities[entity.id] = entity

    def get(self, entity_id: int) -> Optional[Availability]:
        return self._availabilities.get(entity_id)

    def all(self) -> List[Availability]:
        return list(self._availabilities.values())

    def update(self, entity: Availability) -> None:
        if entity.id in self._availabilities:
            self._availabilities[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._availabilities.pop(entity_id, None)

    def by_psychologist(self, psychologist_id: int) -> List[Availability]:
        return [a for a in self._availabilities.values() if a.psychologist_id == psychologist_id]
