"""
Controller de consultas/agendamentos.
Define as rotas HTTP para operações de agendamento.
"""

from flask import Blueprint, request
from pydantic import ValidationError as PydanticValidationError
from synapse.services.appointment_service import AppointmentService
from synapse.api.dto import (
    AppointmentCreateDTO, 
    AppointmentCancelDTO,
    AvailableSlotsRequestDTO
)
from synapse.api.response import ApiResponse
from synapse.api.exceptions import NotFoundError, ValidationError, ConflictError, BusinessRuleError

bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')


def create_appointment_routes(appointment_service: AppointmentService):
    """
    Registra as rotas de consultas no blueprint.
    
    Args:
        appointment_service: Instância do serviço de consultas
        
    Returns:
        Blueprint: Blueprint configurado com as rotas
    """
    
    @bp.route('', methods=['GET'])
    def get_all_appointments():
        """
        Lista todas as consultas.
        
        Query Params:
            patient_id: Filtrar por paciente (opcional)
            psychologist_id: Filtrar por psicólogo (opcional)
            
        Returns:
            JSON com lista de consultas
        """
        patient_id = request.args.get('patient_id', type=int)
        psychologist_id = request.args.get('psychologist_id', type=int)
        
        if patient_id:
            appointments = appointment_service.get_by_patient(patient_id)
        elif psychologist_id:
            appointments = appointment_service.get_by_psychologist(psychologist_id)
        else:
            appointments = appointment_service.get_all()
            
        return ApiResponse.list_response([a.to_dict() for a in appointments])

    @bp.route('/<int:appointment_id>', methods=['GET'])
    def get_appointment(appointment_id: int):
        """
        Busca uma consulta pelo ID.
        
        Args:
            appointment_id: ID da consulta
            
        Returns:
            JSON com dados da consulta ou erro 404
        """
        try:
            appointment = appointment_service.get_by_id(appointment_id)
            return ApiResponse.success(appointment.to_dict())
        except NotFoundError:
            return ApiResponse.not_found("Consulta", appointment_id)

    @bp.route('', methods=['POST'])
    def create_appointment():
        """
        Agenda uma nova consulta.
        
        Body:
            patient_id: ID do paciente
            psychologist_id: ID do psicólogo
            date: Data da consulta (yyyy-mm-dd)
            time: Horário da consulta (HH:MM)
            duration: Duração em minutos (default: 60)
            notes: Observações (opcional)
            
        Returns:
            JSON com dados da consulta agendada ou erro
        """
        data = request.get_json()
        
        try:
            dto = AppointmentCreateDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            appointment = appointment_service.schedule_appointment(
                patient_id=dto.patient_id,
                psychologist_id=dto.psychologist_id,
                date_str=dto.date,
                time_str=dto.time,
                duration=dto.duration,
                notes=dto.notes
            )
            return ApiResponse.created(appointment.to_dict(), "Consulta agendada com sucesso")
        except NotFoundError as e:
            return ApiResponse.not_found(e.resource, e.resource_id)
        except ValidationError as e:
            return ApiResponse.validation_error(e.message, e.field)
        except ConflictError as e:
            return ApiResponse.conflict(e.message)
        except BusinessRuleError as e:
            return ApiResponse.business_error(e.message)

    @bp.route('/<int:appointment_id>', methods=['DELETE'])
    def delete_appointment(appointment_id: int):
        """
        Remove uma consulta do sistema.
        
        Args:
            appointment_id: ID da consulta
            
        Returns:
            204 No Content ou erro 404
        """
        try:
            appointment_service.delete_appointment(appointment_id)
            return ApiResponse.no_content()
        except NotFoundError:
            return ApiResponse.not_found("Consulta", appointment_id)

    @bp.route('/<int:appointment_id>/cancel', methods=['PATCH'])
    def cancel_appointment(appointment_id: int):
        """
        Cancela uma consulta.
        
        Args:
            appointment_id: ID da consulta
            
        Body:
            cancellation_reason: Motivo do cancelamento (opcional)
            
        Returns:
            JSON com dados da consulta cancelada ou erro
        """
        data = request.get_json() or {}
        
        try:
            dto = AppointmentCancelDTO(**data)
        except PydanticValidationError:
            return ApiResponse.validation_error("Dados inválidos")
        
        try:
            appointment = appointment_service.cancel_appointment(
                appointment_id, 
                dto.cancellation_reason
            )
            return ApiResponse.success(appointment.to_dict(), "Consulta cancelada com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Consulta", appointment_id)
        except BusinessRuleError as e:
            return ApiResponse.business_error(e.message)

    @bp.route('/<int:appointment_id>/complete', methods=['PATCH'])
    def complete_appointment(appointment_id: int):
        """
        Marca uma consulta como concluída.
        
        Args:
            appointment_id: ID da consulta
            
        Returns:
            JSON com dados da consulta concluída ou erro
        """
        try:
            appointment = appointment_service.complete_appointment(appointment_id)
            return ApiResponse.success(appointment.to_dict(), "Consulta concluída com sucesso")
        except NotFoundError:
            return ApiResponse.not_found("Consulta", appointment_id)
        except BusinessRuleError as e:
            return ApiResponse.business_error(e.message)

    @bp.route('/available-slots', methods=['POST'])
    def get_available_slots():
        """
        Lista horários disponíveis para agendamento.
        
        Body:
            psychologist_id: ID do psicólogo
            date: Data desejada (yyyy-mm-dd)
            duration: Duração da consulta em minutos (default: 60)
            
        Returns:
            JSON com lista de horários disponíveis
        """
        data = request.get_json()
        
        try:
            dto = AvailableSlotsRequestDTO(**data)
        except PydanticValidationError as e:
            errors = e.errors()
            if errors:
                return ApiResponse.validation_error(errors[0]['msg'], errors[0]['loc'][0])
            return ApiResponse.validation_error("Dados inválidos")
        
        slots = appointment_service.get_available_slots(
            dto.psychologist_id, 
            dto.date,
            dto.duration
        )
        return ApiResponse.success({
            "psychologist_id": dto.psychologist_id,
            "date": dto.date,
            "available_times": slots,
            "count": len(slots)
        })

    return bp
