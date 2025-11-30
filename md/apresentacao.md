# ROTEIRO DE APRESENTAÇÃO - SYNAPSE
## Sistema de Agendamento de Consultas Psicológicas

**Tempo total:** 30 minutos  
**Equipe:** 6 pessoas  
**Distribuição:** ~5 minutos por pessoa

---

## 🎯 ESTRUTURA DA APRESENTAÇÃO

### [0-3min] INTEGRANTE 1: Abertura + Visão Geral
**Tipo:** EXPLICAÇÃO rápida

**O que dizer:**
- "Desenvolvemos o Synapse, um sistema completo de agendamento de consultas psicológicas"
- "É um projeto acadêmico aplicando POO e Engenharia de Software na prática"
- "Backend em Python/Flask + Frontend HTML/CSS/JS"
- "Demonstra arquitetura em camadas, padrões de projeto e API REST completa"

**Mostrar na tela:**
- Estrutura de pastas do projeto (`synapse/`)
- Destacar: `business_model/`, `repositories/`, `services/`, `controllers/`, `api/`

**Transição:**
- "Vamos começar mostrando a arquitetura e API REST, que são os pontos principais"

---

### [3-8min] INTEGRANTE 2: API REST - Parte 1 [ESSENCIAL]
**Tipo:** DEMONSTRAÇÃO PRÁTICA

