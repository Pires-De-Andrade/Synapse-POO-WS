# Guia Completo de Testes da API - Synapse

## Como usar este guia
1. Inicie o servidor: `python main.py`
2. Base URL: `http://localhost:5000`
3. Headers padrão: `Content-Type: application/json`
4. Copie e cole os exemplos no Postman

---

## 1. AUTENTICAÇÃO

### 1.1 Login de Paciente
**POST** `/api/auth/login`

**Body:**
```json
{
  "email": "maria.silva@email.com",
  "password": "senha123"
}
```

**Explicação:** Autentica um paciente no sistema.

---

### 1.2 Login de Psicólogo
**POST** `/api/auth/login`

**Body:**
```json
{
  "email": "carlos.oliveira@psi.com",
  "password": "psi123"
}
```

**Explicação:** Autentica um psicólogo no sistema.

---

### 1.3 Login de Clínica
**POST** `/api/auth/login`

**Body:**
```json
{
  "email": "contato@clinicaexemplo.com",
  "password": "clinic123"
}
```

**Explicação:** Autentica uma clínica no sistema.

---

## 2. PACIENTES

### 2.1 Listar Todos os Pacientes
**GET** `/api/patients`

**Headers:** `Content-Type: application/json`

**Explicação:** Retorna lista de todos os pacientes cadastrados.

---

### 2.2 Buscar Paciente por ID
**GET** `/api/patients/3`

**Headers:** `Content-Type: application/json`

**Explicação:** Retorna dados de um paciente específico.

---

### 2.3 Criar Novo Paciente
**POST** `/api/patients`

**Body:**
```json
{
  "name": "João Silva",
  "email": "joao.silva@email.com",
  "phone": "(11) 98765-4321",
  "cpf": "123.456.789-00"
}
```

**Explicação:** Cria um novo paciente no sistema.

---

### 2.4 Atualizar Paciente
**PUT** `/api/patients/3`

**Body:**
```json
{
  "name": "Maria Silva Santos",
  "phone": "(11) 99999-8888"
}
```

**Explicação:** Atualiza dados de um paciente existente (todos campos opcionais).

---

### 2.5 Deletar Paciente
**DELETE** `/api/patients/3`

**Explicação:** Remove um paciente do sistema.

---

## 3. PSICÓLOGOS

### 3.1 Listar Todos os Psicólogos
**GET** `/api/psychologists`

**Headers:** `Content-Type: application/json`

**Explicação:** Retorna lista de todos os psicólogos cadastrados.

---

### 3.2 Listar Apenas Psicólogos Ativos
**GET** `/api/psychologists?active_only=true`

**Headers:** `Content-Type: application/json`

**Explicação:** Retorna apenas psicólogos com status ativo.

---

### 3.3 Buscar Psicólogo por ID
**GET** `/api/psychologists/1`

**Headers:** `Content-Type: application/json`

**Explicação:** Retorna dados de um psicólogo específico.

---

### 3.4 Criar Novo Psicólogo
**POST** `/api/psychologists`

**Body:**
```json
{
  "user_id": 2,
  "name": "Dr. Carlos Oliveira",
  "crp": "06/123456",
  "specialty": "Psicologia Clínica",
  "hourly_rate": 200.00,
  "themes": ["Ansiedade", "Depressão", "Relacionamentos"],
  "bio": "Psicólogo com 10 anos de experiência"
}
```

**Explicação:** Cria um novo psicólogo no sistema.

---

### 3.5 Atualizar Psicólogo
**PUT** `/api/psychologists/1`

**Body:**
```json
{
  "hourly_rate": 250.00,
  "bio": "Psicólogo com 15 anos de experiência"
}
```

**Explicação:** Atualiza dados de um psicólogo (todos campos opcionais).

---

### 3.6 Deletar Psicólogo
**DELETE** `/api/psychologists/1`

**Explicação:** Remove um psicólogo do sistema.

---

### 3.7 Ativar Psicólogo
**PATCH** `/api/psychologists/1/activate`

**Explicação:** Marca um psicólogo como ativo.

---

### 3.8 Desativar Psicólogo
**PATCH** `/api/psychologists/1/deactivate`

**Explicação:** Marca um psicólogo como inativo.

