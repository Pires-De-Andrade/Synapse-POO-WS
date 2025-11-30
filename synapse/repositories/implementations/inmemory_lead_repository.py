from typing import List, Optional
from synapse.repositories.interfaces.abstract_repository import AbstractRepository
from synapse.business_model.lead import Lead

class InMemoryLeadRepository(AbstractRepository[Lead]):
    def __init__(self, initial_data: Optional[List[Lead]]=None):
        self._leads = {l.id: l for l in (initial_data or [])}
        self._last_id = max(self._leads.keys(), default=0)

    def add(self, entity: Lead) -> None:
        self._last_id += 1
        entity.id = self._last_id
        self._leads[entity.id] = entity

    def get(self, entity_id: int) -> Optional[Lead]:
        return self._leads.get(entity_id)

    def all(self) -> List[Lead]:
        return list(self._leads.values())

    def update(self, entity: Lead) -> None:
        if entity.id in self._leads:
            self._leads[entity.id] = entity

    def delete(self, entity_id: int) -> None:
        self._leads.pop(entity_id, None)

    def by_status(self, status: str) -> List[Lead]:
        return [l for l in self._leads.values() if l.status == status]
