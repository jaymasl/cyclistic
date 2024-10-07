import duckdb
from prettytable import PrettyTable

def execute_query(query):
    with duckdb.connect('ridedata.ddb') as con:
        return con.execute(query).fetchall()

def filter_outliers():
    outlier_conditions = {
        "Negative Durations": "ended_at < started_at",
        "Long Rides (> 3 hours)": "(ended_at - started_at) > INTERVAL '3 hours'",
        "Short Rides (< 1 minute)": "(ended_at - started_at) < INTERVAL '1 minute'",
        "Long Distance Rides (> 25 km)": "(6371 * ACOS(GREATEST(-1, LEAST(1, COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) * COS(RADIANS(end_lng) - RADIANS(start_lng)) + SIN(RADIANS(start_lat)) * SIN(RADIANS(end_lat))))) > 25)",
        "No Location Info": "(start_lat IS NULL AND start_lng IS NULL) OR (end_lat IS NULL AND end_lng IS NULL)"
    }

    cleaned_counts = {key: 0 for key in outlier_conditions.keys()}

    for outlier_type, condition in outlier_conditions.items():
        count_outlier_query = f"SELECT COUNT(*) FROM rides WHERE {condition}"
        count = execute_query(count_outlier_query)[0][0]
        cleaned_counts[outlier_type] += count

    if all(count == 0 for count in cleaned_counts.values()):
        print("The outliers have already been cleaned. No further action needed.")
        return None

    outlier_query = "DELETE FROM rides WHERE " + " OR ".join(outlier_conditions.values())
    execute_query(outlier_query)

    return cleaned_counts

def check_remaining_outliers():
    outlier_check_query = """
        SELECT COUNT(*) AS outlier_count
        FROM rides
        WHERE ended_at < started_at 
           OR (ended_at - started_at) > INTERVAL '3 hours'
           OR (ended_at - started_at) < INTERVAL '1 minute'
           OR (6371 * ACOS(GREATEST(-1, LEAST(1, COS(RADIANS(start_lat)) * COS(RADIANS(end_lat)) * COS(RADIANS(end_lng) - RADIANS(start_lng)) + SIN(RADIANS(start_lat)) * SIN(RADIANS(end_lat))))) > 25)
           OR (start_lat IS NULL AND start_lng IS NULL) 
           OR (end_lat IS NULL AND end_lng IS NULL)
    """
    outlier_count = execute_query(outlier_check_query)[0][0]
    if outlier_count == 0:
        print("All outliers have been cleaned. No remaining outliers.")
        return False
    else:
        print(f"Warning: There are still {outlier_count} outliers remaining.")
        return True

def report_cleaned_outliers(cleaned_counts):
    if cleaned_counts is None:
        return
    
    table = PrettyTable()
    table.field_names = ["Outlier Type", "Count Cleaned"]

    for outlier_type, count in cleaned_counts.items():
        table.add_row([outlier_type, count])
    
    print("\nOutlier Cleaning Report:")
    print(table)

if check_remaining_outliers():
    cleaned_counts = filter_outliers()
    report_cleaned_outliers(cleaned_counts)
    check_remaining_outliers()