---

## 4. CONSULTAS/AGENDAMENTOS

### 4.1 Listar Todas as Consultas
**GET** `/api/appointments`

**Explicação:** Retorna lista de todos os agendamentos.

---

### 4.2 Filtrar Consultas por Paciente
**GET** `/api/appointments?patient_id=3`

**Explicação:** Retorna agendamentos de um paciente específico.

---

### 4.3 Filtrar Consultas por Psicólogo
**GET** `/api/appointments?psychologist_id=1`

**Explicação:** Retorna agendamentos de um psicólogo específico.

---

### 4.4 Buscar Consulta por ID
**GET** `/api/appointments/1`

**Explicação:** Retorna dados de uma consulta específica.

---

### 4.5 Verificar Horários Disponíveis
**POST** `/api/appointments/available-slots`

**Body:**
```json
{
  "psychologist_id": 1,
  "date": "2025-12-03",
  "duration": 60
}
```

**Explicação:** Lista horários disponíveis para uma data.

---

### 4.6 Criar Novo Agendamento
**POST** `/api/appointments`

**Body:**
```json
{
  "patient_id": 3,
  "psychologist_id": 1,
  "date": "2025-12-03",
  "time": "15:00",
  "duration": 60,
  "notes": "Primeira consulta"
}
```

**Explicação:** Cria um novo agendamento.

---

### 4.7 Cancelar Consulta
**PATCH** `/api/appointments/1/cancel`

**Body:**
```json
{
  "cancellation_reason": "Imprevisto pessoal"
}
```

**Explicação:** Cancela uma consulta.

---

### 4.8 Marcar Consulta como Concluída
**PATCH** `/api/appointments/1/complete`

**Explicação:** Marca uma consulta como realizada.

---

### 4.9 Deletar Consulta
**DELETE** `/api/appointments/1`

**Explicação:** Remove uma consulta do sistema.

---

## 5. DISPONIBILIDADES

### 5.1 Listar Todas as Disponibilidades
**GET** `/api/availabilities`

**Explicação:** Retorna todas as disponibilidades cadastradas.

---

### 5.2 Filtrar Disponibilidades por Psicólogo
**GET** `/api/availabilities?psychologist_id=1`

**Explicação:** Retorna disponibilidades de um psicólogo.

---

### 5.3 Buscar Disponibilidades de um Psicólogo
**GET** `/api/availabilities/psychologist/1`

**Explicação:** Retorna todas as disponibilidades de um psicólogo.

---

### 5.4 Buscar Disponibilidade por ID
**GET** `/api/availabilities/1`

**Explicação:** Retorna dados de uma disponibilidade específica.

---

### 5.5 Criar Nova Disponibilidade
**POST** `/api/availabilities`

**Body:**
```json
{
  "psychologist_id": 1,
  "day_of_week": 1,
  "start_time": "14:00",
  "end_time": "18:00"
}
```

**Explicação:** Cria um horário de disponibilidade (0 = Segunda, 6 = Domingo).

---

### 5.6 Atualizar Disponibilidade
**PUT** `/api/availabilities/1`

**Body:**
```json
{
  "start_time": "13:00",
  "end_time": "19:00"
}
```

**Explicação:** Atualiza horários de uma disponibilidade.

---

### 5.7 Deletar Disponibilidade
**DELETE** `/api/availabilities/1`

**Explicação:** Remove uma disponibilidade do sistema.

---

### 5.8 Ativar Disponibilidade
**PATCH** `/api/availabilities/1/activate`

**Explicação:** Ativa uma disponibilidade.

---

### 5.9 Desativar Disponibilidade
**PATCH** `/api/availabilities/1/deactivate`

**Explicação:** Desativa uma disponibilidade.

---

## 6. CLÍNICAS

### 6.1 Listar Todas as Clínicas
**GET** `/api/clinics`

**Explicação:** Retorna todas as clínicas cadastradas.

---

### 6.2 Buscar Clínica por ID
**GET** `/api/clinics/1`

**Explicação:** Retorna dados de uma clínica específica.

---

### 6.3 Criar Nova Clínica
**POST** `/api/clinics`

