"""
Serviço de gerenciamento de pacientes.
Contém a lógica de negócio para operações CRUD de pacientes.
"""

from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository
from synapse.business_model.patient import Patient
from synapse.api.exceptions import NotFoundError, ValidationError


class PatientService:
    """
    Serviço responsável pela lógica de negócio relacionada a pacientes.
    
    Attributes:
        patient_repository: Repositório para persistência de pacientes
    """
    
    def __init__(self, patient_repository: InMemoryPatientRepository):
        self.patient_repository = patient_repository

    def get_all(self):
        """Retorna todos os pacientes cadastrados."""
        return self.patient_repository.all()

    def get_by_id(self, patient_id: int):
        """
        Busca um paciente pelo ID.
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            Patient: Paciente encontrado
            
        Raises:
            NotFoundError: Se o paciente não for encontrado
        """
        patient = self.patient_repository.get(patient_id)
        if not patient:
            raise NotFoundError("Paciente", patient_id)
        return patient

    def create_patient(self, name: str, email: str, phone: str, cpf: str = None) -> Patient:
        """
        Cria um novo paciente.
        
        Args:
            name: Nome do paciente
            email: Email do paciente
            phone: Telefone do paciente
            cpf: CPF do paciente (opcional)
            
        Returns:
            Patient: Paciente criado
            
        Raises:
            ValidationError: Se os dados forem inválidos
        """
        patient = Patient(name=name, email=email, phone=phone, cpf=cpf)
        
        if not patient.validate_email():
            raise ValidationError("Email inválido", "email")
        if not patient.validate_phone():
            raise ValidationError("Telefone deve ter pelo menos 8 caracteres", "phone")
            
        self.patient_repository.add(patient)
        return patient

    def update_patient(self, patient_id: int, name: str = None, email: str = None, 
                       phone: str = None, cpf: str = None) -> Patient:
        """
        Atualiza os dados de um paciente.
        
        Args:
            patient_id: ID do paciente
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            cpf: Novo CPF (opcional)
            
        Returns:
            Patient: Paciente atualizado
            
        Raises:
            NotFoundError: Se o paciente não for encontrado
            ValidationError: Se os dados forem inválidos
        """
        patient = self.get_by_id(patient_id)
        
        if name is not None:
            patient.name = name
        if email is not None:
            patient.email = email
            if not patient.validate_email():
                raise ValidationError("Email inválido", "email")
        if phone is not None:
            patient.phone = phone
            if not patient.validate_phone():
                raise ValidationError("Telefone deve ter pelo menos 8 caracteres", "phone")
        if cpf is not None:
            patient.cpf = cpf
            
        self.patient_repository.update(patient)
        return patient

    def delete_patient(self, patient_id: int) -> None:
        """
        Remove um paciente do sistema.
        
        Args:
            patient_id: ID do paciente
            
        Raises:
            NotFoundError: Se o paciente não for encontrado
        """
        patient = self.get_by_id(patient_id)
        self.patient_repository.delete(patient_id)
