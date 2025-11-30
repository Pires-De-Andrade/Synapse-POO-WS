# Synapse - Sistema de Agendamento de Consultas Psicológicas

Sistema web desenvolvido como projeto acadêmico para demonstrar conceitos de **Programação Orientada a Objetos (POO)** e **Engenharia de Software**.
O Synapse permite que pacientes agendem consultas com psicólogos, respeitando disponibilidades e horários configurados.

---

## Índice

* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Arquitetura e Padrões de Projeto](#arquitetura-e-padrões-de-projeto)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Como Executar](#como-executar)
* [Credenciais de Teste](#credenciais-de-teste)
* [Endpoints da API](#endpoints-da-api)
* [Conceitos de POO Aplicados](#conceitos-de-poo-aplicados)
* [Documentação Adicional](#documentação-adicional)
* [Funcionalidades Principais](#funcionalidades-principais)
* [Regras de Negócio](#regras-de-negócio)
* [Testes](#testes)
* [Desenvolvido por](#desenvolvido-por)
* [Licença](#licença)

---

## Tecnologias Utilizadas

### Backend

* **Python 3.x**
* **Flask**
* **Pydantic**
* **bcrypt**

### Frontend

* **HTML5**
* **CSS3**
* **JavaScript**
* **Jinja2**

### Persistência

* **In-Memory** – dicionários Python
* **JSON** – dados carregados de `seeds.json`

---

## Arquitetura e Padrões de Projeto

O projeto segue uma **arquitetura em camadas**, com separação clara de responsabilidades:

```
┌────────────────────────────┐
│ VIEWS (Frontend)           │  Templates HTML + JS
├────────────────────────────┤
│ CONTROLLERS (API)          │  Endpoints REST (Flask Blueprints)
├────────────────────────────┤
│ SERVICES                   │  Regras de negócio
├────────────────────────────┤
│ REPOSITORIES               │  Abstração de persistência
├────────────────────────────┤
│ BUSINESS MODELS            │  Entidades do domínio
└────────────────────────────┘
```

### Padrões de Projeto Implementados

1. **Repository Pattern**
2. **Dependency Injection**
3. **Factory Pattern**
4. **DTO Pattern** (Pydantic)
5. **Custom Exceptions**
6. **API Response Standardization**

### Princípios SOLID

* **S**ingle Responsibility
* **O**pen/Closed
* **L**iskov Substitution
* **I**nterface Segregation
* **D**ependency Inversion

---

## Estrutura do Projeto

```
synapse/
├── business_model/
│   ├── patient.py
│   ├── psychologist.py
│   ├── appointment.py
│   ├── availability.py
│   ├── clinic.py
│   ├── lead.py
│   └── user.py
│
├── repositories/
│   ├── abstract_repository.py
│   └── implementations/
│       ├── inmemory_patient_repository.py
│       ├── inmemory_psychologist_repository.py
│       ├── inmemory_appointment_repository.py
│       ├── inmemory_availability_repository.py
│       ├── inmemory_clinic_repository.py
│       ├── inmemory_lead_repository.py
│       └── inmemory_user_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── patient_service.py
│   ├── psychologist_service.py
│   ├── appointment_service.py
│   ├── availability_service.py
│   ├── clinic_service.py
│   ├── lead_service.py
│   └── seed_loader.py
│
├── controllers/
│   ├── auth_controller.py
│   ├── patient_controller.py
│   ├── psychologist_controller.py
│   ├── appointment_controller.py
│   ├── availability_controller.py
│   ├── clinic_controller.py
│   └── lead_controller.py
│
├── api/
│   ├── dtos.py
│   ├── exceptions.py
│   └── response.py
│
├── views/
│   ├── templates/
│   │   ├── index.html
│   │   ├── patient_login.html
│   │   ├── patient_booking.html
│   │   ├── psychologist_login.html
│   │   ├── psychologist_dashboard.html
│   │   ├── clinic_login.html
│   │   └── clinic_dashboard.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
└── seeds.json
```

---

## Como Executar

### 1. Pré-requisitos

* Python **3.8+**
* pip

### 2. Instalação

```bash
# Entre no diretório do projeto
cd synapse-project

# Instale as dependências
pip install -r requirements.txt
```

### 3. Executar o servidor

```bash
python main.py
```

Servidor disponível em:
**[http://localhost:5000](http://localhost:5000)**

### 4. Acessar a aplicação

* Página inicial: **[http://localhost:5000/](http://localhost:5000/)**
* Login Paciente: **/patient/login**
* Login Psicólogo: **/psychologist/login**
* Login Clínica: **/clinic/login**
* Health Check: **/health**

---

## Credenciais de Teste

### Paciente

* **Email:** [maria.silva@email.com](mailto:maria.silva@email.com)
* **Senha:** senha123

### Psicólogo

* **Email:** [carlos.souza@psi.com](mailto:carlos.souza@psi.com)
* **Senha:** psi123

### Clínica

* **Email:** [contato@clinicavida.com](mailto:contato@clinicavida.com)
* **Senha:** clinic123

---

## Endpoints da API

### Autenticação

```
POST /api/auth/login
Body: { "email": "...", "password": "..." }
```

---

### Pacientes

```
GET    /api/patients
GET    /api/patients/{id}
POST   /api/patients
PUT    /api/patients/{id}
DELETE /api/patients/{id}
```

### Psicólogos

```
GET    /api/psychologists
GET    /api/psychologists/{id}
POST   /api/psychologists
PUT    /api/psychologists/{id}
DELETE /api/psychologists/{id}
PATCH  /api/psychologists/{id}/activate
PATCH  /api/psychologists/{id}/deactivate
```

### Consultas

```
GET    /api/appointments
GET    /api/appointments/{id}
POST   /api/appointments
PUT    /api/appointments/{id}
DELETE /api/appointments/{id}
GET    /api/appointments/patient/{id}
GET    /api/appointments/psychologist/{id}
GET    /api/appointments/available-slots
PATCH  /api/appointments/{id}/cancel
PATCH  /api/appointments/{id}/complete
```

### Disponibilidades

```
GET    /api/availabilities
GET    /api/availabilities/{id}
POST   /api/availabilities
PUT    /api/availabilities/{id}
DELETE /api/availabilities/{id}
GET    /api/availabilities/psychologist/{id}
PATCH  /api/availabilities/{id}/activate
PATCH  /api/availabilities/{id}/deactivate
```

### Clínicas e Leads

```
GET /api/clinics
GET /api/leads
```

Documentação completa: **API_DOCS.md**

---

## Conceitos de POO Aplicados

### Encapsulamento

* Atributos privados
* Validações internas nas entidades

### Herança

* `AbstractRepository` como superclasse
* Hierarquia de exceções

### Polimorfismo

* Repositórios intercambiáveis
* Services aceitam qualquer implementação

### Abstração

* Interfaces de repositório
* DTOs simplificam validação e transporte

### Composição

* Services utilizam múltiplos repositórios
* Entidades compostas entre si

---

## Documentação Adicional

* **API_DOCS.md** – Detalhamento dos endpoints
* **ARCHITECTURE.md** – Arquitetura expandida
* **CREDENCIAIS_TESTE.md** – Dados para testes
* **HORARIOS_DISPONIVEIS.md** – Lógica de geração
* **APRESENTACAO.md** – Roteiro da apresentação

---

## Funcionalidades Principais

### Pacientes

* Agendamento de consultas
* Consulta de horários disponíveis
* Histórico de consultas

### Psicólogos

* Gestão de disponibilidades
* Dashboard
* Conclusão e cancelamento de consultas

### Clínicas

* Gestão de psicólogos
* Relatórios operacionais

---

## Regras de Negócio

* Slots de **15 minutos**
* Detecção de conflitos de horário
* Status: *scheduled*, *completed*, *canceled*
* Ativação/desativação de psicólogos
* Disponibilidades vinculadas a datas específicas

---

## Testes

Fluxo sugerido:

1. Login como paciente
2. Escolher psicólogo
3. Selecionar data
4. Escolher horário disponível
5. Confirmar
6. Login como psicólogo para visualizar a consulta

---

## Desenvolvido por

Projeto acadêmico — Engenharia de Software
Tecnologias: **Python**, **Flask**, **Pydantic**, **Jinja2**
Ano: **2025**

---

## Licença

Projeto acadêmico para fins educacionais.