**Body:**
```json
{
  "user_id": 4,
  "name": "Clínica Saúde Mental",
  "address": "Rua Exemplo, 123",
  "phone": "(11) 3333-4444",
  "email": "contato@clinicasaude.com"
}
```

**Explicação:** Cria uma nova clínica no sistema.

---

### 6.4 Atualizar Clínica
**PUT** `/api/clinics/1`

**Body:**
```json
{
  "phone": "(11) 4444-5555",
  "address": "Rua Nova, 456"
}
```

**Explicação:** Atualiza dados de uma clínica.

---

### 6.5 Deletar Clínica
**DELETE** `/api/clinics/1`

**Explicação:** Remove uma clínica do sistema.

---

## 7. LEADS

### 7.1 Listar Todos os Leads
**GET** `/api/leads`

**Explicação:** Retorna lista de todos os leads.

---

### 7.2 Buscar Lead por ID
**GET** `/api/leads/1`

**Explicação:** Retorna dados de um lead específico.

---

### 7.3 Criar Novo Lead
**POST** `/api/leads`

**Body:**
```json
{
  "name": "Ana Costa",
  "email": "ana.costa@email.com",
  "phone": "(11) 97777-6666",
  "source": "Instagram",
  "notes": "Interessada em terapia para ansiedade"
}
```

**Explicação:** Cria um novo lead no sistema.

---

### 7.4 Atualizar Lead
**PUT** `/api/leads/1`

**Body:**
```json
{
  "phone": "(11) 98888-7777",
  "notes": "Contato realizado"
}
```

**Explicação:** Atualiza dados de um lead.

---

### 7.5 Deletar Lead
**DELETE** `/api/leads/1`

**Explicação:** Remove um lead do sistema.

---

### 7.6 Marcar Lead como Contatado
**PATCH** `/api/leads/1/contacted`

**Body:**
```json
{
  "notes": "Primeiro contato realizado por telefone"
}
```

**Explicação:** Atualiza o status do lead para contatado.

---

### 7.7 Marcar Lead como Perdido
**PATCH** `/api/leads/1/lost`

**Body:**
```json
{
  "reason": "Não respondeu após 3 tentativas"
}
```

**Explicação:** Marca lead como perdido.

---

### 7.8 Converter Lead em Paciente
**PATCH** `/api/leads/1/convert`

**Body:**
```json
{
  "patient_id": 5
}
```

**Explicação:** Converte o lead em paciente ativo.

---

## RESUMO DE ENDPOINTS

| Recurso | GET (Listar) | GET (ID) | POST (Criar) | PUT (Atualizar) | DELETE | PATCH (Outros) |
|---------|--------------|----------|--------------|------------------|--------|----------------|
| **Auth** | - | - | /login | - | - | - |
| **Patients** | /patients | /patients/:id | /patients | /patients/:id | /patients/:id | - |
| **Psychologists** | /psychologists | /psychologists/:id | /psychologists | /psychologists/:id | /psychologists/:id | /activate, /deactivate |
| **Appointments** | /appointments | /appointments/:id | /appointments | - | /appointments/:id | /cancel, /complete |
| **Availabilities** | /availabilities | /availabilities/:id | /availabilities | /availabilities/:id | /availabilities/:id | /activate, /deactivate |
| **Clinics** | /clinics | /clinics/:id | /clinics | /clinics/:id | /clinics/:id | - |
| **Leads** | /leads | /leads/:id | /leads | /leads/:id | /leads/:id | /contacted, /lost, /convert |

**Total de Endpoints: 48**

---

## DICAS PARA TESTES

1. **Sequência recomendada:**
   - Teste os GETs primeiro
   - Depois POSTs
   - Por último PUT, PATCH e DELETE
2. **IDs válidos no seeds.json:**
   - Paciente: 3  
   - Psicólogo: 1  
   - Disponibilidades: 1–5  
   - Consulta: 1  
3. **Dias da semana:**
   - 0 = Segunda  
   - 1 = Terça  
   - 2 = Quarta  
   - 3 = Quinta  
   - 4 = Sexta  
   - 5 = Sábado  
   - 6 = Domingo  
4. **Formato de datas:**
   - Data: `YYYY-MM-DD`
   - Hora: `HH:MM`

