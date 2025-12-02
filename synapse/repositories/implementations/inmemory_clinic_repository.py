from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.clinic import Clinic

class InMemoryClinicRepository(AbstractRepository[Clinic]):
    def __init__(self, initial_data: Optional[List[Clinic]]=None):
        self._clinics = {c.id: c for c in (initial_data or [])}
        self._last_id = max(self._clinics.keys(), default=0)

    def add(self, entity: Clinic) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._clinics[entity.id] = entity

    def get(self, entity_id: int) -> Optional[Clinic]:
        return self._clinics.get(entity_id)

    def all(self) -> List[Clinic]:
        return list(self._clinics.values())

    def update(self, entity: Clinic) -> None:
        if entity.id in self._clinics:
            self._clinics[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._clinics.pop(entity_id, None)