**O que fazer:**
1. Abrir arquivo `API_DOCS.md`
2. Mostrar estrutura de resposta padronizada:
   \`\`\`json
   {
     "success": true/false,
     "data": {...},
     "error": {...}
   }
   \`\`\`

3. **DEMONSTRAR NO POSTMAN/INSOMNIA (ou curl):**

   **GET** - Listar psicólogos:
   \`\`\`
   GET http://localhost:5000/api/psychologists
   \`\`\`
   - Mostrar resposta JSON com lista de psicólogos
   - Apontar: `id`, `name`, `crp`, `specialty`, `hourly_rate`

   **GET** - Buscar psicólogo específico:
   \`\`\`
   GET http://localhost:5000/api/psychologists/1
   \`\`\`
   - Mostrar dados detalhados de um psicólogo

**O que explicar:**
- "Todos os endpoints seguem padrão RESTful"
- "Sempre retornamos JSON padronizado com success, data e message/error"
- "Códigos HTTP semânticos: 200 OK, 201 Created, 404 Not Found, 409 Conflict"

---

### [8-14min] INTEGRANTE 3: API REST - Parte 2 [ESSENCIAL]
**Tipo:** DEMONSTRAÇÃO PRÁTICA

**O que fazer:**

1. **POST** - Criar novo paciente:
   \`\`\`
   POST http://localhost:5000/api/patients
   Content-Type: application/json
   
   {
     "name": "Carlos Mendes",
     "email": "carlos@email.com",
     "phone": "(11) 99999-8888",
     "cpf": "111.222.333-44"
   }
   \`\`\`
   - Mostrar resposta de sucesso com `201 Created`
   - Apontar validações: email válido, telefone mínimo 8 chars

2. **POST** - Buscar horários disponíveis:
   \`\`\`
   POST http://localhost:5000/api/appointments/available-slots
   
   {
     "psychologist_id": 1,
     "date": "2025-12-08",
     "duration": 60
   }
   \`\`\`
   - Mostrar lista de horários: `["08:00", "08:15", "09:00", ...]`
   - Explicar: "Sistema calcula automaticamente baseado nas disponibilidades e consultas existentes"

3. **POST** - Agendar consulta:
   \`\`\`
   POST http://localhost:5000/api/appointments
   
   {
     "patient_id": 1,
     "psychologist_id": 1,
     "date": "2025-12-08",
     "time": "14:00",
     "duration": 60,
     "notes": "Primeira consulta"
   }
   \`\`\`
   - Mostrar sucesso
   
4. **Provocar ERRO** - Tentar agendar no mesmo horário:
   - Repetir mesma requisição
   - Mostrar erro 409 Conflict: "Já existe consulta agendada neste horário"

**O que explicar:**
- "API valida todas as regras de negócio: disponibilidade, conflitos, datas futuras"
- "Erros personalizados com códigos específicos facilitam debugging"

---

### [14-19min] INTEGRANTE 4: POO - Classes e Arquitetura [ESSENCIAL]
**Tipo:** EXPLICAÇÃO + código

**O que mostrar:**

1. **Abrir:** `synapse/business_model/appointment.py`
   - Mostrar classe `Appointment`:
     \`\`\`python
     class Appointment:
         def __init__(self, patient_id, psychologist_id, date, time, ...):
             self.patient_id = patient_id
             self.status = "scheduled"
             
         def cancel(self, reason=None):
             self.status = "cancelled"
             self.cancelled_at = datetime.now()
             
         def complete(self):
             if self.status in ['scheduled', 'confirmed']:
                 self.status = 'completed'
     \`\`\`
   
   - **Destacar:**
     - Atributos: `patient_id`, `psychologist_id`, `date`, `time`, `status`
     - Métodos de negócio: `cancel()`, `complete()`, `reschedule()`
     - Encapsulamento: estado interno controlado por métodos

2. **Mostrar diagrama conceitual** (desenhar ou mostrar):
   \`\`\`
   Patient ──────┐
                 │
                 ├──> Appointment
                 │
   Psychologist ─┘
        │
        └──> Availability (dia da semana + horário)
   \`\`\`

3. **Abrir:** `synapse/business_model/patient.py`
   - Mostrar validações:
     \`\`\`python
     def validate_email(self):
         return "@" in self.email and "." in self.email
     
     def validate_phone(self):
         return len(self.phone) >= 8
     \`\`\`

**O que explicar:**
- "Cada entidade tem sua própria classe com responsabilidades claras"
- "Métodos encapsulam comportamento (não manipulamos status diretamente)"
- "Validações no modelo garantem consistência dos dados"
- "Relacionamentos: Appointment conecta Patient e Psychologist"

---

### [19-24min] INTEGRANTE 5: Padrões de Projeto [ESSENCIAL]
**Tipo:** EXPLICAÇÃO + código

**O que mostrar:**

1. **Repository Pattern**
   
   **Abrir:** `synapse/repositories/interfaces/abstract_repository.py`
   \`\`\`python
   class AbstractRepository(ABC, Generic[T]):
       @abstractmethod
       def add(self, entity: T) -> None: ...
       
       @abstractmethod
       def get(self, entity_id: int) -> Optional[T]: ...
       
       @abstractmethod
       def all(self) -> List[T]: ...
   \`\`\`
   
   - Explicar: "Interface abstrata define contrato"
   - "Implementações concretas (in-memory, SQL) são intercambiáveis"

2. **Dependency Injection**
   
   **Abrir:** `synapse/services/appointment_service.py` (linha 18-25)
   \`\`\`python
   class AppointmentService:
       def __init__(self, appointment_repository, 
                    patient_repository,
                    psychologist_repository,
                    availability_repository):
           self.appointment_repository = appointment_repository
   \`\`\`
   
   - Explicar: "Service recebe repositórios prontos"
   - "Facilita testes: podemos injetar mocks"
   - "Reduz acoplamento: Service não sabe se é in-memory ou SQL"

3. **Custom Exceptions**
   
   **Abrir:** `synapse/api/exceptions.py`
   \`\`\`python
   class NotFoundError(SynapseException): ...
   class ValidationError(SynapseException): ...
   class ConflictError(SynapseException): ...
   class BusinessRuleError(SynapseException): ...
   \`\`\`
   
   - Explicar: "Hierarquia de erros específicos do domínio"
   - "Cada tipo mapeia para código HTTP apropriado"

4. **DTO Pattern**
   
   Mostrar rapidamente `synapse/api/dto.py`:
   \`\`\`python
   class AppointmentCreateDTO(BaseModel):
       patient_id: int
       psychologist_id: int
       date: str
       time: str
       duration: int = 60
       
       @field_validator('date')
       def date_must_be_future(cls, v):
           # validação automática
   \`\`\`

**O que explicar:**
- "Repository: abstrai persistência (facilmente mudamos de in-memory para PostgreSQL)"
- "Dependency Injection: baixo acoplamento, alta testabilidade"
- "Exceptions: erros claros e tratamento específico"
- "DTOs com Pydantic: validação automática de entrada"

---

### [24-28min] INTEGRANTE 6: Arquitetura em Camadas + Frontend
**Tipo:** EXPLICAÇÃO + demonstração rápida

**O que mostrar:**

1. **Arquitetura em camadas** (desenhar ou mostrar diagrama):
   \`\`\`
   CLIENTE (Browser)
        ↓
   CONTROLLERS (/api/...)
        ↓
   SERVICES (lógica de negócio)
        ↓
   REPOSITORIES (persistência)
        ↓
   BUSINESS MODELS (entidades)
   \`\`\`

2. **Fluxo de uma requisição:**
   \`\`\`
   POST /api/appointments
   ↓
   appointment_controller.py
     ├─ Valida DTO (Pydantic)
     └─ Chama appointment_service.schedule_appointment()
   ↓
   appointment_service.py
     ├─ Busca patient (patient_repository)
     ├─ Busca psychologist (psychologist_repository)
     ├─ Verifica disponibilidade
     ├─ Checa conflitos
     └─ Cria Appointment
   ↓
   appointment_repository.add(entity)
   ↓
   Retorna JSON padronizado
   \`\`\`

3. **[SE HOUVER TEMPO] Mostrar frontend rapidamente:**
   - Abrir `http://localhost:5000` no navegador
   - Fazer login como paciente: `maria@email.com` / `senha123`
   - Navegar até agendamento
   - Mostrar interface de seleção de psicólogo e data
   - "Frontend consome a API REST que demonstramos"

