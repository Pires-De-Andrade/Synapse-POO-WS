from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.patient import Patient

class InMemoryPatientRepository(AbstractRepository[Patient]):
    def __init__(self, initial_data: Optional[List[Patient]]=None):
        self._patients = {p.id: p for p in (initial_data or [])}
        self._last_id = max(self._patients.keys(), default=0)

    def add(self, entity: Patient) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._patients[entity.id] = entity

    def get(self, entity_id: int) -> Optional[Patient]:
        return self._patients.get(entity_id)

    def all(self) -> List[Patient]:
        return list(self._patients.values())

    def update(self, entity: Patient) -> None:
        if entity.id in self._patients:
            self._patients[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._patients.pop(entity_id, None)
