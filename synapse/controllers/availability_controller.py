"""
Controller de disponibilidades.
Define as rotas HTTP para operações CRUD de disponibilidades de psicólogos.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.availability_service import AvailabilityService
from synapse.api.dto import AvailabilityCreateDTO, AvailabilityUpdateDTO
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError, ConflictError

bp = Blueprint('availabilities', __name__, url_prefix='/api/availabilities')


def create_availability_routes(availability_service: AvailabilityService):
    """
    Registra as rotas de disponibilidades no blueprint.
    
    Args:
        availability_service: Instância do serviço de disponibilidades
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_availabilities():
        """
        Lista todas as disponibilidades.
        
        Query Params:
            psychologist_id: Filtrar por psicólogo (opcional)
            
        Returns:
            JSON com lista de disponibilidades
        """
        psychologist_id = request.args.get('psychologist_id', type=int)
        
        if psychologist_id:
            availabilities = availability_service.get_by_psychologist(psychologist_id)
        else:
            availabilities = availability_service.get_all()
            
        return ApiResponse.list_response([a.to_dict() for a in availabilities])

    @bp.route('/<int:availability_id>', methods=['GET'])
    def get_availability(availability_id: int):
        """
        Busca uma disponibilidade pelo ID.
        
        Args:
            availability_id: ID da disponibilidade
            
        Returns:
            JSON com dados da disponibilidade ou erro 404
        """
        try:
            availability = availability_service.get_by_id(availability_id)
            return ApiResponse.success(availability.to_dict())
        except NotFoundError:
            return ApiResponse.not_found("Disponibilidade", availability_id)

    @bp.route('/psychologist/<int:psychologist_id>', methods=['GET'])
    def get_psychologist_availabilities(psychologist_id: int):
        """
        Lista todas as disponibilidades de um psicólogo.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Returns:
            JSON com lista de disponibilidades do psicólogo
        """
        availabilities = availability_service.get_by_psychologist(psychologist_id)
        return ApiResponse.list_response([a.to_dict() for a in availabilities])

    @bp.route('', methods=['POST'])
    def create_availability():
        """
        Cria uma nova disponibilidade para um psicólogo.
        
        Body:
            psychologist_id: ID do psicólogo
            day_of_week: Dia da semana (0=Segunda, 6=Domingo)
            start_time: Horário de início (HH:MM)
            end_time: Horário de fim (HH:MM)
            
        Returns:
            JSON com dados da disponibilidade criada ou erro
        """
        data = request.get_json()
        
        try:
            dto = AvailabilityCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            availability = availability_service.create_availability(
                psychologist_id=dto.psychologist_id,
                day_of_week=dto.day_of_week,
                start_time_str=dto.start_time,
                end_time_str=dto.end_time
            )
            return ApiResponse.created(availability.to_dict(), "Disponibilidade criada com sucesso")
        except NotFoundError as e:
            return ApiResponse.not_found(e.resource, e.resource_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)
        except ConflictError as e:
            return ApiResponse.conflict(e.message)

    @bp.route('/<int:availability_id>', methods=['PUT'])
    def update_availability(availability_id: int):
        """
        Atualiza uma disponibilidade.
        
        Args:
            availability_id: ID da disponibilidade
            
        Body:
            start_time: Novo horário de início (opcional)
            end_time: Novo horário de fim (opcional)
            is_active: Novo status ativo (opcional)
            
        Returns:
            JSON com dados da disponibilidade atualizada ou erro
        """
        data = request.get_json()
        
        try:
            dto = AvailabilityUpdateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            availability = availability_service.update_availability(
                availability_id=availability_id,
                start_time_str=dto.start_time,
                end_time_str=dto.end_time,
                is_active=dto.is_active
            )
            return ApiResponse.success(availability.to_dict(), "Disponibilidade atualizada com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Disponibilidade", availability_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:availability_id>', methods=['DELETE'])
    def delete_availability(availability_id: int):
        """
        Remove uma disponibilidade do sistema.
        
        Args:
            availability_id: ID da disponibilidade
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            availability_service.delete_availability(availability_id)
            return ApiResponse.no_content()
        except NotFoundError:
            return ApiResponse.not_found("Disponibilidade", availability_id)

    @bp.route('/<int:availability_id>/activate', methods=['PATCH'])
    def activate_availability(availability_id: int):
        """Ativa uma disponibilidade."""
        try:
            availability = availability_service.activate(availability_id)
            return ApiResponse.success(availability.to_dict(), "Disponibilidade ativada com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Disponibilidade", availability_id)

    @bp.route('/<int:availability_id>/deactivate', methods=['PATCH'])
    def deactivate_availability(availability_id: int):
        """Desativa uma disponibilidade."""
        try:
            availability = availability_service.deactivate(availability_id)
            return ApiResponse.success(availability.to_dict(), "Disponibilidade desativada com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Disponibilidade", availability_id)

    return bp
