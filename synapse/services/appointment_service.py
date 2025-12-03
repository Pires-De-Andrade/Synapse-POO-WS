"""
Serviço de gerenciamento de consultas/agendamentos.
Contém a lógica de negócio para operações de agendamento.
"""

from synapse.repositories.implementations.inmemory_appointment_repository import InMemoryAppointmentRepository
from synapse.repositories.implementations.inmemory_patient_repository import InMemoryPatientRepository
from synapse.repositories.implementations.inmemory_psychologist_repository import InMemoryPsychologistRepository
from synapse.repositories.implementations.inmemory_availability_repository import InMemoryAvailabilityRepository
from synapse.business_model.appointment import Appointment
from synapse.api.exceptions import NotFoundError, ValidationError, ConflictError, BusinessRuleError
from datetime import datetime, date, time as dtime, timedelta


class AppointmentService:
    """
    Serviço responsável pela lógica de negócio relacionada a consultas.
    
    Attributes:
        appointment_repository: Repositório para persistência de consultas
        patient_repository: Repositório para validação de pacientes
        psychologist_repository: Repositório para validação de psicólogos
        availability_repository: Repositório para verificação de disponibilidade
    """
    
    def __init__(self, appointment_repository: InMemoryAppointmentRepository,
                 patient_repository: InMemoryPatientRepository,
                 psychologist_repository: InMemoryPsychologistRepository,
                 availability_repository: InMemoryAvailabilityRepository):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.psychologist_repository = psychologist_repository
        self.availability_repository = availability_repository

    def get_all(self):
        """Retorna todas as consultas cadastradas."""
        return self.appointment_repository.all()

    def get_by_id(self, appointment_id: int):
        """
        Busca uma consulta pelo ID.
        
        Args:
            appointment_id: ID da consulta
            
        Returns:
            Appointment: Consulta encontrada
            
        Raises:
            NotFoundError: Se a consulta não for encontrada
        """
        appointment = self.appointment_repository.get(appointment_id)
        if not appointment:
            raise NotFoundError("Consulta", appointment_id)
        return appointment

    def get_by_patient(self, patient_id: int):
        """Retorna todas as consultas de um paciente."""
        return [a for a in self.get_all() if a.patient_id == patient_id]

    def get_by_psychologist(self, psychologist_id: int):
        """Retorna todas as consultas de um psicólogo."""
        return [a for a in self.get_all() if a.psychologist_id == psychologist_id]

    def get_available_slots(self, psychologist_id: int, date_str: str, duration: int = 60):
        """
        Retorna lista de horários disponíveis para um psicólogo em uma data específica.
        
        Args:
            psychologist_id: ID do psicólogo
            date_str: Data no formato yyyy-mm-dd
            duration: Duração da consulta em minutos
            
        Returns:
            List[str]: Lista de horários disponíveis (HH:MM)
        """
        try:
            appt_date = date.fromisoformat(date_str)
        except:
            return []
        
        day_of_week = appt_date.weekday()
        availabilities = self.availability_repository.by_psychologist(psychologist_id)
        day_availabilities = [a for a in availabilities if a.day_of_week == day_of_week and a.is_active]
        
        if not day_availabilities:
            return []
        
        existing_appointments = self.appointment_repository.all()
        booked_times = set()
        for ap in existing_appointments:
            if (ap.psychologist_id == psychologist_id 
                and ap.date == appt_date 
                and ap.status != 'cancelled'):
                if isinstance(ap.time, str):
                    booked_time = dtime.fromisoformat(ap.time)
                else:
                    booked_time = ap.time
                booked_times.add(booked_time.strftime('%H:%M'))
        
        available_slots = []
        for ava in day_availabilities:
            current_time = ava.start_time
            while current_time < ava.end_time:
                slot_end = (datetime.combine(date.today(), current_time) + timedelta(minutes=duration)).time()
                current_time_str = current_time.strftime('%H:%M')
                
                if slot_end <= ava.end_time and current_time_str not in booked_times:
                    available_slots.append(current_time_str)
                
                current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=15)).time()
        
        return sorted(available_slots)

    def schedule_appointment(self, patient_id: int, psychologist_id: int, 
                            date_str: str, time_str: str, duration: int = 60, 
                            notes: str = None) -> Appointment:
        """
        Agenda uma nova consulta.
        
        Args:
            patient_id: ID do paciente
            psychologist_id: ID do psicólogo
            date_str: Data da consulta (yyyy-mm-dd)
            time_str: Horário da consulta (HH:MM)
            duration: Duração em minutos
            notes: Observações (opcional)
            
        Returns:
            Appointment: Consulta agendada
            
        Raises:
            NotFoundError: Se paciente ou psicólogo não forem encontrados
            ValidationError: Se data/hora forem inválidos
            BusinessRuleError: Se psicólogo estiver inativo ou sem disponibilidade
            ConflictError: Se já existir consulta no horário
        """
        # Validar existência
        patient = self.patient_repository.get(patient_id)
        if not patient:
            raise NotFoundError("Paciente", patient_id)
            
        psy = self.psychologist_repository.get(psychologist_id)
        if not psy:
            raise NotFoundError("Psicólogo", psychologist_id)
        if not psy.is_active:
            raise BusinessRuleError("Psicólogo está inativo")
        
        # Converter datas
        try:
            appt_date = date.fromisoformat(date_str)
            appt_time = dtime.fromisoformat(time_str)
        except Exception:
            raise ValidationError("Data ou hora em formato inválido")
        
        # Validar data futura
        if appt_date < date.today():
            raise ValidationError("Data da consulta deve ser futura", "date")
        
        # Checar disponibilidade
        avas = self.availability_repository.by_psychologist(psychologist_id)
        ava_day = [a for a in avas if a.day_of_week == appt_date.weekday() and a.is_active]
        if not ava_day:
            raise BusinessRuleError("Psicólogo não possui disponibilidade neste dia")
        
        slot_ok = any(a.start_time <= appt_time < a.end_time for a in ava_day)
        if not slot_ok:
            raise BusinessRuleError("Horário fora da faixa de disponibilidade")
        
        # Checar conflitos
        existing = self.appointment_repository.all()
        for ap in existing:
            if (ap.psychologist_id == psychologist_id and 
                ap.date == appt_date and 
                ap.time == appt_time and 
                ap.status != 'cancelled'):
                raise ConflictError("Já existe consulta agendada neste horário")
        
        # Criar e salvar
        appt = Appointment(patient_id, psychologist_id, appt_date, appt_time, duration, notes)
        self.appointment_repository.add(appt)
        return appt

    def cancel_appointment(self, appointment_id: int, reason: str = None) -> Appointment:
        """
        Cancela uma consulta.
        
        Args:
            appointment_id: ID da consulta
            reason: Motivo do cancelamento
            
        Returns:
            Appointment: Consulta cancelada
            
        Raises:
            NotFoundError: Se a consulta não for encontrada
            BusinessRuleError: Se a consulta não puder ser cancelada
        """
        appt = self.get_by_id(appointment_id)
        
        if appt.status in ['cancelled', 'completed']:
            raise BusinessRuleError(f"Consulta com status '{appt.status}' não pode ser cancelada")
        
        appt.cancel(reason)
        self.appointment_repository.update(appt)
        return appt

    def complete_appointment(self, appointment_id: int) -> Appointment:
        """
        Marca uma consulta como concluída.
        
        Args:
            appointment_id: ID da consulta
            
        Returns:
            Appointment: Consulta concluída
            
        Raises:
            NotFoundError: Se a consulta não for encontrada
            BusinessRuleError: Se a consulta não puder ser concluída
        """
        appt = self.get_by_id(appointment_id)
        
        if appt.status not in ['scheduled', 'confirmed']:
            raise BusinessRuleError(f"Consulta com status '{appt.status}' não pode ser concluída")
        
        appt.complete()
        self.appointment_repository.update(appt)
        return appt

    def delete_appointment(self, appointment_id: int) -> None:
        """
        Remove uma consulta do sistema.
        
        Args:
            appointment_id: ID da consulta
            
        Raises:
            NotFoundError: Se a consulta não for encontrada
        """
        self.get_by_id(appointment_id)
        self.appointment_repository.delete(appointment_id)
