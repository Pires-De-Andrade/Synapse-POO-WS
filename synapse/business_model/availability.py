from datetime import time as dtime
from typing import Optional, Dict

class Availability:
    def __init__(self, psychologist_id: int, day_of_week: int, start_time: dtime, end_time: dtime, id: Optional[int]=None, is_active: bool=True):
        self.id = id
        self.psychologist_id = psychologist_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = is_active

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True

    def update_times(self, start_time=None, end_time=None):
        if start_time: self.start_time = start_time
        if end_time: self.end_time = end_time

    def get_time_range(self):
        return (self.start_time, self.end_time)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "psychologist_id": self.psychologist_id,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time.isoformat() if isinstance(self.start_time, dtime) else self.start_time,
            "end_time": self.end_time.isoformat() if isinstance(self.end_time, dtime) else self.end_time,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: Dict):
        data = data.copy()
        if data.get("start_time") and not isinstance(data["start_time"], dtime):
            data["start_time"] = dtime.fromisoformat(data["start_time"])
        if data.get("end_time") and not isinstance(data["end_time"], dtime):
            data["end_time"] = dtime.fromisoformat(data["end_time"])
        return cls(**data)
