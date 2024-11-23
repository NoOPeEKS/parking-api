from pydantic import BaseModel


class InputBody(BaseModel):
    parking_id: int
    event_type: str
    time: str


class OutputBody(BaseModel):
    message: str
