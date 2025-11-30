# Documentação de Endpoints - Synapse API

## Formato Padrão de Respostas

### Resposta de Sucesso
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Mensagem opcional"
}
\`\`\`

### Resposta de Lista
\`\`\`json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "count": 10
  }
}
\`\`\`

### Resposta de Erro
\`\`\`json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Descrição do erro",
    "field": "campo_opcional"
  }
}
\`\`\`

### Códigos de Erro
| Código | HTTP | Descrição |
|--------|------|-----------|
| VALIDATION_ERROR | 400 | Dados de entrada inválidos |
| NOT_FOUND | 404 | Recurso não encontrado |
| CONFLICT | 409 | Conflito de recursos |
| BUSINESS_RULE_VIOLATION | 422 | Regra de negócio violada |

---

## Auth

### POST /api/auth/login
Autentica um usuário no sistema.

**Request Body:**
\`\`\`json
{
  "email": "dra.ana@clinica.com",
  "password": "senha123"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "token": "abc.def.ghi",
    "user_id": 1,
    "name": "Dra. Ana Silva",
    "user_type": "psychologist"
  }
}
\`\`\`

**Erros:**
- 401: Credenciais inválidas

---

## Patients

### GET /api/patients
Lista todos os pacientes.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "name": "João Pedro Santos",
        "email": "joao@email.com",
        "phone": "(11) 98765-4321",
        "cpf": "123.456.789-00",
        "created_at": "2025-01-01T10:00:00"
      }
    ],
    "count": 1
  }
}
\`\`\`

### GET /api/patients/{id}
Busca um paciente pelo ID.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "João Pedro Santos",
    "email": "joao@email.com",
    "phone": "(11) 98765-4321",
    "cpf": "123.456.789-00",
    "created_at": "2025-01-01T10:00:00"
  }
}
\`\`\`

**Erros:**
- 404: Paciente não encontrado

### POST /api/patients
Cria um novo paciente.

**Request Body:**
\`\`\`json
{
  "name": "João Pedro Santos",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
\`\`\`

**Response (201):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Paciente criado com sucesso"
}
\`\`\`

**Erros:**
- 400: Dados inválidos (nome vazio, email inválido, telefone curto)

### PUT /api/patients/{id}
Atualiza os dados de um paciente.

**Request Body:**
\`\`\`json
{
  "name": "João Pedro Santos Atualizado",
  "phone": "(11) 91234-5678"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Paciente atualizado com sucesso"
}
\`\`\`

**Erros:**
- 404: Paciente não encontrado
- 400: Dados inválidos

### DELETE /api/patients/{id}
Remove um paciente do sistema.

**Response:** 204 No Content

**Erros:**
- 404: Paciente não encontrado

---

## Psychologists

### GET /api/psychologists
Lista todos os psicólogos.

**Query Params:**
- `active_only` (boolean): Se true, retorna apenas psicólogos ativos

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 1,
        "name": "Dra. Ana Silva",
        "crp": "06/12345",
        "specialty": "TCC",
        "themes": ["Ansiedade", "Depressão"],
        "bio": "Especialista em TCC",
        "hourly_rate": 150.0,
        "is_active": true,
        "created_at": "2025-01-01T10:00:00"
      }
    ],
    "count": 1
  }
}
\`\`\`

### GET /api/psychologists/{id}
Busca um psicólogo pelo ID.

### POST /api/psychologists
Cria um novo psicólogo.

**Request Body:**
\`\`\`json
{
  "user_id": 1,
  "name": "Dra. Ana Silva",
  "crp": "06/12345",
  "specialty": "TCC",
  "themes": ["Ansiedade", "Depressão"],
  "hourly_rate": 150.0,
  "bio": "Especialista em TCC"
}
\`\`\`

**Validações:**
- CRP deve estar no formato XX/XXXXX
- hourly_rate deve ser positivo

### PUT /api/psychologists/{id}
Atualiza os dados de um psicólogo.

**Request Body:**
\`\`\`json
{
  "specialty": "Psicanálise",
  "hourly_rate": 180.0,
  "is_active": true
}
\`\`\`

### DELETE /api/psychologists/{id}
Remove um psicólogo do sistema.

### PATCH /api/psychologists/{id}/activate
Ativa um psicólogo.

### PATCH /api/psychologists/{id}/deactivate
Desativa um psicólogo.

---

## Clinics

### GET /api/clinics
Lista todas as clínicas.

### GET /api/clinics/{id}
Busca uma clínica pelo ID.

### POST /api/clinics
Cria uma nova clínica.

**Request Body:**
\`\`\`json
{
  "user_id": 1,
  "name": "Clínica Saúde Mental",
  "address": "Rua das Flores, 123",
  "phone": "(11) 3456-7890",
  "email": "contato@clinica.com"
}
\`\`\`

### PUT /api/clinics/{id}
Atualiza os dados de uma clínica.

### DELETE /api/clinics/{id}
Remove uma clínica do sistema.

---

## Availabilities

### GET /api/availabilities
Lista todas as disponibilidades.

**Query Params:**
- `psychologist_id` (int): Filtrar por psicólogo

### GET /api/availabilities/{id}
Busca uma disponibilidade pelo ID.

### GET /api/availabilities/psychologist/{psychologist_id}
Lista todas as disponibilidades de um psicólogo.

### POST /api/availabilities
Cria uma nova disponibilidade.

**Request Body:**
\`\`\`json
{
  "psychologist_id": 1,
  "day_of_week": 1,
  "start_time": "08:00",
  "end_time": "12:00"
}
\`\`\`

**Validações:**
- day_of_week: 0 (Segunda) a 6 (Domingo)
- start_time/end_time: formato HH:MM
- start_time deve ser anterior a end_time
- Não pode haver sobreposição com disponibilidades existentes

**Erros:**
- 404: Psicólogo não encontrado
- 409: Sobreposição de horários

### PUT /api/availabilities/{id}
Atualiza uma disponibilidade.

**Request Body:**
\`\`\`json
{
  "start_time": "09:00",
  "end_time": "13:00",
  "is_active": true
}
\`\`\`

### DELETE /api/availabilities/{id}
Remove uma disponibilidade do sistema.

### PATCH /api/availabilities/{id}/activate
Ativa uma disponibilidade.

### PATCH /api/availabilities/{id}/deactivate
Desativa uma disponibilidade.

---

## Appointments

### GET /api/appointments
Lista todas as consultas.

**Query Params:**
- `patient_id` (int): Filtrar por paciente
- `psychologist_id` (int): Filtrar por psicólogo

### GET /api/appointments/{id}
Busca uma consulta pelo ID.

### POST /api/appointments
Agenda uma nova consulta.

**Request Body:**
\`\`\`json
{
  "patient_id": 1,
  "psychologist_id": 1,
  "date": "2025-12-08",
  "time": "14:00",
  "duration": 60,
  "notes": "Primeira consulta"
}
\`\`\`

**Validações:**
- Paciente e psicólogo devem existir
- Psicólogo deve estar ativo
- Data deve ser futura
- Horário deve estar dentro da disponibilidade do psicólogo
- Não pode haver conflito de horários
- Duração entre 15 e 180 minutos

**Response (201):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "patient_id": 1,
    "psychologist_id": 1,
    "date": "2025-12-08",
    "time": "14:00:00",
    "duration": 60,
    "status": "scheduled",
    "notes": "Primeira consulta"
  },
  "message": "Consulta agendada com sucesso"
}
\`\`\`

**Erros:**
- 404: Paciente ou psicólogo não encontrado
- 409: Conflito de horário
- 422: Psicólogo inativo ou sem disponibilidade

### DELETE /api/appointments/{id}
Remove uma consulta do sistema.

### PATCH /api/appointments/{id}/cancel
Cancela uma consulta.

**Request Body:**
\`\`\`json
{
  "cancellation_reason": "Imprevisto pessoal"
}
\`\`\`

**Erros:**
- 422: Consulta já cancelada ou concluída

### PATCH /api/appointments/{id}/complete
Marca uma consulta como concluída.

**Erros:**
- 422: Consulta não pode ser concluída (status inválido)

### POST /api/appointments/available-slots
Lista horários disponíveis para agendamento.

**Request Body:**
\`\`\`json
{
  "psychologist_id": 1,
  "date": "2025-12-08",
  "duration": 60
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "psychologist_id": 1,
    "date": "2025-12-08",
    "available_times": ["08:00", "08:15", "09:00", "10:30"],
    "count": 4
  }
}
\`\`\`

---

## Leads

### GET /api/leads
Lista todos os leads.

### GET /api/leads/{id}
Busca um lead pelo ID.

### POST /api/leads
Cria um novo lead.

**Request Body:**
\`\`\`json
{
  "name": "Maria Silva",
  "email": "maria@email.com",
  "phone": "(11) 91234-5678",
  "source": "website",
  "notes": "Interesse em terapia de casal"
}
\`\`\`

### PUT /api/leads/{id}
Atualiza os dados de um lead.

### DELETE /api/leads/{id}
Remove um lead do sistema.

### PATCH /api/leads/{id}/contacted
Marca um lead como contatado.

**Request Body:**
\`\`\`json
{
  "notes": "Ligação realizada, agendou visita"
}
\`\`\`

### PATCH /api/leads/{id}/lost
Marca um lead como perdido.

**Request Body:**
\`\`\`json
{
  "reason": "Optou por outro serviço"
}
\`\`\`

### PATCH /api/leads/{id}/convert
Converte um lead em paciente.

**Request Body:**
\`\`\`json
{
  "patient_id": 5
}
\`\`\`

**Erros:**
- 422: Lead já foi convertido anteriormente

---

## Health Check

### GET /health
Verifica o status da API.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "status": "healthy",
    "service": "Synapse API",
    "version": "1.0.0"
  }
}
\`\`\`

---

## Observações Gerais

- Todas as respostas seguem o formato padronizado com `success`, `data` e opcionalmente `message` ou `error`
- Datas no formato ISO 8601: `yyyy-mm-dd` ou `yyyy-mm-ddTHH:MM:SS`
- Horários no formato: `HH:MM`
- A autenticação está seedada com usuários prontos para teste
- Códigos HTTP: 200 (OK), 201 (Created), 204 (No Content), 400 (Validation Error), 404 (Not Found), 409 (Conflict), 422 (Business Rule Violation)
