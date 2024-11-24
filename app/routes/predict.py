import sqlite3
from fastapi import APIRouter, HTTPException
import pandas as pd
from xgboost import XGBRegressor

router = APIRouter(prefix="/predict")

@router.get(path="/{parking_id}")
def predict_historic_data(parking_id: int):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        # Fetch historical data
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

        # Convert data to DataFrame
        df = pd.DataFrame(results, columns=["datetime", "occupied_spots"])

        # Feature engineering
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['is_weekend'] = df['datetime'].dt.isin([5,6]).astype(int)

        # Train model
        X = df[['hour', 'day_of_week', 'is_weekend']]
        y = df['occupied_spots']
        model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
        model.fit(X, y)

        # Predict
        future_timestamps = pd.date_range(start=df['datetime'].iloc[-1] + pd.Timedelta(hours=1), periods=168, freq='H')
        future_data = pd.DataFrame({
            'hour': future_timestamps.hour,
            'day_of_week': future_timestamps.dayofweek,
            'is_weekend': future_timestamps.dayofweek.isin([5, 6]).astype(int)
        })

        future_predictions = model.predict(future_data)

        # Crear un dataframe per les prediccions
        predictions = pd.DataFrame({
            "datetime": future_timestamps,
            "predicted_occupied_spots": future_predictions
        })

        return predictions.to_json(orient="records", date_format="iso")

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        connection.close()
