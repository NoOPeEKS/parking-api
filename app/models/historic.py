from pydantic import BaseModel
from typing import List

class HistoryEntry(BaseModel):
    hour: str
    occupied_spots: int

class OutputBody(BaseModel):
    parking_id: int
    history: List[HistoryEntry]
