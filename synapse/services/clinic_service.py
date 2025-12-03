"""
Serviço de gerenciamento de clínicas.
Contém a lógica de negócio para operações CRUD de clínicas.
"""

from synapse.repositories.implementations.inmemory_clinic_repository import InMemoryClinicRepository
from synapse.business_model.clinic import Clinic
from synapse.api.exceptions import NotFoundError, ValidationError


class ClinicService:
    """
    Serviço responsável pela lógica de negócio relacionada a clínicas.
    
    Attributes:
        clinic_repository: Repositório para persistência de clínicas
    """
    
    def __init__(self, clinic_repository: InMemoryClinicRepository):
        self.clinic_repository = clinic_repository

    def get_all(self):
        """Retorna todas as clínicas cadastradas."""
        return self.clinic_repository.all()

    def get_by_id(self, clinic_id: int):
        """
        Busca uma clínica pelo ID.
        
        Args:
            clinic_id: ID da clínica
            
        Returns:
            Clinic: Clínica encontrada
            
        Raises:
            NotFoundError: Se a clínica não for encontrada
        """
        clinic = self.clinic_repository.get(clinic_id)
        if not clinic:
            raise NotFoundError("Clínica", clinic_id)
        return clinic

    def create_clinic(self, user_id: int, name: str, address: str, 
                      phone: str, email: str) -> Clinic:
        """
        Cria uma nova clínica.
        
        Args:
            user_id: ID do usuário associado
            name: Nome da clínica
            address: Endereço
            phone: Telefone
            email: Email
            
        Returns:
            Clinic: Clínica criada
            
        Raises:
            ValidationError: Se os dados forem inválidos
        """
        if not name or not name.strip():
            raise ValidationError("Nome não pode ser vazio", "name")
        if not email or "@" not in email:
            raise ValidationError("Email inválido", "email")
            
        clinic = Clinic(
            user_id=user_id,
            name=name.strip(),
            address=address,
            phone=phone,
            email=email
        )
        self.clinic_repository.add(clinic)
        return clinic

    def update_clinic(self, clinic_id: int, name: str = None, address: str = None,
                      phone: str = None, email: str = None) -> Clinic:
        """
        Atualiza os dados de uma clínica.
        
        Args:
            clinic_id: ID da clínica
            name: Novo nome (opcional)
            address: Novo endereço (opcional)
            phone: Novo telefone (opcional)
            email: Novo email (opcional)
            
        Returns:
            Clinic: Clínica atualizada
            
        Raises:
            NotFoundError: Se a clínica não for encontrada
            ValidationError: Se os dados forem inválidos
        """
        clinic = self.get_by_id(clinic_id)
        
        if name is not None:
            if not name.strip():
                raise ValidationError("Nome não pode ser vazio", "name")
            clinic.name = name.strip()
        if address is not None:
            clinic.address = address
        if phone is not None:
            clinic.phone = phone
        if email is not None:
            if "@" not in email:
                raise ValidationError("Email inválido", "email")
            clinic.email = email
            
        self.clinic_repository.update(clinic)
        return clinic

    def delete_clinic(self, clinic_id: int) -> None:
        """
        Remove uma clínica do sistema.
        
        Args:
            clinic_id: ID da clínica
            
        Raises:
            NotFoundError: Se a clínica não for encontrada
        """
        self.get_by_id(clinic_id)
        self.clinic_repository.delete(clinic_id)