**O que explicar:**
- "Separação clara de responsabilidades em cada camada"
- "Controller não tem lógica de negócio, só delega"
- "Service orquestra repositórios e aplica regras"
- "Repository não sabe nada de HTTP ou validação"
- "Princípios SOLID aplicados: cada camada tem uma responsabilidade"

---

## 🔥 POSSÍVEIS PERGUNTAS DO PROFESSOR + RESPOSTAS

### Sobre API:
**P: "Por que usar API REST e não outro tipo?"**
**R:** "REST é stateless, usa protocolo HTTP padrão, facilita integração com diferentes clientes (web, mobile, desktop) e segue convenções amplamente adotadas. É ideal para sistemas distribuídos."

**P: "Como você garante que os dados estão corretos?"**
**R:** "Temos 3 camadas de validação: DTOs com Pydantic (formato e tipo), validações no modelo (email, telefone), e regras de negócio no Service (disponibilidade, conflitos)."

### Sobre POO:
**P: "Quais princípios SOLID foram aplicados?"**
**R:** 
- **S**: Cada classe tem uma responsabilidade (Patient cuida de dados do paciente, AppointmentService de lógica de agendamento)
- **O**: Podemos adicionar novos repositories sem modificar código existente
- **L**: Qualquer implementação de AbstractRepository pode substituir outra
- **I**: Interface mínima no AbstractRepository
- **D**: Services dependem de interfaces, não implementações concretas

**P: "Por que separar em tantas classes?"**
**R:** "Baixo acoplamento e alta coesão. Se precisarmos mudar a persistência de in-memory para PostgreSQL, só alteramos o repository. Controller e Service ficam intactos."

### Sobre Engenharia de Software:
**P: "Como seria migrar de in-memory para banco real?"**
**R:** "Criar nova classe SQLAppointmentRepository implementando AbstractRepository, injetar no Service no lugar do InMemory. Zero mudanças em Controller e Service. Isso é o poder do Repository Pattern."

