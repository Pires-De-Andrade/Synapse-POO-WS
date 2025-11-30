# Synapse - Sistema de Agendamento de Consultas Psicológicas

Sistema web desenvolvido como projeto acadêmico para demonstrar conceitos de **Programação Orientada a Objetos (POO)** e **Engenharia de Software**. O Synapse permite que pacientes agendem consultas com psicólogos, respeitando disponibilidades e horários configurados.

## Índice

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura e Padrões de Projeto](#arquitetura-e-padrões-de-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Credenciais de Teste](#credenciais-de-teste)
- [Endpoints da API](#endpoints-da-api)
- [Conceitos de POO Aplicados](#conceitos-de-poo-aplicados)
- [Documentação Adicional](#documentação-adicional)

---

## Tecnologias Utilizadas

### Backend
- **Python 3.x** - Linguagem de programação
- **Flask** - Framework web minimalista
- **Pydantic** - Validação de dados e DTOs
- **bcrypt** - Criptografia de senhas

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização
- **JavaScript** - Interatividade
- **Jinja2** - Template engine

### Persistência
- **In-Memory** - Dados em dicionários Python (facilmente substituível por banco de dados real)
- **JSON** - Dados iniciais carregados de `seeds.json`

---

## Arquitetura e Padrões de Projeto

O projeto segue uma **arquitetura em camadas** com clara separação de responsabilidades:

\`\`\`
┌─────────────────────────┐
│   VIEWS (Frontend)      │  Templates HTML + JavaScript
├─────────────────────────┤
│   CONTROLLERS (API)     │  Endpoints REST com Flask Blueprints
├─────────────────────────┤
│   SERVICES              │  Regras de negócio e orquestração
├─────────────────────────┤
│   REPOSITORIES          │  Abstração de persistência
├─────────────────────────┤
│   BUSINESS MODELS       │  Entidades do domínio
└─────────────────────────┘
\`\`\`

### Padrões de Projeto Implementados

1. **Repository Pattern** - Abstração da camada de persistência
   - Interface `AbstractRepository` define contrato
   - Implementações `InMemory*Repository` para testes/desenvolvimento
   - Fácil substituição por repositórios com banco de dados real

2. **Dependency Injection** - Serviços recebem repositórios via construtor
   - Baixo acoplamento entre camadas
   - Facilita testes unitários

3. **Factory Pattern** - Métodos `from_dict()` e `to_dict()` nas entidades
   - Conversão entre objetos e dicionários
   - Serialização/deserialização consistente

4. **DTO Pattern** - Data Transfer Objects com Pydantic
   - Validação automática de entrada
   - Documentação de contratos da API

5. **Custom Exceptions** - Hierarquia de exceções específicas do domínio
   - `EntityNotFoundException`
   - `InvalidDataException`
   - `ConflictException`

6. **API Response Standardization** - Formato consistente de respostas
   - `ApiResponse.success()` e `ApiResponse.error()`
   - Mensagens padronizadas

### Princípios SOLID

- **S**ingle Responsibility - Cada classe tem uma única responsabilidade
- **O**pen/Closed - Extensível sem modificar código existente
- **L**iskov Substitution - Repositórios são intercambiáveis
- **I**nterface Segregation - AbstractRepository define apenas métodos essenciais
- **D**ependency Inversion - Dependências de abstrações, não implementações concretas

---

## Estrutura do Projeto

\`\`\`
synapse/
├── business_model/          # Entidades do domínio
│   ├── patient.py          # Entidade Paciente
│   ├── psychologist.py     # Entidade Psicólogo
│   ├── appointment.py      # Entidade Consulta
│   ├── availability.py     # Entidade Disponibilidade
│   ├── clinic.py           # Entidade Clínica
│   ├── lead.py             # Entidade Lead
│   └── user.py             # Entidade Usuário
│
├── repositories/            # Camada de persistência
│   ├── abstract_repository.py           # Interface base
│   └── implementations/
│       ├── inmemory_patient_repository.py
│       ├── inmemory_psychologist_repository.py
│       ├── inmemory_appointment_repository.py
│       ├── inmemory_availability_repository.py
│       ├── inmemory_clinic_repository.py
│       ├── inmemory_lead_repository.py
│       └── inmemory_user_repository.py
│
├── services/                # Lógica de negócio
│   ├── auth_service.py     # Autenticação
│   ├── patient_service.py  # Gestão de pacientes
│   ├── psychologist_service.py  # Gestão de psicólogos
│   ├── appointment_service.py   # Agendamento de consultas
│   ├── availability_service.py  # Gestão de disponibilidades
│   ├── clinic_service.py   # Gestão de clínicas
│   ├── lead_service.py     # Gestão de leads
│   └── seed_loader.py      # Carregamento de dados iniciais
│
├── controllers/             # Endpoints da API REST
│   ├── auth_controller.py
│   ├── patient_controller.py
│   ├── psychologist_controller.py
│   ├── appointment_controller.py
│   ├── availability_controller.py
│   ├── clinic_controller.py
│   └── lead_controller.py
│
├── api/                     # DTOs e componentes da API
│   ├── dtos.py             # Data Transfer Objects (Pydantic)
│   ├── exceptions.py       # Exceções customizadas
│   └── response.py         # Padronização de respostas
│
├── views/                   # Interface Web
│   ├── templates/          # Templates HTML (Jinja2)
│   │   ├── index.html
│   │   ├── patient_login.html
│   │   ├── patient_booking.html
│   │   ├── psychologist_login.html
│   │   ├── psychologist_dashboard.html
│   │   ├── clinic_login.html
│   │   └── clinic_dashboard.html
│   └── static/             # CSS, JavaScript, imagens
│       ├── css/
│       ├── js/
│       └── img/
│
└── seeds.json              # Dados iniciais (pacientes, psicólogos, consultas)
\`\`\`

---

## Como Executar

### 1. Pré-requisitos

- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### 2. Instalação

\`\`\`bash
# Clone ou baixe o projeto
cd synapse-project

# Instale as dependências
pip install -r requirements.txt
\`\`\`

### 3. Executar o servidor

\`\`\`bash
python main.py
\`\`\`

O servidor estará disponível em: **http://localhost:5000**

### 4. Acessar a aplicação

- **Página inicial**: http://localhost:5000/
- **Login Paciente**: http://localhost:5000/patient/login
- **Login Psicólogo**: http://localhost:5000/psychologist/login
- **Login Clínica**: http://localhost:5000/clinic/login
- **Health Check API**: http://localhost:5000/health

---

## Credenciais de Teste

Use estas credenciais para testar o sistema:

### Paciente
- **Email**: `maria.silva@email.com`
- **Senha**: `senha123`

### Psicólogo
- **Email**: `carlos.souza@psi.com`
- **Senha**: `psi123`

### Clínica
- **Email**: `contato@clinicavida.com`
- **Senha**: `clinic123`

---

## Endpoints da API

### Autenticação

\`\`\`http
POST /api/auth/login
Body: { "email": "...", "password": "..." }
Response: { "success": true, "data": { "user": {...}, "token": "..." } }
\`\`\`

### Pacientes

\`\`\`http
GET    /api/patients           # Listar todos
GET    /api/patients/{id}      # Buscar por ID
POST   /api/patients           # Criar novo
PUT    /api/patients/{id}      # Atualizar
DELETE /api/patients/{id}      # Deletar
\`\`\`

### Psicólogos

\`\`\`http
GET    /api/psychologists           # Listar todos
GET    /api/psychologists/{id}      # Buscar por ID
POST   /api/psychologists           # Criar novo
PUT    /api/psychologists/{id}      # Atualizar
DELETE /api/psychologists/{id}      # Deletar
PATCH  /api/psychologists/{id}/activate    # Ativar
PATCH  /api/psychologists/{id}/deactivate  # Desativar
\`\`\`

### Consultas

\`\`\`http
GET    /api/appointments                    # Listar todas
GET    /api/appointments/{id}               # Buscar por ID
POST   /api/appointments                    # Criar agendamento
PUT    /api/appointments/{id}               # Atualizar
DELETE /api/appointments/{id}               # Deletar
GET    /api/appointments/patient/{id}       # Consultas do paciente
GET    /api/appointments/psychologist/{id}  # Consultas do psicólogo
GET    /api/appointments/available-slots    # Horários disponíveis
PATCH  /api/appointments/{id}/cancel        # Cancelar consulta
PATCH  /api/appointments/{id}/complete      # Marcar como concluída
\`\`\`

### Disponibilidades

\`\`\`http
GET    /api/availabilities                    # Listar todas
GET    /api/availabilities/{id}               # Buscar por ID
POST   /api/availabilities                    # Criar nova
PUT    /api/availabilities/{id}               # Atualizar
DELETE /api/availabilities/{id}               # Deletar
GET    /api/availabilities/psychologist/{id}  # Do psicólogo
PATCH  /api/availabilities/{id}/activate      # Ativar
PATCH  /api/availabilities/{id}/deactivate    # Desativar
\`\`\`

### Clínicas e Leads

\`\`\`http
GET    /api/clinics      # Gestão de clínicas
GET    /api/leads        # Gestão de leads
\`\`\`

Documentação completa: **[API_DOCS.md](API_DOCS.md)**

---

## Conceitos de POO Aplicados

### 1. Encapsulamento
- Atributos privados nas entidades
- Getters e setters controlados
- Validação interna de estados

### 2. Herança
- `AbstractRepository` como classe base
- Hierarquia de exceções customizadas
- Reutilização de código entre repositórios

### 3. Polimorfismo
- Repositories intercambiáveis através da interface
- Services aceitam qualquer implementação de repository
- Métodos abstratos implementados de formas específicas

### 4. Abstração
- Interface `AbstractRepository` esconde detalhes de implementação
- Services isolam regras de negócio
- DTOs abstraem validações complexas

### 5. Composição
- Services compõem múltiplos repositories
- Entidades compõem outras entidades (Appointment tem Patient e Psychologist)
- Controllers compõem services

---

## Documentação Adicional

- **[API_DOCS.md](API_DOCS.md)** - Documentação completa da API REST
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura detalhada e decisões de design
- **[CREDENCIAIS_TESTE.md](CREDENCIAIS_TESTE.md)** - Credenciais para testes
- **[HORARIOS_DISPONIVEIS.md](HORARIOS_DISPONIVEIS.md)** - Documentação de horários
- **[APRESENTACAO.md](APRESENTACAO.md)** - Roteiro para apresentação acadêmica

---

## Funcionalidades Principais

### Para Pacientes
- Login e autenticação
- Visualização de psicólogos disponíveis
- Seleção de data e horário
- Agendamento de consultas
- Visualização de consultas agendadas

### Para Psicólogos
- Login e dashboard personalizado
- Gestão de disponibilidades por dia da semana
- Visualização de consultas agendadas
- Marcação de consultas como concluídas

### Para Clínicas
- Gestão de psicólogos associados
- Visualização de agendamentos
- Relatórios de consultas

### Regras de Negócio
- Validação de disponibilidade antes de agendar
- Verificação de conflitos de horário
- Slots de 15 em 15 minutos
- Cálculo automático de horários disponíveis
- Status de consultas (agendada, cancelada, concluída)
- Sistema de ativação/desativação de psicólogos e disponibilidades

---

## Testes

Para executar testes manuais, use as credenciais de teste fornecidas e:

1. Faça login como paciente
2. Selecione um psicólogo
3. Escolha uma data futura
4. Selecione um horário disponível
5. Confirme o agendamento
6. Faça login como psicólogo para visualizar a consulta

---

## Desenvolvido por

Projeto acadêmico - Engenharia de Software

**Tecnologias**: Python, Flask, Pydantic, Jinja2

**Ano**: 2025

---

## Licença

Projeto acadêmico para fins educacionais.
