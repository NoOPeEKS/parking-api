import sqlite3
from fastapi import APIRouter, HTTPException
from models import historic

router = APIRouter(prefix="/historic")


@router.get(path="/{parking_id}")
def get_historic_data(parking_id: int):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
        SELECT 
            strftime('%Y-%m-%d %H:00:00', h.timestamp) AS hour,
            MAX(p.max_spots - h.free_spots) AS occupied_spots
        FROM 
            SpotHistory h
        JOIN 
            Parking p ON h.parking_id = p.id
        WHERE 
            h.parking_id = ?
        GROUP BY 
            hour
        ORDER BY 
            hour ASC;
        """,
            (parking_id,),
        )

        results = cursor.fetchall()
        if not results:
            raise HTTPException(
                status_code=404, detail="No history found for this parking lot"
            )

        history = [
            historic.HistoryEntry(hour=row[0], occupied_spots=row[1]) for row in results
        ]
        return historic.OutputBody(parking_id=parking_id, history=history)

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()
