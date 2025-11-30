"""
Controller de psicólogos.
Define as rotas HTTP para operações CRUD de psicólogos.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.psychologist_service import PsychologistService
from synapse.api.dto import PsychologistCreateDTO, PsychologistUpdateDTO
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError

bp = Blueprint('psychologists', __name__, url_prefix='/api/psychologists')


def create_psychologist_routes(psychologist_service: PsychologistService):
    """
    Registra as rotas de psicólogos no blueprint.
    
    Args:
        psychologist_service: Instância do serviço de psicólogos
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_psychologists():
        """
        Lista todos os psicólogos.
        
        Query Params:
            active_only: Se 'true', retorna apenas psicólogos ativos
            
        Returns:
            JSON com lista de psicólogos
        """
        active_only = request.args.get('active_only', 'false').lower() == 'true'
        psychologists = psychologist_service.get_all(active_only=active_only)
        return ApiResponse.list_response([p.to_dict() for p in psychologists])

    @bp.route('/<int:psychologist_id>', methods=['GET'])
    def get_psychologist(psychologist_id: int):
        """
        Busca um psicólogo pelo ID.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Returns:
            JSON com dados do psicólogo ou erro 404
        """
        try:
            psychologist = psychologist_service.get_by_id(psychologist_id)
            return ApiResponse.success(psychologist.to_dict())
        except NotFoundError:
            return ApiResponse.not_found("Psicólogo", psychologist_id)

    @bp.route('', methods=['POST'])
    def create_psychologist():
        """
        Cria um novo psicólogo.
        
        Body:
            user_id: ID do usuário associado
            name: Nome do psicólogo
            crp: Número do CRP
            specialty: Especialidade
            hourly_rate: Valor hora
            themes: Lista de temas (opcional)
            bio: Biografia (opcional)
            
        Returns:
            JSON com dados do psicólogo criado ou erro de validação
        """
        data = request.get_json()
        
        try:
            dto = PsychologistCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            psychologist = psychologist_service.create_psychologist(
                user_id=dto.user_id,
                name=dto.name,
                crp=dto.crp,
                specialty=dto.specialty,
                hourly_rate=dto.hourly_rate,
                themes=dto.themes,
                bio=dto.bio
            )
            return ApiResponse.created(psychologist.to_dict(), "Psicólogo criado com sucesso")
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:psychologist_id>', methods=['PUT'])
    def update_psychologist(psychologist_id: int):
        """
        Atualiza os dados de um psicólogo.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Body:
            name: Novo nome (opcional)
            specialty: Nova especialidade (opcional)
            themes: Novos temas (opcional)
            bio: Nova biografia (opcional)
            hourly_rate: Novo valor hora (opcional)
            is_active: Novo status ativo (opcional)
            
        Returns:
            JSON com dados do psicólogo atualizado ou erro
        """
        data = request.get_json()
        
        try:
            dto = PsychologistUpdateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            psychologist = psychologist_service.update_psychologist(
                psychologist_id=psychologist_id,
                name=dto.name,
                specialty=dto.specialty,
                themes=dto.themes,
                bio=dto.bio,
                hourly_rate=dto.hourly_rate,
                is_active=dto.is_active
            )
            return ApiResponse.success(psychologist.to_dict(), "Psicólogo atualizado com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Psicólogo", psychologist_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:psychologist_id>', methods=['DELETE'])
    def delete_psychologist(psychologist_id: int):
        """
        Remove um psicólogo do sistema.
        
        Args:
            psychologist_id: ID do psicólogo
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            psychologist_service.delete_psychologist(psychologist_id)
            return ApiResponse.no_content()
        except NotFoundError:
            return ApiResponse.not_found("Psicólogo", psychologist_id)

    @bp.route('/<int:psychologist_id>/activate', methods=['PATCH'])
    def activate_psychologist(psychologist_id: int):
        """Ativa um psicólogo."""
        try:
            psychologist = psychologist_service.activate(psychologist_id)
            return ApiResponse.success(psychologist.to_dict(), "Psicólogo ativado com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Psicólogo", psychologist_id)

    @bp.route('/<int:psychologist_id>/deactivate', methods=['PATCH'])
    def deactivate_psychologist(psychologist_id: int):
        """Desativa um psicólogo."""
        try:
            psychologist = psychologist_service.deactivate(psychologist_id)
            return ApiResponse.success(psychologist.to_dict(), "Psicólogo desativado com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Psicólogo", psychologist_id)

    return bp
