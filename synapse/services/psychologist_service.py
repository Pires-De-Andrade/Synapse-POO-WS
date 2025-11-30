"""
Serviço de gerenciamento de psicólogos.
Contém a lógica de negócio para operações CRUD de psicólogos.
"""

from typing import List, Optional
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.business_model.psychologist import Psychologist
from synapse.api.exceptions import NotFoundError, ValidationError


class PsychologistService:
    """
    Serviço responsável pela lógica de negócio relacionada a psicólogos.
    
    Attributes:
        psychologist_repository: Repositório para persistência de psicólogos
    """
    
    def __init__(self, psychologist_repository: InMemoryPsychologistRepository):
        self.psychologist_repository = psychologist_repository

    def get_all(self, active_only: bool = False):
        """
        Retorna todos os psicólogos cadastrados.
        
        Args:
            active_only: Se True, retorna apenas psicólogos ativos
        """
        psychologists = self.psychologist_repository.all()
        if active_only:
            return [p for p in psychologists if p.is_active]
        return psychologists

    def get_by_id(self, psychologist_id: int):
        """
        Busca um psicólogo pelo ID.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Returns:
            Psychologist: Psicólogo encontrado
            
        Raises:
            NotFoundError: Se o psicólogo não for encontrado
        """
        psychologist = self.psychologist_repository.get(psychologist_id)
        if not psychologist:
            raise NotFoundError("Psicólogo", psychologist_id)
        return psychologist

    def create_psychologist(self, user_id: int, name: str, crp: str, specialty: str,
                            hourly_rate: float, themes: List[str] = None, 
                            bio: str = "") -> Psychologist:
        """
        Cria um novo psicólogo.
        
        Args:
            user_id: ID do usuário associado
            name: Nome do psicólogo
            crp: Número do CRP
            specialty: Especialidade
            hourly_rate: Valor hora
            themes: Lista de temas (opcional)
            bio: Biografia (opcional)
            
        Returns:
            Psychologist: Psicólogo criado
            
        Raises:
            ValidationError: Se os dados forem inválidos
        """
        psychologist = Psychologist(
            user_id=user_id,
            name=name,
            crp=crp,
            specialty=specialty,
            hourly_rate=hourly_rate,
            themes=themes,
            bio=bio
        )
        
        if not psychologist.validate_crp():
            raise ValidationError("CRP deve estar no formato XX/XXXXX", "crp")
        if hourly_rate <= 0:
            raise ValidationError("Valor hora deve ser positivo", "hourly_rate")
            
        self.psychologist_repository.add(psychologist)
        return psychologist

    def update_psychologist(self, psychologist_id: int, name: str = None,
                            specialty: str = None, themes: List[str] = None,
                            bio: str = None, hourly_rate: float = None,
                            is_active: bool = None) -> Psychologist:
        """
        Atualiza os dados de um psicólogo.
        
        Args:
            psychologist_id: ID do psicólogo
            name: Novo nome (opcional)
            specialty: Nova especialidade (opcional)
            themes: Novos temas (opcional)
            bio: Nova biografia (opcional)
            hourly_rate: Novo valor hora (opcional)
            is_active: Novo status ativo (opcional)
            
        Returns:
            Psychologist: Psicólogo atualizado
            
        Raises:
            NotFoundError: Se o psicólogo não for encontrado
            ValidationError: Se os dados forem inválidos
        """
        psychologist = self.get_by_id(psychologist_id)
        
        if name is not None:
            psychologist.name = name
        if specialty is not None:
            psychologist.specialty = specialty
        if themes is not None:
            psychologist.themes = themes
        if bio is not None:
            psychologist.bio = bio
        if hourly_rate is not None:
            if hourly_rate <= 0:
                raise ValidationError("Valor hora deve ser positivo", "hourly_rate")
            psychologist.hourly_rate = hourly_rate
        if is_active is not None:
            if is_active:
                psychologist.activate()
            else:
                psychologist.deactivate()
                
        self.psychologist_repository.update(psychologist)
        return psychologist

    def delete_psychologist(self, psychologist_id: int) -> None:
        """
        Remove um psicólogo do sistema.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Raises:
            NotFoundError: Se o psicólogo não for encontrado
        """
        self.get_by_id(psychologist_id)
        self.psychologist_repository.delete(psychologist_id)

    def activate(self, psychologist_id: int) -> Psychologist:
        """Ativa um psicólogo."""
        psychologist = self.get_by_id(psychologist_id)
        psychologist.activate()
        self.psychologist_repository.update(psychologist)
        return psychologist

    def deactivate(self, psychologist_id: int) -> Psychologist:
        """Desativa um psicólogo."""
        psychologist = self.get_by_id(psychologist_id)
        psychologist.deactivate()
        self.psychologist_repository.update(psychologist)
        return psychologist
