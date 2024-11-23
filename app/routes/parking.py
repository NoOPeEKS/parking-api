import sqlite3
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/parking")


@router.get(path="/{parking_id}")
def get_parking_info(parking_id: int):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        # Query to fetch the parking details and calculate occupied spots
        cursor.execute("""
        SELECT 
            p.id AS parking_id,
            p.max_spots,
            (p.max_spots - h.free_spots) AS occupied_spots,
            p.coordinates,
            p.name
        FROM 
            Parking p
        LEFT JOIN 
            SpotHistory h ON p.id = h.parking_id
        WHERE 
            p.id = ?
        ORDER BY 
            h.timestamp DESC
        LIMIT 1;
        """, (parking_id,))

        result = cursor.fetchone()
        if result:
            return {
                "parking_id": result[0],
                "max_spots": result[1],
                "occupied_spots": result[2],
                "coordinates": result[3],
                "name": result[4]
            }
        else:
            raise HTTPException(status_code=404, detail="Parking lot not found")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()
