"""
Serviço de gerenciamento de leads.
Contém a lógica de negócio para operações CRUD de leads.
"""

from synapse.repositories.implementations.inmemory_lead_repository import InMemoryLeadRepository
from synapse.business_model.lead import Lead
from synapse.api.exceptions import NotFoundError, ValidationError, BusinessRuleError
from datetime import datetime


class LeadService:
    """
    Serviço responsável pela lógica de negócio relacionada a leads.
    
    Attributes:
        lead_repository: Repositório para persistência de leads
    """
    
    def __init__(self, lead_repository: InMemoryLeadRepository):
        self.lead_repository = lead_repository

    def get_all(self):
        """Retorna todos os leads cadastrados."""
        return self.lead_repository.all()

    def get_by_id(self, lead_id: int):
        """
        Busca um lead pelo ID.
        
        Args:
            lead_id: ID do lead
            
        Returns:
            Lead: Lead encontrado
            
        Raises:
            NotFoundError: Se o lead não for encontrado
        """
        lead = self.lead_repository.get(lead_id)
        if not lead:
            raise NotFoundError("Lead", lead_id)
        return lead

    def create_lead(self, name: str, email: str, phone: str, 
                    source: str, notes: str = None) -> Lead:
        """
        Cria um novo lead.
        
        Args:
            name: Nome do lead
            email: Email do lead
            phone: Telefone do lead
            source: Origem do lead
            notes: Observações (opcional)
            
        Returns:
            Lead: Lead criado
        """
        lead = Lead(name=name, email=email, phone=phone, source=source, notes=notes)
        self.lead_repository.add(lead)
        return lead

    def update_lead(self, lead_id: int, name: str = None, email: str = None,
                    phone: str = None, notes: str = None) -> Lead:
        """
        Atualiza os dados de um lead.
        
        Args:
            lead_id: ID do lead
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            notes: Novas observações (opcional)
            
        Returns:
            Lead: Lead atualizado
        """
        lead = self.get_by_id(lead_id)
        
        if name is not None:
            lead.name = name
        if email is not None:
            lead.email = email
        if phone is not None:
            lead.phone = phone
        if notes is not None:
            lead.notes = notes
            
        self.lead_repository.update(lead)
        return lead

    def delete_lead(self, lead_id: int) -> None:
        """
        Remove um lead do sistema.
        
        Args:
            lead_id: ID do lead
            
        Raises:
            NotFoundError: Se o lead não for encontrado
        """
        self.get_by_id(lead_id)
        self.lead_repository.delete(lead_id)

    def mark_contacted(self, lead_id: int, notes: str = None) -> Lead:
        """
        Marca um lead como contatado.
        
        Args:
            lead_id: ID do lead
            notes: Observações do contato
            
        Returns:
            Lead: Lead atualizado
        """
        lead = self.get_by_id(lead_id)
        lead.mark_as_contacted(notes)
        self.lead_repository.update(lead)
        return lead

    def mark_lost(self, lead_id: int, reason: str = None) -> Lead:
        """
        Marca um lead como perdido.
        
        Args:
            lead_id: ID do lead
            reason: Motivo da perda
            
        Returns:
            Lead: Lead atualizado
        """
        lead = self.get_by_id(lead_id)
        lead.mark_as_lost(reason)
        self.lead_repository.update(lead)
        return lead

    def convert_to_patient(self, lead_id: int, patient_id: int) -> Lead:
        """
        Converte um lead em paciente.
        
        Args:
            lead_id: ID do lead
            patient_id: ID do paciente criado
            
        Returns:
            Lead: Lead atualizado
            
        Raises:
            BusinessRuleError: Se o lead já foi convertido
        """
        lead = self.get_by_id(lead_id)
        
        if lead.status == 'converted':
            raise BusinessRuleError("Lead já foi convertido anteriormente")
        
        lead.convert_to_patient(patient_id)
        self.lead_repository.update(lead)
        return lead
