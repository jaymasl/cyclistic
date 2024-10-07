import duckdb
import os
from datetime import datetime, timedelta

def create_db(db_path):
    conn = duckdb.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rides (
            ride_id TEXT,
            rideable_type TEXT,
            started_at TIMESTAMP,
            ended_at TIMESTAMP,
            start_station_name TEXT,
            start_station_id TEXT,
            end_station_name TEXT,
            end_station_id TEXT,
            start_lat FLOAT,
            start_lng FLOAT,
            end_lat FLOAT,
            end_lng FLOAT,
            member_casual TEXT
        )
    """)

    csv_folder = 'ridedata'
    start_date, end_date = datetime(2023, 9, 1), datetime(2024, 8, 31)
    current_date = start_date

    while current_date <= end_date:
        month_str = current_date.strftime('%Y%m')
        csv_file = os.path.join(csv_folder, f'{month_str}-divvy-ridedata.csv')
        if os.path.exists(csv_file):
            try:
                conn.execute(f"""
                    INSERT INTO rides 
                    SELECT * FROM read_csv_auto('{csv_file}')
                """)
            except Exception as e:
                print(f"Error inserting data from {csv_file}: {e}")
        else:
            print(f"Warning: File {csv_file} not found. Skipping.")
        current_date = (current_date + timedelta(days=32)).replace(day=1)

    conn.close()
    print("Dirty database created successfully. Make sure to check it and run clean_outliers.py.")

if __name__ == "__main__":
    db_path = 'ridedata.ddb'
    create_db(db_path)
