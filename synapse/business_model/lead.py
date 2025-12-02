from datetime import datetime
from typing import Optional, Dict

class Lead:
    def __init__(self, name: str, email: str, phone: str, source: str, notes: Optional[str]=None, status: str="new", id: Optional[int]=None, created_at: Optional[datetime]=None, converted_at: Optional[datetime]=None, converted_to_patient_id: Optional[int]=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.source = source
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.converted_at = converted_at
        self.converted_to_patient_id = converted_to_patient_id

    def mark_as_contacted(self, notes=None):
        if self.status == "new":
            self.status = "contacted"
            if notes:
                self.notes = notes

    def convert_to_patient(self, patient_id):
        if self.status in ["new","contacted"]:
            self.status = "converted"
            self.converted_at = datetime.now()
            self.converted_to_patient_id = patient_id

    def mark_as_lost(self, reason=None):
        if self.status in ["new", "contacted"]:
            self.status = "lost"
            if reason:
                self.notes = f"Perdido: {reason}"

    def update_notes(self, notes):
        self.notes = notes

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "source": self.source,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "converted_at": self.converted_at.isoformat() if self.converted_at and isinstance(self.converted_at, datetime) else self.converted_at,
            "converted_to_patient_id": self.converted_to_patient_id
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        for attr in ["created_at","converted_at"]:
            if data.get(attr) and not isinstance(data[attr], datetime):
                data[attr] = datetime.fromisoformat(data[attr])
        return cls(**data)
