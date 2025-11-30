"""
Classe ApiResponse para padronização de respostas da API.
Garante formato consistente em todas as respostas HTTP.
"""

from typing import Any, Optional, List, Dict
from flask import jsonify


class ApiResponse:
    """
    Classe utilitária para criar respostas HTTP padronizadas.
    
    Formato de sucesso:
    {
        "success": true,
        "data": {...} ou [...],
        "message": "opcional"
    }
    
    Formato de erro:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Descrição do erro",
            "field": "campo_opcional"
        }
    }
    """
    
    @staticmethod
    def success(data: Any = None, message: str = None, status_code: int = 200):
        """
        Cria uma resposta de sucesso padronizada.
        
        Args:
            data: Dados a serem retornados (dict, list, ou None)
            message: Mensagem opcional de sucesso
            status_code: Código HTTP (default 200)
            
        Returns:
            Tuple de (response_json, status_code)
        """
        response = {
            "success": True,
            "data": data
        }
        if message:
            response["message"] = message
        return jsonify(response), status_code
    
    @staticmethod
    def created(data: Any = None, message: str = "Recurso criado com sucesso"):
        """Atalho para resposta 201 Created."""
        return ApiResponse.success(data, message, 201)
    
    @staticmethod
    def no_content():
        """Atalho para resposta 204 No Content."""
        return '', 204
    
    @staticmethod
    def error(
        message: str,
        code: str = "ERROR",
        status_code: int = 400,
        field: str = None,
        details: Dict = None
    ):
        """
        Cria uma resposta de erro padronizada.
        
        Args:
            message: Mensagem descritiva do erro
            code: Código do erro (ex: NOT_FOUND, VALIDATION_ERROR)
            status_code: Código HTTP (default 400)
            field: Campo relacionado ao erro (para erros de validação)
            details: Detalhes adicionais do erro
            
        Returns:
            Tuple de (response_json, status_code)
        """
        error_obj = {
            "code": code,
            "message": message
        }
        if field:
            error_obj["field"] = field
        if details:
            error_obj["details"] = details
            
        response = {
            "success": False,
            "error": error_obj
        }
        return jsonify(response), status_code
    
    @staticmethod
    def not_found(resource: str, resource_id: int = None):
        """Atalho para resposta 404 Not Found."""
        message = f"{resource} não encontrado(a)"
        if resource_id:
            message = f"{resource} com ID {resource_id} não encontrado(a)"
        return ApiResponse.error(message, "NOT_FOUND", 404)
    
    @staticmethod
    def validation_error(message: str, field: str = None):
        """Atalho para resposta 400 de erro de validação."""
        return ApiResponse.error(message, "VALIDATION_ERROR", 400, field)
    
    @staticmethod
    def conflict(message: str):
        """Atalho para resposta 409 Conflict."""
        return ApiResponse.error(message, "CONFLICT", 409)
    
    @staticmethod
    def business_error(message: str):
        """Atalho para resposta 422 de erro de regra de negócio."""
        return ApiResponse.error(message, "BUSINESS_RULE_VIOLATION", 422)
    
    @staticmethod
    def list_response(items: List, total: int = None):
        """
        Cria uma resposta de lista padronizada.
        
        Args:
            items: Lista de itens
            total: Total de itens (para paginação futura)
            
        Returns:
            Tuple de (response_json, status_code)
        """
        data = {
            "items": items,
            "count": len(items)
        }
        if total is not None:
            data["total"] = total
        return ApiResponse.success(data)
