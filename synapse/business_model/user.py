from datetime import datetime
from typing import Optional, Dict
import bcrypt

class User:
    def __init__(self, email: str, password: str, user_type: str, name: str, id: Optional[int]=None, password_hash: Optional[str]=None, created_at: Optional[datetime]=None):
        self.id = id
        self.email = email
        self.user_type = user_type
        self.name = name
        self.created_at = created_at or datetime.now()
        if password_hash:
            self.password_hash = password_hash
        else:
            self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def update_password(self, old_password, new_password):
        if self.check_password(old_password) and len(new_password) >= 8:
            self.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode()
            return True
        return False

    def get_role(self):
        return self.user_type

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "email": self.email,
            "user_type": self.user_type,
            "name": self.name,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        if data.get("created_at") and not isinstance(data["created_at"], datetime):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        password_hash = data.pop("password_hash", None)
        password = data.pop("password", "dummy")
        return cls(password_hash=password_hash, password=password, **data)
