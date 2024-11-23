import sqlite3
from fastapi import APIRouter
from models import event

router = APIRouter(prefix="/event")

@router.post(path="/insert")
def process_event(body: event.InputBody) -> event.OutputBody:
    con = sqlite3.connect("database.db")
    print(body)

    return event.OutputBody(message="Worked")
