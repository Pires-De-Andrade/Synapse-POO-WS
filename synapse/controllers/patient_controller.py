"""
Controller de pacientes.
Define as rotas HTTP para operações CRUD de pacientes.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.patient_service import PatientService
from synapse.api.dto import PatientCreateDTO, PatientUpdateDTO
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError

bp = Blueprint('patients', __name__, url_prefix='/api/patients')


def create_patient_routes(patient_service: PatientService):
    """
    Registra as rotas de pacientes no blueprint.
    
    Args:
        patient_service: Instância do serviço de pacientes
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_patients():
        """
        Lista todos os pacientes.
        
        Returns:
            JSON com lista de pacientes
        """
        patients = patient_service.get_all()
        return ApiResponse.list_response([p.to_dict() for p in patients])

    @bp.route('/<int:patient_id>', methods=['GET'])
    def get_patient(patient_id: int):
        """
        Busca um paciente pelo ID.
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            JSON com dados do paciente ou erro 404
        """
        try:
            patient = patient_service.get_by_id(patient_id)
            return ApiResponse.success(patient.to_dict())
        except NotFoundError as e:
            return ApiResponse.not_found("Paciente", patient_id)

    @bp.route('', methods=['POST'])
    def create_patient():
        """
        Cria um novo paciente.
        
        Body:
            name: Nome do paciente
            email: Email do paciente
            phone: Telefone do paciente
            cpf: CPF do paciente (opcional)
            
        Returns:
            JSON com dados do paciente criado ou erro de validação
        """
        data = request.get_json()
        
        # Validar DTO
        try:
            dto = PatientCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        # Criar paciente via service
        try:
            patient = patient_service.create_patient(
                name=dto.name,
                email=dto.email,
                phone=dto.phone,
                cpf=dto.cpf
            )
            return ApiResponse.created(patient.to_dict(), "Paciente criado com sucesso")
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:patient_id>', methods=['PUT'])
    def update_patient(patient_id: int):
        """
        Atualiza os dados de um paciente.
        
        Args:
            patient_id: ID do paciente
            
        Body:
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            cpf: Novo CPF (opcional)
            
        Returns:
            JSON com dados do paciente atualizado ou erro
        """
        data = request.get_json()
        
        try:
            dto = PatientUpdateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            patient = patient_service.update_patient(
                patient_id=patient_id,
                name=dto.name,
                email=dto.email,
                phone=dto.phone,
                cpf=dto.cpf
            )
            return ApiResponse.success(patient.to_dict(), "Paciente atualizado com sucesso")
        except NotFoundError as e:
            return ApiResponse.not_found("Paciente", patient_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)

    @bp.route('/<int:patient_id>', methods=['DELETE'])
    def delete_patient(patient_id: int):
        """
        Remove um paciente do sistema.
        
        Args:
            patient_id: ID do paciente
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            patient_service.delete_patient(patient_id)
            return ApiResponse.no_content()
        except NotFoundError as e:
            return ApiResponse.not_found("Paciente", patient_id)

    return bp
