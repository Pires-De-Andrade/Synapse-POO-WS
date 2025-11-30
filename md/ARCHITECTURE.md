# Arquitetura do Synapse

## 1. Visão Geral

O Synapse é um sistema de agendamento de consultas psicológicas que utiliza arquitetura em camadas, alinhada aos princípios de Programação Orientada a Objetos (POO) e padrões de Engenharia de Software. Cada camada possui uma única responsabilidade (SRP) e depende de abstrações (Dependency Inversion Principle).

## 2. Estrutura de Pastas

\`\`\`
synapse/
├── api/
│   ├── dto.py              # Data Transfer Objects (Pydantic)
│   ├── response.py         # Classe ApiResponse para respostas padronizadas
│   ├── exceptions.py       # Exceções customizadas
│   └── middlewares/        # Middlewares da API
├── business_model/
│   ├── patient.py          # Entidade Paciente
│   ├── psychologist.py     # Entidade Psicólogo
│   ├── clinic.py           # Entidade Clínica
│   ├── appointment.py      # Entidade Consulta
│   ├── availability.py     # Entidade Disponibilidade
│   ├── lead.py             # Entidade Lead
│   └── user.py             # Entidade Usuário
├── repositories/
│   ├── interfaces/
│   │   └── abstract_repository.py  # Interface genérica
│   └── implementations/
│       ├── inmemory_patient_repository.py
│       ├── inmemory_psychologist_repository.py
│       ├── inmemory_appointment_repository.py
│       ├── inmemory_availability_repository.py
│       ├── inmemory_clinic_repository.py
│       ├── inmemory_lead_repository.py
│       └── inmemory_user_repository.py
├── services/
│   ├── patient_service.py
│   ├── psychologist_service.py
│   ├── appointment_service.py
│   ├── availability_service.py
│   ├── clinic_service.py
│   ├── lead_service.py
│   ├── auth_service.py
│   └── seed_loader.py
├── controllers/
│   ├── patient_controller.py
│   ├── psychologist_controller.py
│   ├── appointment_controller.py
│   ├── availability_controller.py
│   ├── clinic_controller.py
│   ├── lead_controller.py
│   └── auth_controller.py
├── views/
│   ├── templates/          # Templates HTML
│   └── static/             # CSS e JavaScript
├── config/                 # Configurações globais
├── tests/                  # Testes unitários/integrados
└── seeds.json              # Dados iniciais
main.py                     # Ponto de entrada da aplicação
\`\`\`

## 3. Padrões de Projeto Aplicados

### Repository Pattern (repositories/)
Abstrai a camada de persistência, permitindo trocar facilmente entre diferentes estratégias (in-memory, banco de dados, etc.).

\`\`\`python
class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> None: ...
    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]: ...
    @abstractmethod
    def all(self) -> List[T]: ...
    @abstractmethod
    def update(self, entity: T) -> None: ...
    @abstractmethod
    def delete(self, entity_id: int) -> None: ...
\`\`\`

### Dependency Injection (services/)
Services recebem repositórios injetados, reduzindo acoplamento e facilitando testes.

\`\`\`python
class PatientService:
    def __init__(self, patient_repository: InMemoryPatientRepository):
        self.patient_repository = patient_repository
\`\`\`

### Factory Pattern
Métodos `from_dict()` e `to_dict()` para serialização/deserialização de entidades.

\`\`\`python
@classmethod
def from_dict(cls, data: Dict):
    return cls(**data)

def to_dict(self) -> Dict:
    return {"id": self.id, "name": self.name, ...}
\`\`\`

### Custom Exceptions (api/exceptions.py)
Hierarquia de exceções para tratamento específico de erros.

\`\`\`python
class SynapseException(Exception): ...
class NotFoundError(SynapseException): ...
class ValidationError(SynapseException): ...
class ConflictError(SynapseException): ...
class BusinessRuleError(SynapseException): ...
\`\`\`

### Response Standardization (api/response.py)
Classe `ApiResponse` para garantir formato consistente em todas as respostas HTTP.

\`\`\`python
class ApiResponse:
    @staticmethod
    def success(data, message=None, status_code=200): ...
    @staticmethod
    def error(message, code, status_code=400): ...
    @staticmethod
    def not_found(resource, resource_id=None): ...
    @staticmethod
    def validation_error(message, field=None): ...
\`\`\`

### DTO Pattern (api/dto.py)
Data Transfer Objects usando Pydantic para validação automática de entrada.

\`\`\`python
class PatientCreateDTO(BaseModel):
    name: str
    email: EmailStr
    phone: str
    cpf: Optional[str] = None
    
    @field_validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v.strip()
\`\`\`

## 4. Arquitetura em Camadas

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                                │
│                    (Frontend/API Consumer)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CONTROLLERS                             │
│  - Recebem requisições HTTP                                  │
│  - Validam DTOs (Pydantic)                                   │
│  - Delegam para Services                                     │
│  - Retornam respostas padronizadas (ApiResponse)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       SERVICES                               │
│  - Contêm lógica de negócio                                  │
│  - Orquestram operações entre repositórios                   │
│  - Lançam exceções customizadas                              │
│  - Aplicam validações de regras de negócio                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     REPOSITORIES                             │
│  - Abstraem persistência de dados                            │
│  - Implementam interface genérica                            │
│  - Atualmente: In-Memory (dicionários Python)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS MODELS                           │
│  - Entidades do domínio                                      │
│  - Validações de dados (email, telefone, CRP)               │
│  - Métodos de negócio (cancel, complete, activate)          │
└─────────────────────────────────────────────────────────────┘
\`\`\`

## 5. Fluxo de Requisição (Exemplo: Agendar Consulta)

\`\`\`
1. Cliente → POST /api/appointments
   Body: {patient_id, psychologist_id, date, time, duration, notes}

2. appointment_controller.py
   ├─ Parseia JSON da requisição
   ├─ Valida com AppointmentCreateDTO (Pydantic)
   └─ Chama: appointment_service.schedule_appointment()

3. appointment_service.py
   ├─ Busca paciente (NotFoundError se não existir)
   ├─ Busca psicólogo (NotFoundError se não existir)
   ├─ Verifica se psicólogo está ativo (BusinessRuleError)
   ├─ Converte e valida data/hora (ValidationError)
   ├─ Verifica disponibilidade no dia (BusinessRuleError)
   ├─ Verifica conflitos de horário (ConflictError)
   └─ Cria e salva Appointment

4. appointment_repository.py
   └─ Armazena: self._appointments[id] = entity

5. Controller recebe resultado
   ├─ Sucesso → ApiResponse.created(appointment.to_dict())
   └─ Erro → ApiResponse.error/not_found/conflict/business_error

6. Cliente recebe JSON padronizado
   └─ {success: true/false, data/error: {...}}
\`\`\`

## 6. Tratamento de Erros

| Exceção | Código HTTP | Uso |
|---------|-------------|-----|
| NotFoundError | 404 | Recurso não encontrado |
| ValidationError | 400 | Dados de entrada inválidos |
| ConflictError | 409 | Conflito (ex: horário ocupado) |
| BusinessRuleError | 422 | Violação de regra de negócio |

## 7. DTOs Disponíveis

### Pacientes
- PatientCreateDTO, PatientUpdateDTO, PatientResponseDTO

### Psicólogos
- PsychologistCreateDTO, PsychologistUpdateDTO, PsychologistResponseDTO

### Clínicas
- ClinicCreateDTO, ClinicUpdateDTO, ClinicResponseDTO

### Disponibilidades
- AvailabilityCreateDTO, AvailabilityUpdateDTO, AvailabilityResponseDTO

### Consultas
- AppointmentCreateDTO, AppointmentUpdateDTO, AppointmentCancelDTO, AvailableSlotsRequestDTO

### Leads
- LeadCreateDTO, LeadUpdateDTO, LeadContactedDTO, LeadLostDTO, LeadConvertDTO

## 8. Princípios SOLID Aplicados

| Princípio | Aplicação |
|-----------|-----------|
| **S**ingle Responsibility | Cada classe tem uma responsabilidade única (Controller, Service, Repository) |
| **O**pen/Closed | Extensível via novas implementações de Repository sem modificar código existente |
| **L**iskov Substitution | Repositories são intercambiáveis (in-memory pode ser trocado por SQL) |
| **I**nterface Segregation | AbstractRepository define interface mínima necessária |
| **D**ependency Inversion | Services dependem de abstrações (interfaces), não de implementações concretas |

## 9. Seed Data

O sistema inicializa com dados de teste prontos para uso:
- Usuários com credenciais pré-definidas
- Psicólogos com especialidades e disponibilidades
- Pacientes cadastrados
- Consultas agendadas
- Leads em diferentes status

Arquivo: `synapse/seeds.json`

## 10. Execução Local

\`\`\`bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python main.py

# API disponível em http://localhost:5000
\`\`\`

Sem necessidade de Docker ou banco de dados externo.
