# Plano de Implementação - Synapse

## Fase 1: Estrutura Base
- Definição e criação de todas as pastas-camadas no projeto
- Inclui: __init__.py, main.py, settings.py, seeds JSON
- Entregas: estrutura navegável e documentação

## Fase 2: Persistência
- Criação das interfaces de repositório (Repository Pattern)
- Implementação de repos in-memory (usando arquivos JSON/listas)
- Entrega: repositórios testáveis com seed data

## Fase 3: Modelos & Entidades
- Implementação das entidades (Patient, Psychologist, etc.)
- Métodos de validação, conversão e regras de negócio
- Entrega: business_model completo

## Fase 4: Services e Lógica
- Services principais: AppointmentService, NotificationService, AgentService
- Validações; notificações simuladas
- Entrega: regras core e integração entre entidades

## Fase 5: API REST
- Implementação dos controllers e rotas no Flask
- DTOs Pydantic para entrada/saída
- Documentação dos endpoints
- Entregas: endpoints completos e testáveis

## Fase 6: Testes
- Testes unitários dos serviços
- Testes de integração da API
- Entrega: scripts de teste cobrindo regras principais

## Fase 7: Frontend (Posterior)
- Páginas HTML/CSS puro (landing, login, menus, dashboard)
- Blocos de login separados para cada perfil
- Integração visual com backend 
- Entregas: telas de navegação, login funcional mock

## Critérios de Aprovação
- Pastas e camadas seguem padrão SRP, DIP
- Todas as regras core funcionando
- API totalmente acessível via seed users
- Testes mínimos de ponta a ponta
- Frontend ilustrativo integrando fluxos principais
