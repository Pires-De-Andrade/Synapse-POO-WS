"""
Exceções customizadas para a API Synapse.
Permite tratamento de erros específico e respostas HTTP padronizadas.
"""

class SynapseException(Exception):
    """Exceção base para todas as exceções do Synapse."""
    
    def __init__(self, message: str, code: str = "SYNAPSE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundError(SynapseException):
    """Exceção lançada quando um recurso não é encontrado."""
    
    def __init__(self, resource: str, resource_id: int = None):
        self.resource = resource
        self.resource_id = resource_id
        message = f"{resource} não encontrado(a)"
        if resource_id:
            message = f"{resource} com ID {resource_id} não encontrado(a)"
        super().__init__(message, code="NOT_FOUND")


class ValidationError(SynapseException):
    """Exceção lançada quando dados de entrada são inválidos."""
    
    def __init__(self, message: str, field: str = None):
        self.field = field
        if field:
            message = f"Campo '{field}': {message}"
        super().__init__(message, code="VALIDATION_ERROR")


class ConflictError(SynapseException):
    """Exceção lançada quando há conflito de recursos (ex: horário já ocupado)."""
    
    def __init__(self, message: str):
        super().__init__(message, code="CONFLICT")


class BusinessRuleError(SynapseException):
    """Exceção lançada quando uma regra de negócio é violada."""
    
    def __init__(self, message: str):
        super().__init__(message, code="BUSINESS_RULE_VIOLATION")
