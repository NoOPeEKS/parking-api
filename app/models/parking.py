from pydantic import BaseModel

class OutputBody(BaseModel):
    parking_id: int
    max_spots: int
    occupied_spots: int
    coordinates: str
    name: str
