from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.psychologist import Psychologist

class InMemoryPsychologistRepository(AbstractRepository[Psychologist]):
    def __init__(self, initial_data: Optional[List[Psychologist]]=None):
        self._psychologists = {p.id: p for p in (initial_data or [])}
        self._last_id = max(self._psychologists.keys(), default=0)

    def add(self, entity: Psychologist) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._psychologists[entity.id] = entity

    def get(self, entity_id: int) -> Optional[Psychologist]:
        return self._psychologists.get(entity_id)

    def all(self) -> List[Psychologist]:
        return list(self._psychologists.values())

    def update(self, entity: Psychologist) -> None:
        if entity.id in self._psychologists:
            self._psychologists[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._psychologists.pop(entity_id, None)
