"""
Controller de clínicas.
Define as rotas HTTP para operações CRUD de clínicas.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.clinic_service import ClinicService
from synapse.api.dto import ClinicCreateDTO, ClinicUpdateDTO
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError

bp = Blueprint('clinics', __name__, url_prefix='/api/clinics')


def create_clinic_routes(clinic_service: ClinicService):
    """
    Registra as rotas de clínicas no blueprint.
    
    Args:
        clinic_service: Instância do serviço de clínicas
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_clinics():
        """
        Lista todas as clínicas.
        
        Returns:
            JSON com lista de clínicas
        """
        clinics = clinic_service.get_all()
        return ApiResponse.list_response([c.to_dict() for c in clinics])

    @bp.route('/<int:clinic_id>', methods=['GET'])
    def get_clinic(clinic_id: int):
        """
        Busca uma clínica pelo ID.
        
        Args:
            clinic_id: ID da clínica
            
        Returns:
            JSON com dados da clínica ou erro 404
        """
        try:
            clinic = clinic_service.get_by_id(clinic_id)
            return ApiResponse.success(clinic.to_dict())
        except NotFoundError:
            return ApiResponse.not_found("Clínica", clinic_id)

    @bp.route('', methods=['POST'])
    def create_clinic():
        """
        Cria uma nova clínica.
        
        Body:
            user_id: ID do usuário associado
            name: Nome da clínica
            address: Endereço
            phone: Telefone
            email: Email
            
        Returns:
            JSON com dados da clínica criada ou erro de validação
        """
        data = request.get_json()
        
        try:
            dto = ClinicCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            clinic = clinic_service.create_clinic(
                user_id=dto.user_id,
                name=dto.name,
                address=dto.address,
                phone=dto.phone,
                email=dto.email
            )
            return ApiResponse.created(clinic.to_dict(), "Clínica criada com sucesso")
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:clinic_id>', methods=['PUT'])
    def update_clinic(clinic_id: int):
        """
        Atualiza os dados de uma clínica.
        
        Args:
            clinic_id: ID da clínica
            
        Body:
            name: Novo nome (opcional)
            address: Novo endereço (opcional)
            phone: Novo telefone (opcional)
            email: Novo email (opcional)
            
        Returns:
            JSON com dados da clínica atualizada ou erro
        """
        data = request.get_json()
        
        try:
            dto = ClinicUpdateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            clinic = clinic_service.update_clinic(
                clinic_id=clinic_id,
                name=dto.name,
                address=dto.address,
                phone=dto.phone,
                email=dto.email
            )
            return ApiResponse.success(clinic.to_dict(), "Clínica atualizada com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Clínica", clinic_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:clinic_id>', methods=['DELETE'])
    def delete_clinic(clinic_id: int):
        """
        Remove uma clínica do sistema.
        
        Args:
            clinic_id: ID da clínica
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            clinic_service.delete_clinic(clinic_id)
            return ApiResponse.no_content()
        except NotFoundError:
            return ApiResponse.not_found("Clínica", clinic_id)

    return bp
