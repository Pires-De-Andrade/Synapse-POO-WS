# Documentação da API REST - Synapse

## Índice
1. [Introdução à API REST](#introdução-à-api-rest)
2. [Arquitetura RESTful](#arquitetura-restful)
3. [Formato de Respostas](#formato-de-respostas)
4. [Como Testar a API](#como-testar-a-api)
5. [Endpoints por Recurso](#endpoints-por-recurso)
   - [Autenticação](#autenticação)
   - [Pacientes](#pacientes)
   - [Psicólogos](#psicólogos)
   - [Clínicas](#clínicas)
   - [Disponibilidades](#disponibilidades)
   - [Consultas](#consultas)
   - [Leads](#leads)
6. [Códigos de Status HTTP](#códigos-de-status-http)
7. [Exemplos de Uso](#exemplos-de-uso)

---

## Introdução à API REST

### O que é uma API REST?

**REST** (Representational State Transfer) é um estilo arquitetural para sistemas distribuídos que define como recursos são identificados e endereçados através de URLs e métodos HTTP.

**Características principais:**
- **Stateless**: Cada requisição é independente, não mantém estado de sessão
- **Client-Server**: Separação clara entre cliente e servidor
- **Recursos**: Tudo é tratado como recurso (pacientes, consultas, etc.)
- **Métodos HTTP**: Usa verbos HTTP para operações (GET, POST, PUT, DELETE, PATCH)
- **Representações JSON**: Dados trafegados em formato JSON

### Por que REST?

- **Simplicidade**: Usa protocolos web padrão (HTTP)
- **Escalabilidade**: Facilita cache e balanceamento de carga
- **Independência**: Qualquer cliente pode consumir (web, mobile, desktop)
- **Interoperabilidade**: Funciona em qualquer plataforma

---

## Arquitetura RESTful

### Métodos HTTP e Operações CRUD

| Método HTTP | Operação | Descrição | Exemplo |
|-------------|----------|-----------|---------|
| **GET** | Read | Busca recursos | `GET /api/patients` |
| **POST** | Create | Cria novo recurso | `POST /api/patients` |
| **PUT** | Update | Atualiza recurso completo | `PUT /api/patients/1` |
| **PATCH** | Partial Update | Atualiza parcialmente | `PATCH /api/appointments/1/cancel` |
| **DELETE** | Delete | Remove recurso | `DELETE /api/patients/1` |

### Estrutura de URLs

\`\`\`
/api/{recurso}              → Coleção (lista/criação)
/api/{recurso}/{id}         → Item específico
/api/{recurso}/{id}/{ação}  → Ação específica
\`\`\`

**Exemplos:**
- `/api/patients` → Lista todos os pacientes
- `/api/patients/3` → Busca o paciente com ID 3
- `/api/appointments/5/cancel` → Cancela a consulta 5

---

## Formato de Respostas

Todas as respostas seguem um formato padronizado para facilitar o tratamento de dados e erros.

### Resposta de Sucesso (Item Único)
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@email.com"
  },
  "message": "Operação realizada com sucesso"
}
\`\`\`

### Resposta de Lista
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      { "id": 1, "name": "João" },
      { "id": 2, "name": "Maria" }
    ],
    "count": 2
  }
}
\`\`\`

### Resposta de Erro
\`\`\`json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Nome é obrigatório",
    "field": "name"
  }
}
\`\`\`

### Códigos de Erro Personalizados

| Código | HTTP | Descrição | Quando Ocorre |
|--------|------|-----------|---------------|
| `VALIDATION_ERROR` | 400 | Dados inválidos | Campo obrigatório ausente, formato inválido |
| `NOT_FOUND` | 404 | Recurso não encontrado | ID inexistente |
| `CONFLICT` | 409 | Conflito de recursos | Horário já ocupado, email duplicado |
| `BUSINESS_RULE_VIOLATION` | 422 | Regra de negócio violada | Psicólogo inativo, consulta fora do horário |

---

## Como Testar a API

### 1. Executar o Servidor

\`\`\`bash
# Instalar dependências
pip install -r requirements.txt

# Executar o servidor Flask
python main.py
\`\`\`

O servidor inicia em: `http://localhost:5000`

### 2. Ferramentas para Testes

#### **Opção A: Postman** (Recomendado)

1. Baixe o [Postman](https://www.postman.com/downloads/)
2. Crie uma nova requisição
3. Configure:
   - **Method**: GET, POST, PUT, DELETE, etc.
   - **URL**: `http://localhost:5000/api/patients`
   - **Headers**: `Content-Type: application/json`
   - **Body** (para POST/PUT): JSON com os dados

**Exemplo de requisição POST no Postman:**
\`\`\`
Method: POST
URL: http://localhost:5000/api/patients
Headers:
  Content-Type: application/json
Body (raw JSON):
{
  "name": "João Silva",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
\`\`\`

#### **Opção B: cURL** (Linha de comando)

\`\`\`bash
# GET - Listar todos os pacientes
curl http://localhost:5000/api/patients

# POST - Criar novo paciente
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@email.com",
    "phone": "(11) 98765-4321"
  }'

# GET - Buscar paciente específico
curl http://localhost:5000/api/patients/1

# PUT - Atualizar paciente
curl -X PUT http://localhost:5000/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "João Pedro Silva"}'

# DELETE - Remover paciente
curl -X DELETE http://localhost:5000/api/patients/1
\`\`\`

#### **Opção C: Navegador** (apenas GET)

Para requisições GET, basta acessar diretamente no navegador:
- `http://localhost:5000/api/patients`
- `http://localhost:5000/api/psychologists`
- `http://localhost:5000/health`

#### **Opção D: Python requests**

\`\`\`python
import requests
import json

BASE_URL = "http://localhost:5000"

# GET - Listar pacientes
response = requests.get(f"{BASE_URL}/api/patients")
print(response.json())

# POST - Criar paciente
data = {
    "name": "João Silva",
    "email": "joao@email.com",
    "phone": "(11) 98765-4321"
}
response = requests.post(
    f"{BASE_URL}/api/patients",
    json=data,
    headers={"Content-Type": "application/json"}
)
print(response.json())
\`\`\`

### 3. Dados de Teste Disponíveis

O sistema já vem com dados pré-carregados no arquivo `synapse/seeds.json`:

**Credenciais de Login:**
- **Psicólogo**: `dra.ana@clinica.com` / `senha123`
- **Clínica**: `clinica@contato.com` / `senha123`
- **Paciente**: `maria@email.com` / `senha123`

**IDs de Teste:**
- Paciente ID: 3 (Maria Silva)
- Psicólogo ID: 1 (Dr. Carlos)
- Clínica ID: 1 (Clínica Esperança)

---

## Endpoints por Recurso

### Autenticação

#### `POST /api/auth/login`
Autentica um usuário no sistema e retorna um token de sessão.

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

**Possíveis Erros:**
- `401 Unauthorized`: Credenciais inválidas

**Teste com cURL:**
\`\`\`bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "maria@email.com", "password": "senha123"}'
\`\`\`

---

### Pacientes

#### `GET /api/patients`
Lista todos os pacientes cadastrados no sistema.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 3,
        "name": "Maria Silva",
        "email": "maria@email.com",
        "phone": "(11) 91234-5678",
        "cpf": "987.654.321-00",
        "created_at": "2025-01-15T10:00:00"
      }
    ],
    "count": 1
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/patients
\`\`\`

---

#### `GET /api/patients/{id}`
Busca um paciente específico pelo ID.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 3,
    "name": "Maria Silva",
    "email": "maria@email.com",
    "phone": "(11) 91234-5678",
    "cpf": "987.654.321-00",
    "created_at": "2025-01-15T10:00:00"
  }
}
\`\`\`

**Possíveis Erros:**
- `404 Not Found`: Paciente não encontrado

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/patients/3
\`\`\`

---

#### `POST /api/patients`
Cria um novo paciente no sistema.

**Request Body:**
\`\`\`json
{
  "name": "João Pedro Santos",
  "email": "joao@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
\`\`\`

**Validações:**
- `name`: Obrigatório, mínimo 3 caracteres
- `email`: Obrigatório, formato válido
- `phone`: Obrigatório, mínimo 10 caracteres
- `cpf`: Opcional

**Response (201):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "João Pedro Santos",
    "email": "joao@email.com",
    "phone": "(11) 98765-4321",
    "cpf": "123.456.789-00",
    "created_at": "2025-12-01T14:30:00"
  },
  "message": "Paciente criado com sucesso"
}
\`\`\`

**Possíveis Erros:**
- `400 Validation Error`: Dados inválidos

**Teste:**
\`\`\`bash
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Pedro Santos",
    "email": "joao@email.com",
    "phone": "(11) 98765-4321"
  }'
\`\`\`

---

#### `PUT /api/patients/{id}`
Atualiza os dados de um paciente existente.

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

**Possíveis Erros:**
- `404 Not Found`: Paciente não encontrado
- `400 Validation Error`: Dados inválidos

**Teste:**
\`\`\`bash
curl -X PUT http://localhost:5000/api/patients/3 \
  -H "Content-Type: application/json" \
  -d '{"phone": "(11) 99999-9999"}'
\`\`\`

---

#### `DELETE /api/patients/{id}`
Remove um paciente do sistema.

**Response:** `204 No Content`

**Possíveis Erros:**
- `404 Not Found`: Paciente não encontrado

**Teste:**
\`\`\`bash
curl -X DELETE http://localhost:5000/api/patients/4
\`\`\`

---

### Psicólogos

#### `GET /api/psychologists`
Lista todos os psicólogos cadastrados.

**Query Parameters:**
- `active_only` (boolean): Se `true`, retorna apenas psicólogos ativos

**Exemplo:** `/api/psychologists?active_only=true`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 1,
        "name": "Dr. Carlos Mendes",
        "crp": "06/123456",
        "specialty": "Terapia Cognitivo-Comportamental",
        "themes": ["Ansiedade", "Depressão", "Estresse"],
        "bio": "Especialista em TCC com 10 anos de experiência",
        "hourly_rate": 200.0,
        "is_active": true,
        "created_at": "2025-01-10T09:00:00"
      }
    ],
    "count": 1
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/psychologists
curl http://localhost:5000/api/psychologists?active_only=true
\`\`\`

---

#### `GET /api/psychologists/{id}`
Busca um psicólogo específico pelo ID.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Dr. Carlos Mendes",
    "crp": "06/123456",
    "specialty": "TCC",
    "hourly_rate": 200.0,
    "is_active": true
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/psychologists/1
\`\`\`

---

#### `POST /api/psychologists`
Cria um novo psicólogo no sistema.

**Request Body:**
\`\`\`json
{
  "user_id": 2,
  "name": "Dra. Ana Paula",
  "crp": "06/654321",
  "specialty": "Psicanálise",
  "themes": ["Relacionamentos", "Autoestima"],
  "hourly_rate": 180.0,
  "bio": "Psicanalista com formação na USP"
}
\`\`\`

**Validações:**
- `crp`: Formato XX/XXXXX obrigatório
- `hourly_rate`: Deve ser positivo

**Response (201):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Psicólogo criado com sucesso"
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X POST http://localhost:5000/api/psychologists \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "name": "Dra. Ana Paula",
    "crp": "06/654321",
    "specialty": "Psicanálise",
    "hourly_rate": 180.0
  }'
\`\`\`

---

#### `PUT /api/psychologists/{id}`
Atualiza os dados de um psicólogo.

**Request Body:**
\`\`\`json
{
  "specialty": "Terapia Sistêmica",
  "hourly_rate": 220.0,
  "is_active": true
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Psicólogo atualizado com sucesso"
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X PUT http://localhost:5000/api/psychologists/1 \
  -H "Content-Type: application/json" \
  -d '{"hourly_rate": 220.0}'
\`\`\`

---

#### `DELETE /api/psychologists/{id}`
Remove um psicólogo do sistema.

**Response:** `204 No Content`

---

#### `PATCH /api/psychologists/{id}/activate`
Ativa um psicólogo no sistema.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Psicólogo ativado com sucesso"
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X PATCH http://localhost:5000/api/psychologists/1/activate
\`\`\`

---

#### `PATCH /api/psychologists/{id}/deactivate`
Desativa um psicólogo no sistema.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Psicólogo desativado com sucesso"
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X PATCH http://localhost:5000/api/psychologists/1/deactivate
\`\`\`

---

### Clínicas

#### `GET /api/clinics`
Lista todas as clínicas cadastradas.

#### `GET /api/clinics/{id}`
Busca uma clínica específica pelo ID.

#### `POST /api/clinics`
Cria uma nova clínica.

**Request Body:**
\`\`\`json
{
  "user_id": 2,
  "name": "Clínica Bem-Estar",
  "address": "Rua das Flores, 123 - São Paulo/SP",
  "phone": "(11) 3456-7890",
  "email": "contato@bemespar.com"
}
\`\`\`

#### `PUT /api/clinics/{id}`
Atualiza os dados de uma clínica.

#### `DELETE /api/clinics/{id}`
Remove uma clínica do sistema.

---

### Disponibilidades

#### `GET /api/availabilities`
Lista todas as disponibilidades cadastradas.

**Query Parameters:**
- `psychologist_id` (int): Filtrar por psicólogo específico

**Exemplo:** `/api/availabilities?psychologist_id=1`

---

#### `GET /api/availabilities/{id}`
Busca uma disponibilidade específica pelo ID.

---

#### `GET /api/availabilities/psychologist/{psychologist_id}`
Lista todas as disponibilidades de um psicólogo específico.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "psychologist_id": 1,
        "day_of_week": 0,
        "start_time": "08:00:00",
        "end_time": "12:00:00",
        "is_active": true
      },
      {
        "id": 2,
        "psychologist_id": 1,
        "day_of_week": 1,
        "start_time": "14:00:00",
        "end_time": "18:00:00",
        "is_active": true
      }
    ],
    "count": 2
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/availabilities/psychologist/1
\`\`\`

---

#### `POST /api/availabilities`
Cria uma nova disponibilidade para um psicólogo.

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
- `day_of_week`: 0 (Segunda) a 6 (Domingo)
- `start_time`/`end_time`: Formato HH:MM
- `start_time` deve ser anterior a `end_time`
- Não pode haver sobreposição com disponibilidades existentes

**Response (201):**
\`\`\`json
{
  "success": true,
  "data": { ... },
  "message": "Disponibilidade criada com sucesso"
}
\`\`\`

**Possíveis Erros:**
- `404 Not Found`: Psicólogo não encontrado
- `409 Conflict`: Sobreposição de horários
- `400 Validation Error`: Dados inválidos

**Teste:**
\`\`\`bash
curl -X POST http://localhost:5000/api/availabilities \
  -H "Content-Type: application/json" \
  -d '{
    "psychologist_id": 1,
    "day_of_week": 2,
    "start_time": "14:00",
    "end_time": "18:00"
  }'
\`\`\`

---

#### `PUT /api/availabilities/{id}`
Atualiza uma disponibilidade existente.

**Request Body:**
\`\`\`json
{
  "start_time": "09:00",
  "end_time": "13:00",
  "is_active": true
}
\`\`\`

---

#### `DELETE /api/availabilities/{id}`
Remove uma disponibilidade do sistema.

---

#### `PATCH /api/availabilities/{id}/activate`
Ativa uma disponibilidade.

#### `PATCH /api/availabilities/{id}/deactivate`
Desativa uma disponibilidade.

---

### Consultas

#### `GET /api/appointments`
Lista todas as consultas agendadas.

**Query Parameters:**
- `patient_id` (int): Filtrar por paciente
- `psychologist_id` (int): Filtrar por psicólogo

**Exemplos:**
- `/api/appointments?patient_id=3`
- `/api/appointments?psychologist_id=1`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "patient_id": 3,
        "psychologist_id": 1,
        "date": "2025-12-01",
        "time": "14:00:00",
        "duration": 60,
        "status": "scheduled",
        "notes": "Primeira consulta",
        "created_at": "2025-11-30T10:00:00"
      }
    ],
    "count": 1
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl http://localhost:5000/api/appointments
curl http://localhost:5000/api/appointments?patient_id=3
\`\`\`

---

#### `GET /api/appointments/{id}`
Busca uma consulta específica pelo ID.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "patient_id": 3,
    "psychologist_id": 1,
    "date": "2025-12-01",
    "time": "14:00:00",
    "duration": 60,
    "status": "scheduled"
  }
}
\`\`\`

---

#### `POST /api/appointments`
Agenda uma nova consulta.

**Request Body:**
\`\`\`json
{
  "patient_id": 3,
  "psychologist_id": 1,
  "date": "2025-12-08",
  "time": "14:00",
  "duration": 60,
  "notes": "Consulta de acompanhamento"
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
    "id": 2,
    "patient_id": 3,
    "psychologist_id": 1,
    "date": "2025-12-08",
    "time": "14:00:00",
    "duration": 60,
    "status": "scheduled",
    "notes": "Consulta de acompanhamento"
  },
  "message": "Consulta agendada com sucesso"
}
\`\`\`

**Possíveis Erros:**
- `404 Not Found`: Paciente ou psicólogo não encontrado
- `409 Conflict`: Conflito de horário
- `422 Business Rule`: Psicólogo inativo ou sem disponibilidade

**Teste:**
\`\`\`bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 3,
    "psychologist_id": 1,
    "date": "2025-12-08",
    "time": "14:00",
    "duration": 60
  }'
\`\`\`

---

#### `DELETE /api/appointments/{id}`
Remove uma consulta do sistema.

**Response:** `204 No Content`

---

#### `PATCH /api/appointments/{id}/cancel`
Cancela uma consulta agendada.

**Request Body:**
\`\`\`json
{
  "cancellation_reason": "Imprevisto pessoal"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "cancelled",
    "cancellation_reason": "Imprevisto pessoal"
  },
  "message": "Consulta cancelada com sucesso"
}
\`\`\`

**Possíveis Erros:**
- `404 Not Found`: Consulta não encontrada
- `422 Business Rule`: Consulta já cancelada ou concluída

**Teste:**
\`\`\`bash
curl -X PATCH http://localhost:5000/api/appointments/1/cancel \
  -H "Content-Type: application/json" \
  -d '{"cancellation_reason": "Imprevisto pessoal"}'
\`\`\`

---

#### `PATCH /api/appointments/{id}/complete`
Marca uma consulta como concluída.

**Response (200):**
\`\`\`json
{
  "success": true,
  "data": {
    "id": 1,
    "status": "completed"
  },
  "message": "Consulta concluída com sucesso"
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X PATCH http://localhost:5000/api/appointments/1/complete
\`\`\`

---

#### `POST /api/appointments/available-slots`
Lista horários disponíveis para agendamento em uma data específica.

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
    "available_times": [
      "08:00",
      "08:15",
      "08:30",
      "09:00",
      "10:30",
      "11:00"
    ],
    "count": 6
  }
}
\`\`\`

**Teste:**
\`\`\`bash
curl -X POST http://localhost:5000/api/appointments/available-slots \
  -H "Content-Type: application/json" \
  -d '{
    "psychologist_id": 1,
    "date": "2025-12-08",
    "duration": 60
  }'
\`\`\`

---

### Leads

#### `GET /api/leads`
Lista todos os leads cadastrados.

#### `GET /api/leads/{id}`
Busca um lead específico pelo ID.

#### `POST /api/leads`
Cria um novo lead.

**Request Body:**
\`\`\`json
{
  "name": "Pedro Santos",
  "email": "pedro@email.com",
  "phone": "(11) 91234-5678",
  "source": "website",
  "notes": "Interesse em terapia de casal"
}
\`\`\`

#### `PUT /api/leads/{id}`
Atualiza os dados de um lead.

#### `DELETE /api/leads/{id}`
Remove um lead do sistema.

#### `PATCH /api/leads/{id}/contacted`
Marca um lead como contatado.

**Request Body:**
\`\`\`json
{
  "notes": "Ligação realizada, agendou visita"
}
\`\`\`

#### `PATCH /api/leads/{id}/lost`
Marca um lead como perdido.

**Request Body:**
\`\`\`json
{
  "reason": "Optou por outro serviço"
}
\`\`\`

#### `PATCH /api/leads/{id}/convert`
Converte um lead em paciente.

**Request Body:**
\`\`\`json
{
  "patient_id": 5
}
\`\`\`

**Possíveis Erros:**
- `422 Business Rule`: Lead já foi convertido

---

### Health Check

#### `GET /health`
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

**Teste:**
\`\`\`bash
curl http://localhost:5000/health
\`\`\`

---

## Códigos de Status HTTP

| Código | Nome | Significado | Quando Usar |
|--------|------|-------------|-------------|
| **200** | OK | Sucesso | GET, PUT, PATCH bem-sucedidos |
| **201** | Created | Recurso criado | POST bem-sucedido |
| **204** | No Content | Sucesso sem retorno | DELETE bem-sucedido |
| **400** | Bad Request | Dados inválidos | Validação falhou |
| **401** | Unauthorized | Não autenticado | Login inválido |
| **404** | Not Found | Recurso não existe | ID inexistente |
| **409** | Conflict | Conflito de recursos | Horário ocupado, email duplicado |
| **422** | Unprocessable Entity | Regra de negócio violada | Psicólogo inativo, data inválida |
| **500** | Internal Server Error | Erro no servidor | Exceção não tratada |

---

## Exemplos de Uso

### Fluxo Completo: Agendar uma Consulta

#### Passo 1: Listar psicólogos disponíveis
\`\`\`bash
curl http://localhost:5000/api/psychologists?active_only=true
\`\`\`

#### Passo 2: Verificar horários disponíveis
\`\`\`bash
curl -X POST http://localhost:5000/api/appointments/available-slots \
  -H "Content-Type: application/json" \
  -d '{
    "psychologist_id": 1,
    "date": "2025-12-10",
    "duration": 60
  }'
\`\`\`

#### Passo 3: Agendar a consulta
\`\`\`bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 3,
    "psychologist_id": 1,
    "date": "2025-12-10",
    "time": "14:00",
    "duration": 60,
    "notes": "Primeira consulta"
  }'
\`\`\`

#### Passo 4: Confirmar o agendamento
\`\`\`bash
curl http://localhost:5000/api/appointments/2
\`\`\`

---

### Fluxo: Gerenciar Disponibilidades

#### Ver disponibilidades do psicólogo
\`\`\`bash
curl http://localhost:5000/api/availabilities/psychologist/1
\`\`\`

#### Adicionar nova disponibilidade
\`\`\`bash
curl -X POST http://localhost:5000/api/availabilities \
  -H "Content-Type: application/json" \
  -d '{
    "psychologist_id": 1,
    "day_of_week": 3,
    "start_time": "13:00",
    "end_time": "17:00"
  }'
\`\`\`

#### Desativar disponibilidade
\`\`\`bash
curl -X PATCH http://localhost:5000/api/availabilities/3/deactivate
\`\`\`

---

## Conceitos Importantes

### Idempotência
- **GET, PUT, DELETE**: Idempotentes (chamar múltiplas vezes = mesmo resultado)
- **POST**: Não idempotente (cria novo recurso a cada chamada)

### Stateless
- Cada requisição é independente
- Servidor não mantém estado de sessão
- Cliente deve enviar todas as informações necessárias

### Códigos Semânticos
- Use o código HTTP correto para cada situação
- Facilita tratamento de erros no cliente
- Segue padrões REST universais

---

## Referências Adicionais

- **Documentação de Arquitetura**: `ARCHITECTURE.md`
- **Credenciais de Teste**: `CREDENCIAIS_TESTE.md`
- **Horários Disponíveis**: `HORARIOS_DISPONIVEIS.md`
- **Guia de Apresentação**: `APRESENTACAO.md`

---

## Suporte

Para dúvidas ou problemas com a API, consulte o código-fonte em:
- **Controllers**: `synapse/controllers/`
- **Services**: `synapse/services/`
- **Models**: `synapse/business_model/`
