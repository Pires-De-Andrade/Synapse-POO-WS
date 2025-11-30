from datetime import datetime
from typing import Optional, Dict

class Clinic:
    def __init__(self, user_id: int, name: str, address: str, phone: str, email: str, id: Optional[int]=None, created_at: Optional[datetime]=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.created_at = created_at or datetime.now()

    def update_info(self, address=None, phone=None, email=None):
        if address: self.address = address
        if phone: self.phone = phone
        if email: self.email = email

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        if data.get("created_at") and not isinstance(data["created_at"], datetime):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)
