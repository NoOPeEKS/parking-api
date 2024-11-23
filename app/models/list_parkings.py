from pydantic import BaseModel

class OutputModel(BaseModel):
    parking_id: int
    name: str

