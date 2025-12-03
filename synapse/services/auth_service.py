from synapse.repositories.implementations.inmemory_user_repository import InMemoryUserRepository
from synapse.business_model.user import User

class AuthService:
    def __init__(self, user_repository: InMemoryUserRepository):
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> User | None:
        user = self.user_repository.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None
