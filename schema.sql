-- Table to store parking lot details
CREATE TABLE Parking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    coordinates TEXT NOT NULL, -- Stored as "latitude,longitude"
    max_spots INTEGER NOT NULL
);

-- Table to store events (car entry and exit)
CREATE TABLE ParkingEvent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL,
    event_type TEXT CHECK(event_type IN ('ENTRY', 'EXIT')) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parking_id) REFERENCES Parking(id)
);

-- Table to store the history of free spots
CREATE TABLE SpotHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parking_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    free_spots INTEGER NOT NULL,
    FOREIGN KEY (parking_id) REFERENCES Parking(id)
);
