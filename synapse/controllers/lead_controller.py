"""
Controller de leads.
Define as rotas HTTP para operações CRUD de leads.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.lead_service import LeadService
from synapse.api.dto import (
    LeadCreateDTO, 
    LeadUpdateDTO,
    LeadContactedDTO,
    LeadLostDTO,
    LeadConvertDTO
)
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError, BusinessRuleError

bp = Blueprint('leads', __name__, url_prefix='/api/leads')


def create_lead_routes(lead_service: LeadService):
    """
    Registra as rotas de leads no blueprint.
    
    Args:
        lead_service: Instância do serviço de leads
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_leads():
        """
        Lista todos os leads.
        
        Returns:
            JSON com lista de leads
        """
        leads = lead_service.get_all()
        return ApiResponse.list_response([l.to_dict() for l in leads])

    @bp.route('/<int:lead_id>', methods=['GET'])
    def get_lead(lead_id: int):
        """
        Busca um lead pelo ID.
        
        Args:
            lead_id: ID do lead
            
        Returns:
            JSON com dados do lead ou erro 404
        """
        try:
            lead = lead_service.get_by_id(lead_id)
            return ApiResponse.success(lead.to_dict())
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)

    @bp.route('', methods=['POST'])
    def create_lead():
        """
        Cria um novo lead.
        
        Body:
            name: Nome do lead
            email: Email do lead
            phone: Telefone do lead
            source: Origem do lead
            notes: Observações (opcional)
            
        Returns:
            JSON com dados do lead criado ou erro de validação
        """
        data = request.get_json()
        
        try:
            dto = LeadCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        lead = lead_service.create_lead(
            name=dto.name,
            email=dto.email,
            phone=dto.phone,
            source=dto.source,
            notes=dto.notes
        )
        return ApiResponse.created(lead.to_dict(), "Lead criado com sucesso")

    @bp.route('/<int:lead_id>', methods=['PUT'])
    def update_lead(lead_id: int):
        """
        Atualiza os dados de um lead.
        
        Args:
            lead_id: ID do lead
            
        Body:
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            notes: Novas observações (opcional)
            
        Returns:
            JSON com dados do lead atualizado ou erro
        """
        data = request.get_json()
        
        try:
            dto = LeadUpdateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            lead = lead_service.update_lead(
                lead_id=lead_id,
                name=dto.name,
                email=dto.email,
                phone=dto.phone,
                notes=dto.notes
            )
            return ApiResponse.success(lead.to_dict(), "Lead atualizado com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)

    @bp.route('/<int:lead_id>', methods=['DELETE'])
    def delete_lead(lead_id: int):
        """
        Remove um lead do sistema.
        
        Args:
            lead_id: ID do lead
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            lead_service.delete_lead(lead_id)
            return ApiResponse.no_content()
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)

    @bp.route('/<int:lead_id>/contacted', methods=['PATCH'])
    def contacted_lead(lead_id: int):
        """
        Marca um lead como contatado.
        
        Args:
            lead_id: ID do lead
            
        Body:
            notes: Observações do contato (opcional)
            
        Returns:
            JSON com dados do lead atualizado ou erro
        """
        data = request.get_json() or {}
        
        try:
            dto = LeadContactedDTO(**data)
        except PydanticValidationError:
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            lead = lead_service.mark_contacted(lead_id, dto.notes)
            return ApiResponse.success(lead.to_dict(), "Lead marcado como contatado")
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)

    @bp.route('/<int:lead_id>/lost', methods=['PATCH'])
    def lost_lead(lead_id: int):
        """
        Marca um lead como perdido.
        
        Args:
            lead_id: ID do lead
            
        Body:
            reason: Motivo da perda (opcional)
            
        Returns:
            JSON com dados do lead atualizado ou erro
        """
        data = request.get_json() or {}
        
        try:
            dto = LeadLostDTO(**data)
        except PydanticValidationError:
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            lead = lead_service.mark_lost(lead_id, dto.reason)
            return ApiResponse.success(lead.to_dict(), "Lead marcado como perdido")
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)

    @bp.route('/<int:lead_id>/convert', methods=['PATCH'])
    def convert_lead(lead_id: int):
        """
        Converte um lead em paciente.
        
        Args:
            lead_id: ID do lead
            
        Body:
            patient_id: ID do paciente criado
            
        Returns:
            JSON com dados do lead atualizado ou erro
        """
        data = request.get_json() or {}
        
        try:
            dto = LeadConvertDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            lead = lead_service.convert_to_patient(lead_id, dto.patient_id)
            return ApiResponse.success(lead.to_dict(), "Lead convertido em paciente com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Lead", lead_id)
        except BusinessRuleError as e:
            return ApiResponse.business_error(e.message)

    return bp
