from flask import Blueprint, request, jsonify
from synapse.api.dto import AuthLoginDTO, AuthResponseDTO
from synapse.services.auth_service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def create_auth_routes(auth_service: AuthService):
    @bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        try:
            dto = AuthLoginDTO(**data)
        except Exception as e:
            return jsonify({'error': 'Dados inválidos'}), 400
        user = auth_service.login(dto.email, dto.password)
        if not user:
            return jsonify({'error': 'Credenciais inválidas'}), 401
        response = AuthResponseDTO(
            token="fake-token-123",
            user_id=user.id,
            name=user.name,
            user_type=user.user_type
        )
        return jsonify(response.dict()), 200
    return bp
