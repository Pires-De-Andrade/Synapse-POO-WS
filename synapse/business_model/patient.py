from datetime import datetime
from typing import Optional, Dict

class Patient:
    def __init__(self, name: str, email: str, phone: str, cpf: Optional[str] = None, id: Optional[int]=None, created_at: Optional[datetime]=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.cpf = cpf
        self.created_at = created_at or datetime.now()

    def validate_email(self):
        return "@" in self.email and "." in self.email

    def validate_phone(self):
        return self.phone is not None and len(self.phone) >= 8

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "cpf": self.cpf,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        if data.get("created_at") and not isinstance(data["created_at"], datetime):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)
