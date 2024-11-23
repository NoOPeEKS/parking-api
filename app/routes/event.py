import sqlite3
from fastapi import APIRouter
from models import event

router = APIRouter(prefix="/event")


@router.post(path="/insert")
def process_event(body: event.InputBody) -> event.OutputBody:
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        # Insert the event into ParkingEvent
        cursor.execute("""
            INSERT INTO ParkingEvent (parking_id, event_type, timestamp)
            VALUES (?, ?, ?)
        """, (body.parking_id, body.event_type, body.time))

        # Get the current number of free spots from SpotHistory
        cursor.execute("""
            SELECT free_spots 
            FROM SpotHistory 
            WHERE parking_id = ?
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (body.parking_id,))
        current_free_spots = cursor.fetchone()

        if current_free_spots is None:
            # If no history exists, use the maximum number of spots for this parking lot
            cursor.execute("""
                SELECT max_spots 
                FROM Parking 
                WHERE id = ?
            """, (body.parking_id,))
            max_spots = cursor.fetchone()
            if max_spots is None:
                raise ValueError(f"Parking lot with ID {body.parking_id} does not exist.")
            current_free_spots = max_spots[0]
        else:
            current_free_spots = current_free_spots[0]

        # Adjust free spots based on the event type
        if body.event_type == 'ENTRY':
            new_free_spots = current_free_spots - 1
        elif body.event_type == 'EXIT':
            new_free_spots = current_free_spots + 1
        else:
            raise ValueError(f"Invalid event_type: {body.event_type}")

        # Ensure free spots do not exceed max_spots or go below zero
        cursor.execute("""
            SELECT max_spots 
            FROM Parking 
            WHERE id = ?
        """, (body.parking_id,))
        max_spots = cursor.fetchone()[0]
        new_free_spots = max(0, min(new_free_spots, max_spots))

        # Insert the updated free spots into SpotHistory
        cursor.execute("""
            INSERT INTO SpotHistory (parking_id, timestamp, free_spots)
            VALUES (?, ?, ?)
        """, (body.parking_id, body.time, new_free_spots))

        # Commit changes
        connection.commit()
        print(f"Event and updated free spots saved successfully for parking_id {body.parking_id}.")
        return event.OutputBody(message="Worked")
    
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return event.OutputBody(message=f"error happened: {e}")
    
    finally:
        connection.close()
