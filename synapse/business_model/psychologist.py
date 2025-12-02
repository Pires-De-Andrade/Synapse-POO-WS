from datetime import datetime
from typing import List, Optional, Dict

class Psychologist:
    def __init__(self, user_id: int, name: str, crp: str, specialty: str, hourly_rate: float, themes: Optional[List[str]] = None,
                 bio: str = "", id: Optional[int]=None, is_active: bool = True, created_at: Optional[datetime]=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.crp = crp
        self.specialty = specialty
        self.themes = themes or []
        self.bio = bio
        self.hourly_rate = hourly_rate
        self.is_active = is_active
        self.created_at = created_at or datetime.now()

    def update_profile(self, specialty=None, themes=None, bio=None):
        if specialty: self.specialty = specialty
        if themes: self.themes = themes
        if bio: self.bio = bio

    def set_hourly_rate(self, rate):
        if rate > 0:
            self.hourly_rate = rate

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def validate_crp(self):
        return isinstance(self.crp, str) and "/" in self.crp

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "crp": self.crp,
            "specialty": self.specialty,
            "themes": self.themes,
            "bio": self.bio,
            "hourly_rate": self.hourly_rate,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        if data.get("created_at") and not isinstance(data["created_at"], datetime):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)
