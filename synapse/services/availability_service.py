"""
Serviço de gerenciamento de disponibilidades.
Contém a lógica de negócio para operações CRUD de disponibilidades de psicólogos.
"""

from datetime import time as dtime
from typing import List
from synapse.repositories.implementations.inmemory_availability_repository import InMemoryAvailabilityRepository
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.business_model.availability import Availability
from synapse.api.exceptions import NotFoundError, ValidationError, ConflictError


class AvailabilityService:
    """
    Serviço responsável pela lógica de negócio relacionada a disponibilidades.
    
    Attributes:
        availability_repository: Repositório para persistência de disponibilidades
        psychologist_repository: Repositório para validação de psicólogos
    """
    
    def __init__(self, availability_repository: InMemoryAvailabilityRepository,
                 psychologist_repository: InMemoryPsychologistRepository):
        self.availability_repository = availability_repository
        self.psychologist_repository = psychologist_repository

    def get_all(self):
        """Retorna todas as disponibilidades cadastradas."""
        return self.availability_repository.all()

    def get_by_id(self, availability_id: int):
        """
        Busca uma disponibilidade pelo ID.
        
        Args:
            availability_id: ID da disponibilidade
            
        Returns:
            Availability: Disponibilidade encontrada
            
        Raises:
            NotFoundError: Se a disponibilidade não for encontrada
        """
        availability = self.availability_repository.get(availability_id)
        if not availability:
            raise NotFoundError("Disponibilidade", availability_id)
        return availability

    def get_by_psychologist(self, psychologist_id: int) -> List[Availability]:
        """
        Retorna todas as disponibilidades de um psicólogo.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Returns:
            List[Availability]: Lista de disponibilidades
        """
        return self.availability_repository.by_psychologist(psychologist_id)

    def create_availability(self, psychologist_id: int, day_of_week: int,
                            start_time_str: str, end_time_str: str) -> Availability:
        """
        Cria uma nova disponibilidade para um psicólogo.
        
        Args:
            psychologist_id: ID do psicólogo
            day_of_week: Dia da semana (0=Segunda, 6=Domingo)
            start_time_str: Horário de início (HH:MM)
            end_time_str: Horário de fim (HH:MM)
            
        Returns:
            Availability: Disponibilidade criada
            
        Raises:
            NotFoundError: Se o psicólogo não for encontrado
            ValidationError: Se os dados forem inválidos
            ConflictError: Se houver sobreposição de horários
        """
        # Validar psicólogo
        psychologist = self.psychologist_repository.get(psychologist_id)
        if not psychologist:
            raise NotFoundError("Psicólogo", psychologist_id)
        
        # Validar dia da semana
        if day_of_week < 0 or day_of_week > 6:
            raise ValidationError("Dia da semana deve ser entre 0 (Segunda) e 6 (Domingo)", "day_of_week")
        
        # Converter horários
        try:
            start_time = dtime.fromisoformat(start_time_str)
            end_time = dtime.fromisoformat(end_time_str)
        except ValueError:
            raise ValidationError("Horário deve estar no formato HH:MM", "time")
        
        # Validar intervalo
        if start_time >= end_time:
            raise ValidationError("Horário de início deve ser anterior ao horário de fim", "start_time")
        
        # Verificar sobreposição
        existing = self.get_by_psychologist(psychologist_id)
        for av in existing:
            if av.day_of_week == day_of_week and av.is_active:
                if (start_time < av.end_time and end_time > av.start_time):
                    raise ConflictError(
                        f"Já existe disponibilidade neste dia das {av.start_time.strftime('%H:%M')} às {av.end_time.strftime('%H:%M')}"
                    )
        
        availability = Availability(
            psychologist_id=psychologist_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        self.availability_repository.add(availability)
        return availability

    def update_availability(self, availability_id: int, start_time_str: str = None,
                            end_time_str: str = None, is_active: bool = None) -> Availability:
        """
        Atualiza uma disponibilidade.
        
        Args:
            availability_id: ID da disponibilidade
            start_time_str: Novo horário de início (opcional)
            end_time_str: Novo horário de fim (opcional)
            is_active: Novo status ativo (opcional)
            
        Returns:
            Availability: Disponibilidade atualizada
        """
        availability = self.get_by_id(availability_id)
        
        if start_time_str is not None:
            try:
                availability.start_time = dtime.fromisoformat(start_time_str)
            except ValueError:
                raise ValidationError("Horário deve estar no formato HH:MM", "start_time")
                
        if end_time_str is not None:
            try:
                availability.end_time = dtime.fromisoformat(end_time_str)
            except ValueError:
                raise ValidationError("Horário deve estar no formato HH:MM", "end_time")
        
        # Validar intervalo após atualização
        if availability.start_time >= availability.end_time:
            raise ValidationError("Horário de início deve ser anterior ao horário de fim", "start_time")
        
        if is_active is not None:
            if is_active:
                availability.activate()
            else:
                availability.deactivate()
                
        self.availability_repository.update(availability)
        return availability

    def delete_availability(self, availability_id: int) -> None:
        """
        Remove uma disponibilidade do sistema.
        
        Args:
            availability_id: ID da disponibilidade
            
        Raises:
            NotFoundError: Se a disponibilidade não for encontrada
        """
        self.get_by_id(availability_id)
        self.availability_repository.delete(availability_id)

    def deactivate(self, availability_id: int) -> Availability:
        """Desativa uma disponibilidade."""
        availability = self.get_by_id(availability_id)
        availability.deactivate()
        self.availability_repository.update(availability)
        return availability

    def activate(self, availability_id: int) -> Availability:
        """Ativa uma disponibilidade."""
        availability = self.get_by_id(availability_id)
        availability.activate()
        self.availability_repository.update(availability)
        return availability
