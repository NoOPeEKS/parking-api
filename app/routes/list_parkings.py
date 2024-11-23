import sqlite3
from fastapi import APIRouter, HTTPException
from models import list_parkings

router = APIRouter(prefix="/list_parkings")


@router.get(path="")
def get_parkings():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id, name FROM Parking")
        results = cursor.fetchall()

        if not results:
            raise HTTPException(status_code=404, detail="No parkings found")

        parkings = [
            list_parkings.OutputModel(parking_id=row[0], name=row[1]) for row in results
        ]
        return parkings

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()