**P: "Como você testaria esse sistema?"**
**R:** "Testes unitários dos Services injetando repositories mockados, testes de integração chamando os endpoints da API, testes de modelo validando regras de negócio nas entidades."

**P: "E se dois usuários tentarem agendar o mesmo horário simultaneamente?"**
**R:** "Atualmente o sistema valida conflitos antes de criar. Em produção, usaríamos transações no banco de dados ou locks otimistas para garantir atomicidade."

### Sobre o Projeto:
**P: "Qual foi a maior dificuldade?"**
**R:** "Calcular horários disponíveis considerando dia da semana, disponibilidades do psicólogo e consultas já agendadas. Requer coordenação entre 3 repositórios diferentes."

**P: "O que vocês aprenderem fazendo isso?"**
**R:** "A importância de abstrações bem definidas. Quando fizemos refatorações, percebemos que camadas bem separadas facilitam muito manutenção e extensão do código."

---

## ✅ CHECKLIST PRÉ-APRESENTAÇÃO

### Preparar:
- [ ] Servidor rodando: `python main.py` (porta 5000)
- [ ] Postman/Insomnia com requisições prontas (GET, POST examples)
- [ ] VSCode aberto com arquivos-chave em abas:
  - `API_DOCS.md`
  - `synapse/business_model/appointment.py`
  - `synapse/services/appointment_service.py`
  - `synapse/repositories/interfaces/abstract_repository.py`
  - `synapse/api/exceptions.py`
- [ ] Navegador com `http://localhost:5000` aberto
- [ ] Credenciais de teste anotadas (maria@email.com / senha123)

### Durante apresentação:
- [ ] Falar devagar e claro (professor precisa entender conceitos)
- [ ] Apontar na tela o que está sendo explicado
- [ ] SEMPRE mostrar código + resultado (não só teoria)
- [ ] Fazer transições claras entre integrantes

### Dicas de ouro:
1. **Foco em DEMONSTRAR, não só explicar**
2. **Provocar erros propositalmente** mostra que você entende validações
3. **Relacionar com teoria:** "Isso aqui é o princípio X que vimos na aula Y"
4. **Ter resposta pronta para "por que fizeram assim?"**

---

## 📊 PRIORIZAÇÃO (se faltar tempo)

### OBRIGATÓRIO (não pule):
1. Demonstração GET/POST na API (Integrantes 2 e 3)
2. Classes principais e métodos (Integrante 4)
3. Repository Pattern e Dependency Injection (Integrante 5)
4. Arquitetura em camadas (Integrante 6)

### PODE CORTAR:
- Frontend (só mencionar que existe)
- Leads e Clínicas (focar em Patient/Psychologist/Appointment)
- Detalhes de todos os endpoints (mostrar só os principais)

### SE SOBRAR TEMPO:
- Mostrar arquivo `seeds.json` (dados de teste)
- Explicar como converter date/time (métodos `from_dict`, `to_dict`)
- Demonstrar cancelamento de consulta (PATCH)

---

## 🎬 ENCERRAMENTO (últimos 2 minutos)

**Qualquer integrante:**

"Em resumo, o Synapse demonstra:
- ✅ API REST completa e funcional com validações robustas
- ✅ POO aplicada: classes, encapsulamento, herança, polimorfismo
- ✅ Padrões de projeto: Repository, Dependency Injection, Factory, DTO
- ✅ Arquitetura em camadas respeitando SOLID
- ✅ Código organizado, extensível e preparado para crescer

O projeto está pronto para receber novas funcionalidades sem quebrar o existente. É isso que engenharia de software ensina: código sustentável."

**Agradecer e abrir para perguntas.**

---

## 💡 DICA FINAL

**Mostre CONFIANÇA.** Vocês construíram um sistema completo e bem arquitetado. Não é só "um trabalho de faculdade", é um exemplo real de como software profissional deve ser organizado.

Boa sorte! 🚀
