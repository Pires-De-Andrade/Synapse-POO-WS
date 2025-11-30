"""
Data Transfer Objects (DTOs) para validação de entrada/saída da API.
Utiliza Pydantic para validação automática e documentação.
"""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List


# =============================================================================
# AUTH DTOs
# =============================================================================

class AuthLoginDTO(BaseModel):
    """DTO para requisição de login."""
    email: EmailStr
    password: str


class AuthResponseDTO(BaseModel):
    """DTO para resposta de autenticação."""
    token: str
    user_id: int
    name: str
    user_type: str


# =============================================================================
# PATIENT DTOs
# =============================================================================

class PatientCreateDTO(BaseModel):
    """DTO para criação de paciente."""
    name: str
    email: EmailStr
    phone: str
    cpf: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip()
    
    @field_validator('phone')
    @classmethod
    def phone_valid(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Telefone deve ter pelo menos 8 caracteres')
        return v


class PatientUpdateDTO(BaseModel):
    """DTO para atualização de paciente."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None


class PatientResponseDTO(BaseModel):
    """DTO para resposta de paciente."""
    id: int
    name: str
    email: str
    phone: str
    cpf: Optional[str] = None
    created_at: str


# =============================================================================
# PSYCHOLOGIST DTOs
# =============================================================================

class PsychologistCreateDTO(BaseModel):
    """DTO para criação de psicólogo."""
    user_id: int
    name: str
    crp: str
    specialty: str
    hourly_rate: float
    themes: Optional[List[str]] = None
    bio: Optional[str] = ""
    
    @field_validator('crp')
    @classmethod
    def crp_valid(cls, v):
        if not v or '/' not in v:
            raise ValueError('CRP deve estar no formato XX/XXXXX')
        return v
    
    @field_validator('hourly_rate')
    @classmethod
    def rate_positive(cls, v):
        if v <= 0:
            raise ValueError('Valor hora deve ser positivo')
        return v


class PsychologistUpdateDTO(BaseModel):
    """DTO para atualização de psicólogo."""
    name: Optional[str] = None
    specialty: Optional[str] = None
    themes: Optional[List[str]] = None
    bio: Optional[str] = None
    hourly_rate: Optional[float] = None
    is_active: Optional[bool] = None


class PsychologistResponseDTO(BaseModel):
    """DTO para resposta de psicólogo."""
    id: int
    user_id: int
    name: str
    crp: str
    specialty: str
    themes: List[str]
    bio: str
    hourly_rate: float
    is_active: bool
    created_at: str


# =============================================================================
# CLINIC DTOs
# =============================================================================

class ClinicCreateDTO(BaseModel):
    """DTO para criação de clínica."""
    user_id: int
    name: str
    address: str
    phone: str
    email: EmailStr
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip()


class ClinicUpdateDTO(BaseModel):
    """DTO para atualização de clínica."""
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class ClinicResponseDTO(BaseModel):
    """DTO para resposta de clínica."""
    id: int
    user_id: int
    name: str
    address: str
    phone: str
    email: str
    created_at: str


# =============================================================================
# AVAILABILITY DTOs
# =============================================================================

class AvailabilityCreateDTO(BaseModel):
    """DTO para criação de disponibilidade."""
    psychologist_id: int
    day_of_week: int  # 0=Segunda, 6=Domingo
    start_time: str   # HH:MM
    end_time: str     # HH:MM
    
    @field_validator('day_of_week')
    @classmethod
    def day_valid(cls, v):
        if v < 0 or v > 6:
            raise ValueError('Dia da semana deve ser entre 0 (Segunda) e 6 (Domingo)')
        return v
    
    @field_validator('start_time', 'end_time')
    @classmethod
    def time_format(cls, v):
        try:
            parts = v.split(':')
            if len(parts) != 2:
                raise ValueError()
            h, m = int(parts[0]), int(parts[1])
            if h < 0 or h > 23 or m < 0 or m > 59:
                raise ValueError()
        except:
            raise ValueError('Horário deve estar no formato HH:MM')
        return v


class AvailabilityUpdateDTO(BaseModel):
    """DTO para atualização de disponibilidade."""
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_active: Optional[bool] = None


class AvailabilityResponseDTO(BaseModel):
    """DTO para resposta de disponibilidade."""
    id: int
    psychologist_id: int
    day_of_week: int
    start_time: str
    end_time: str
    is_active: bool


# =============================================================================
# APPOINTMENT DTOs
# =============================================================================

class AppointmentCreateDTO(BaseModel):
    """DTO para criação de consulta."""
    patient_id: int
    psychologist_id: int
    date: str   # yyyy-mm-dd
    time: str   # HH:MM
    duration: int = 60
    notes: Optional[str] = None
    
    @field_validator('duration')
    @classmethod
    def duration_valid(cls, v):
        if v < 15 or v > 180:
            raise ValueError('Duração deve ser entre 15 e 180 minutos')
        return v


class AppointmentUpdateDTO(BaseModel):
    """DTO para atualização de consulta."""
    date: Optional[str] = None
    time: Optional[str] = None
    duration: Optional[int] = None
    notes: Optional[str] = None


class AppointmentCancelDTO(BaseModel):
    """DTO para cancelamento de consulta."""
    cancellation_reason: Optional[str] = None


class AppointmentResponseDTO(BaseModel):
    """DTO para resposta de consulta."""
    id: int
    patient_id: int
    psychologist_id: int
    date: str
    time: str
    duration: int
    status: str
    notes: Optional[str] = None


class AvailableSlotsRequestDTO(BaseModel):
    """DTO para requisição de horários disponíveis."""
    psychologist_id: int
    date: str
    duration: int = 60


# =============================================================================
# LEAD DTOs
# =============================================================================

class LeadCreateDTO(BaseModel):
    """DTO para criação de lead."""
    name: str
    email: EmailStr
    phone: str
    source: str
    notes: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip()


class LeadUpdateDTO(BaseModel):
    """DTO para atualização de lead."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class LeadContactedDTO(BaseModel):
    """DTO para marcar lead como contatado."""
    notes: Optional[str] = None


class LeadLostDTO(BaseModel):
    """DTO para marcar lead como perdido."""
    reason: Optional[str] = None


class LeadConvertDTO(BaseModel):
    """DTO para conversão de lead em paciente."""
    patient_id: int


class LeadResponseDTO(BaseModel):
    """DTO para resposta de lead."""
    id: int
    name: str
    email: str
    phone: str
    source: str
    status: str
    notes: Optional[str] = None
    created_at: str
    converted_at: Optional[str] = None
    converted_to_patient_id: Optional[int] = None
