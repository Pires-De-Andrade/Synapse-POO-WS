# Arquitetura do Synapse

## 1. Visão Geral

O Synapse é um sistema de agendamento de consultas psicológicas desenvolvido como projeto acadêmico para demonstrar conceitos avançados de **Programação Orientada a Objetos (POO)** e **Engenharia de Software**. O sistema utiliza **arquitetura em camadas** com separação clara de responsabilidades, alinhada aos princípios **SOLID** e aplicando diversos **padrões de projeto** consolidados na indústria.

### Características Principais

- **API REST completa** com endpoints para todas as operações CRUD
- **Arquitetura em camadas** com baixo acoplamento e alta coesão
- **Validação automática** de dados de entrada com Pydantic
- **Tratamento de erros** robusto com exceções customizadas
- **Respostas padronizadas** para todas as requisições
- **Separação de responsabilidades** seguindo princípios SOLID
- **Facilmente extensível** - preparado para migração de persistência in-memory para banco de dados relacional

## 2. Estrutura de Pastas

\`\`\`
synapse/
├── api/                        # Camada de API (DTOs, Respostas, Exceções)
│   ├── dto.py                  # Data Transfer Objects (Pydantic)
│   ├── response.py             # ApiResponse para respostas padronizadas
│   └── exceptions.py           # Exceções customizadas (NotFoundError, etc.)
│
├── business_model/             # Entidades do Domínio (Modelos de Negócio)
│   ├── patient.py              # Entidade Paciente
│   ├── psychologist.py         # Entidade Psicólogo
│   ├── clinic.py               # Entidade Clínica
│   ├── appointment.py          # Entidade Consulta
│   ├── availability.py         # Entidade Disponibilidade
│   ├── lead.py                 # Entidade Lead
│   └── user.py                 # Entidade Usuário (autenticação)
│
├── repositories/               # Camada de Persistência (Repository Pattern)
│   ├── interfaces/
│   │   └── abstract_repository.py      # Interface genérica de Repository
│   └── implementations/
│       ├── inmemory_patient_repository.py
│       ├── inmemory_psychologist_repository.py
│       ├── inmemory_appointment_repository.py
│       ├── inmemory_availability_repository.py
│       ├── inmemory_clinic_repository.py
│       ├── inmemory_lead_repository.py
│       └── inmemory_user_repository.py
│
├── services/                   # Camada de Lógica de Negócio
│   ├── patient_service.py      # Lógica de negócio para pacientes
│   ├── psychologist_service.py # Lógica de negócio para psicólogos
│   ├── appointment_service.py  # Lógica de agendamento e validações
│   ├── availability_service.py # Cálculo de slots disponíveis
│   ├── clinic_service.py       # Gestão de clínicas
│   ├── lead_service.py         # Gestão de leads e conversões
│   ├── auth_service.py         # Autenticação e sessões
│   └── seed_loader.py          # Carregamento de dados iniciais
│
├── controllers/                # Camada de Controle (Endpoints REST)
│   ├── patient_controller.py
│   ├── psychologist_controller.py
│   ├── appointment_controller.py
│   ├── availability_controller.py
│   ├── clinic_controller.py
│   ├── lead_controller.py
│   └── auth_controller.py
│
├── views/                      # Interface Web (Frontend)
│   ├── templates/              # Templates HTML (Jinja2)
│   │   ├── patient_login.html
│   │   ├── patient_booking.html
│   │   ├── psychologist_dashboard.html
│   │   └── ...
│   └── static/                 # Assets estáticos (CSS/JS)
│       ├── css/
│       └── js/
│
├── config/                     # Configurações globais
├── tests/                      # Testes unitários e de integração
└── seeds.json                  # Dados iniciais para desenvolvimento

main.py                         # Ponto de entrada da aplicação Flask
requirements.txt                # Dependências Python
\`\`\`

## 3. Arquitetura em Camadas

O sistema segue uma arquitetura em 5 camadas, onde cada camada tem uma responsabilidade única e bem definida:

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                               │
│              (Browser, Postman, cURL, etc.)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP Request
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    1. CONTROLLERS                            │
│                   (Camada de Controle)                       │
│                                                              │
│  Responsabilidades:                                          │
│  ✓ Receber requisições HTTP (GET, POST, PUT, DELETE)        │
│  ✓ Validar DTOs com Pydantic                                │
│  ✓ Delegar operações para Services                          │
│  ✓ Tratar exceções e retornar respostas padronizadas        │
│  ✓ Gerenciar sessões e autenticação                         │
│                                                              │
│  Exemplo: appointment_controller.py                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ Chama métodos
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     2. SERVICES                              │
│                (Camada de Lógica de Negócio)                │
│                                                              │
│  Responsabilidades:                                          │
│  ✓ Implementar regras de negócio complexas                  │
│  ✓ Orquestrar operações entre múltiplos repositórios        │
│  ✓ Validar consistência de dados                            │
│  ✓ Lançar exceções customizadas                             │
│  ✓ Aplicar cálculos e transformações                        │
│                                                              │
│  Exemplo: appointment_service.py                             │
│  - Verifica disponibilidade do psicólogo                    │
│  - Valida conflitos de horário                              │
│  - Calcula slots disponíveis                                │
└──────────────────────────┬──────────────────────────────────┘
                           │ Acessa dados via
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   3. REPOSITORIES                            │
│               (Camada de Persistência)                       │
│                                                              │
│  Responsabilidades:                                          │
│  ✓ Abstrair mecanismo de persistência                       │
│  ✓ Implementar operações CRUD básicas                       │
│  ✓ Permitir troca fácil de estratégia (in-memory → SQL)    │
│  ✓ Isolar serviços da implementação de banco de dados      │
│                                                              │
│  Exemplo: inmemory_appointment_repository.py                 │
│  Interface: AbstractRepository<T>                            │
└──────────────────────────┬──────────────────────────────────┘
                           │ Manipula
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  4. BUSINESS MODELS                          │
│                 (Entidades do Domínio)                       │
│                                                              │
│  Responsabilidades:                                          │
│  ✓ Representar entidades do mundo real                      │
│  ✓ Encapsular dados e comportamentos                        │
│  ✓ Validar dados no momento da criação                      │
│  ✓ Fornecer métodos de conversão (to_dict, from_dict)      │
│                                                              │
│  Exemplo: Appointment, Patient, Psychologist                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ Armazenados em
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   5. DATA STORAGE                            │
│                (Armazenamento de Dados)                      │
│                                                              │
│  Atual: In-Memory (dicionários Python)                       │
│  Futuro: PostgreSQL, MySQL, MongoDB, etc.                    │
│                                                              │
│  seeds.json → carregado na inicialização                     │
└─────────────────────────────────────────────────────────────┘
\`\`\`

## 4. Padrões de Projeto Aplicados

### 4.1 Repository Pattern

**Objetivo:** Abstrair a camada de persistência, permitindo trocar facilmente entre diferentes estratégias de armazenamento.

**Implementação:**

\`\`\`python
# repositories/interfaces/abstract_repository.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class AbstractRepository(ABC, Generic[T]):
    """Interface genérica para repositórios."""
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """Adiciona uma entidade."""
        pass
    
    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        """Busca entidade por ID."""
        pass
    
    @abstractmethod
    def all(self) -> List[T]:
        """Retorna todas as entidades."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """Atualiza uma entidade."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Remove uma entidade."""
        pass
\`\`\`

**Vantagens:**
- Facilita testes (mock de repositórios)
- Permite trocar persistência (in-memory → SQL) sem alterar services
- Reduz acoplamento entre camadas

### 4.2 Dependency Injection

**Objetivo:** Services recebem dependências (repositórios) injetadas, reduzindo acoplamento.

**Implementação:**

\`\`\`python
class AppointmentService:
    def __init__(
        self,
        appointment_repository: InMemoryAppointmentRepository,
        patient_repository: InMemoryPatientRepository,
        psychologist_repository: InMemoryPsychologistRepository,
        availability_repository: InMemoryAvailabilityRepository
    ):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.psychologist_repository = psychologist_repository
        self.availability_repository = availability_repository
\`\`\`

**Vantagens:**
- Facilita testes (injetar mocks)
- Reduz acoplamento
- Facilita manutenção

### 4.3 Factory Pattern

**Objetivo:** Criar objetos de forma padronizada a partir de dicionários (serialização/deserialização).

**Implementação:**

\`\`\`python
class Patient:
    @classmethod
    def from_dict(cls, data: Dict):
        """Cria instância a partir de dicionário."""
        return cls(
            id=data.get('id'),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            cpf=data.get('cpf'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict:
        """Converte instância para dicionário."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'cpf': self.cpf,
            'created_at': self.created_at
        }
\`\`\`

### 4.4 Custom Exceptions Hierarchy

**Objetivo:** Tratamento específico de erros com hierarquia de exceções.

**Implementação:**

\`\`\`python
class SynapseException(Exception):
    """Exceção base."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

class NotFoundError(SynapseException):
    """Recurso não encontrado (404)."""
    pass

class ValidationError(SynapseException):
    """Dados inválidos (400)."""
    pass

class ConflictError(SynapseException):
    """Conflito de recursos (409)."""
    pass

class BusinessRuleError(SynapseException):
    """Violação de regra de negócio (422)."""
    pass
\`\`\`

**Mapeamento HTTP:**

| Exceção | Código HTTP | Uso |
|---------|-------------|-----|
| NotFoundError | 404 | Paciente/Psicólogo não encontrado |
| ValidationError | 400 | Email inválido, telefone vazio |
| ConflictError | 409 | Horário já ocupado |
| BusinessRuleError | 422 | Psicólogo inativo, fora do horário |

### 4.5 Response Standardization

**Objetivo:** Garantir formato consistente em todas as respostas HTTP.

**Implementação:**

\`\`\`python
class ApiResponse:
    @staticmethod
    def success(data, message=None, status_code=200):
        """Resposta de sucesso."""
        return jsonify({
            'success': True,
            'data': data,
            'message': message
        }), status_code
    
    @staticmethod
    def error(message, code, status_code=400):
        """Resposta de erro."""
        return jsonify({
            'success': False,
            'error': {
                'message': message,
                'code': code
            }
        }), status_code
\`\`\`

**Formato de Resposta:**

\`\`\`json
// Sucesso
{
  "success": true,
  "data": { ... },
  "message": "Consulta agendada com sucesso"
}

// Erro
{
  "success": false,
  "error": {
    "message": "Paciente com ID 3 não encontrado",
    "code": "NOT_FOUND"
  }
}
\`\`\`

### 4.6 DTO Pattern (Data Transfer Objects)

**Objetivo:** Validar automaticamente dados de entrada usando Pydantic.

**Implementação:**

\`\`\`python
from pydantic import BaseModel, EmailStr, field_validator

class AppointmentCreateDTO(BaseModel):
    patient_id: int
    psychologist_id: int
    date: str  # yyyy-mm-dd
    time: str  # HH:MM
    duration: int = 60
    notes: Optional[str] = None
    
    @field_validator('duration')
    @classmethod
    def duration_valid(cls, v):
        if v < 15 or v > 180:
            raise ValueError('Duração entre 15 e 180 minutos')
        return v
\`\`\`

**Vantagens:**
- Validação automática antes de processar requisição
- Documentação clara dos dados esperados
- Conversão automática de tipos
- Mensagens de erro padronizadas

## 5. Fluxo de Requisição Completo

Exemplo: **Agendar uma consulta**

\`\`\`
┌──────────────────────────────────────────────────────────────┐
│ 1. CLIENT                                                     │
│    POST /api/appointments                                     │
│    Body: {                                                    │
│      "patient_id": 3,                                        │
│      "psychologist_id": 1,                                   │
│      "date": "2025-12-01",                                   │
│      "time": "14:00",                                        │
│      "duration": 60                                          │
│    }                                                          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. CONTROLLER (appointment_controller.py)                    │
│    ├─ Recebe JSON da requisição                             │
│    ├─ Valida com AppointmentCreateDTO (Pydantic)            │
│    │   └─ Se inválido → ValidationError (400)               │
│    └─ Chama: appointment_service.schedule_appointment()     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. SERVICE (appointment_service.py)                          │
│    ├─ 1. Busca paciente (patient_repository.get(3))         │
│    │   └─ Se não existe → NotFoundError (404)               │
│    │                                                          │
│    ├─ 2. Busca psicólogo (psychologist_repository.get(1))   │
│    │   └─ Se não existe → NotFoundError (404)               │
│    │                                                          │
│    ├─ 3. Verifica se psicólogo está ativo                   │
│    │   └─ Se inativo → BusinessRuleError (422)              │
│    │                                                          │
│    ├─ 4. Converte data/hora string para datetime            │
│    │   └─ Se formato inválido → ValidationError (400)       │
│    │                                                          │
│    ├─ 5. Busca disponibilidades do psicólogo no dia         │
│    │   └─ Se não tem disponibilidade → BusinessRuleError    │
│    │                                                          │
│    ├─ 6. Verifica se horário está dentro da disponibilidade │
│    │   └─ Se fora do horário → BusinessRuleError            │
│    │                                                          │
│    ├─ 7. Busca consultas existentes do psicólogo na data    │
│    │                                                          │
│    ├─ 8. Verifica conflitos de horário                      │
│    │   └─ Se conflito → ConflictError (409)                 │
│    │                                                          │
│    ├─ 9. Cria objeto Appointment                            │
│    │                                                          │
│    └─ 10. Salva via appointment_repository.add()            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. REPOSITORY (inmemory_appointment_repository.py)           │
│    └─ Armazena: self._appointments[id] = appointment         │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. CONTROLLER retorna resposta                               │
│    ├─ Sucesso: ApiResponse.created(appointment.to_dict())   │
│    └─ Erro: ApiResponse.error/not_found/conflict            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. CLIENT recebe JSON                                        │
│    {                                                          │
│      "success": true,                                        │
│      "data": {                                               │
│        "id": 4,                                              │
│        "patient_id": 3,                                      │
│        "psychologist_id": 1,                                 │
│        "date": "2025-12-01",                                 │
│        "time": "14:00",                                      │
│        "duration": 60,                                       │
│        "status": "scheduled"                                 │
│      },                                                       │
│      "message": "Consulta agendada com sucesso"             │
│    }                                                          │
└──────────────────────────────────────────────────────────────┘
\`\`\`

## 6. Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
Cada classe tem uma única responsabilidade:
- **Controllers**: Gerenciar requisições HTTP
- **Services**: Implementar lógica de negócio
- **Repositories**: Gerenciar persistência
- **Models**: Representar entidades do domínio

### Open/Closed Principle (OCP)
Sistema extensível sem modificar código existente:
- Novas implementações de Repository (SQL, NoSQL) sem alterar Services
- Novos tipos de autenticação sem alterar AuthService

### Liskov Substitution Principle (LSP)
Repositories são intercambiáveis:
- `InMemoryAppointmentRepository` pode ser substituído por `SQLAppointmentRepository`
- Services funcionam com qualquer implementação de `AbstractRepository`

### Interface Segregation Principle (ISP)
Interfaces mínimas e específicas:
- `AbstractRepository` define apenas operações essenciais
- DTOs específicos para cada operação (CreateDTO, UpdateDTO)

### Dependency Inversion Principle (DIP)
Dependência de abstrações, não implementações:
- Services dependem de `AbstractRepository`, não de implementações concretas
- Facilita testes com mocks

## 7. DTOs Disponíveis

### Autenticação
- `AuthLoginDTO` - Login de usuários
- `AuthResponseDTO` - Resposta de autenticação

### Pacientes
- `PatientCreateDTO` - Criar paciente
- `PatientUpdateDTO` - Atualizar paciente
- `PatientResponseDTO` - Resposta com dados do paciente

### Psicólogos
- `PsychologistCreateDTO` - Criar psicólogo
- `PsychologistUpdateDTO` - Atualizar psicólogo
- `PsychologistResponseDTO` - Resposta com dados do psicólogo

### Clínicas
- `ClinicCreateDTO`, `ClinicUpdateDTO`, `ClinicResponseDTO`

### Disponibilidades
- `AvailabilityCreateDTO` - Criar disponibilidade
- `AvailabilityUpdateDTO` - Atualizar disponibilidade
- `AvailabilityResponseDTO` - Resposta com disponibilidade

### Consultas
- `AppointmentCreateDTO` - Agendar consulta
- `AppointmentUpdateDTO` - Atualizar consulta
- `AppointmentCancelDTO` - Cancelar consulta
- `AvailableSlotsRequestDTO` - Buscar horários disponíveis

### Leads
- `LeadCreateDTO`, `LeadUpdateDTO`, `LeadContactedDTO`, `LeadLostDTO`, `LeadConvertDTO`

## 8. Dados Iniciais (Seed Data)

O sistema inicializa com dados de teste prontos para demonstração:

**Usuários:**
- Psicólogo: `carlos@psi.com` / `senha123`
- Clínica: `clinica@exemplo.com` / `senha123`
- Paciente: `maria@exemplo.com` / `senha123`

**Dados pré-cadastrados:**
- 1 Psicólogo com especialidades e disponibilidades
- 1 Paciente ativo
- 1 Clínica cadastrada
- Disponibilidades: Segunda a Sexta (diferentes horários)
- 1 Consulta agendada para demonstração

Arquivo: `synapse/seeds.json`

## 9. Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.8+ | Linguagem principal |
| Flask | 2.x | Framework web |
| Pydantic | 2.x | Validação de dados |
| bcrypt | 4.x | Criptografia de senhas |
| Jinja2 | 3.x | Templates HTML |

## 10. Execução Local

\`\`\`bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar servidor Flask
python main.py

# 3. Acessar aplicação
# Interface web: http://localhost:5000
# API REST: http://localhost:5000/api/*
\`\`\`

Sem necessidade de Docker ou banco de dados externo. Ideal para desenvolvimento e apresentações acadêmicas.

## 11. Extensibilidade

### Adicionar Persistência SQL

1. Criar `SQLAppointmentRepository` implementando `AbstractRepository`
2. Injetar no `AppointmentService`
3. Nenhuma alteração necessária em Services ou Controllers

\`\`\`python
class SQLAppointmentRepository(AbstractRepository[Appointment]):
    def add(self, entity: Appointment):
        # Usar SQLAlchemy ou psycopg2
        pass
\`\`\`

### Adicionar Autenticação JWT

1. Criar `JWTAuthService` estendendo `AuthService`
2. Atualizar `auth_controller.py`
3. Services e Models permanecem inalterados

## 12. Documentação Adicional

- **API_DOCS.md** - Documentação completa da API REST
- **README.md** - Guia de instalação e uso
- **APRESENTACAO.md** - Roteiro para apresentação acadêmica
- **CREDENCIAIS_TESTE.md** - Credenciais para testes
