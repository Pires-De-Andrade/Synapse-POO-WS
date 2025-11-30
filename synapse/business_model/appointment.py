from datetime import datetime, date, time as dtime
from typing import Optional, Dict

class Appointment:
    def __init__(self, patient_id: int, psychologist_id: int, date: date, time: dtime, duration: int = 60, notes: Optional[str] = None, id: Optional[int]=None, status: str="scheduled", created_at: Optional[datetime]=None, cancelled_at: Optional[datetime]=None, cancellation_reason: Optional[str]=None):
        self.id = id
        self.patient_id = patient_id
        self.psychologist_id = psychologist_id
        self.date = date
        self.time = time
        self.duration = duration
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.cancelled_at = cancelled_at
        self.cancellation_reason = cancellation_reason

    def confirm(self):
        if self.status == "scheduled":
            self.status = "confirmed"

    def cancel(self, reason=None):
        if self.status not in ["cancelled", "completed"]:
            self.status = "cancelled"
            self.cancelled_at = datetime.now()
            self.cancellation_reason = reason

    def complete(self):
        if self.status in ["scheduled", "confirmed"]:
            self.status = "completed"

    def reschedule(self, new_date, new_time):
        if self.status not in ["cancelled", "completed"]:
            self.date = new_date
            self.time = new_time
            self.status = "scheduled"

    def is_past(self):
        dt = self.get_datetime()
        return dt < datetime.now()

    def get_datetime(self):
        return datetime.combine(self.date, self.time)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "psychologist_id": self.psychologist_id,
            "date": self.date.isoformat() if isinstance(self.date, date) else self.date,
            "time": self.time.isoformat() if isinstance(self.time, dtime) else self.time,
            "duration": self.duration,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at and isinstance(self.cancelled_at, datetime) else self.cancelled_at,
            "cancellation_reason": self.cancellation_reason
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        for attr in ["created_at", "cancelled_at"]:
            if data.get(attr) and not isinstance(data[attr], datetime):
                data[attr] = datetime.fromisoformat(data[attr])
        if data.get("date") and not isinstance(data["date"], date):
            data["date"] = date.fromisoformat(data["date"])
        if data.get("time") and not isinstance(data["time"], dtime):
            data["time"] = dtime.fromisoformat(data["time"])
        return cls(**data)
