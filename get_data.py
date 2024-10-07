import duckdb

def execute_query(query):
    with duckdb.connect('ridedata.ddb') as con:
        return con.execute(query).fetchall()

def get_user_ride_counts():
    user_counts = execute_query("""
        SELECT COUNT(*) FILTER (WHERE member_casual = 'member') AS total_members,
               COUNT(*) FILTER (WHERE member_casual = 'casual') AS total_casual
        FROM rides
    """)[0]
    return user_counts[0], user_counts[1]

def get_total_rides():
    return execute_query("SELECT COUNT(*) AS total_rides FROM rides")[0][0]

def get_average_duration_by_user_type():
    average_durations = execute_query("""
        SELECT member_casual, AVG(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60) AS average_duration
        FROM rides
        GROUP BY member_casual
    """)
    return {user_type: round(duration, 2) for user_type, duration in average_durations}

def get_hourly_ride_counts():
    query = """
    SELECT 
        strftime('%H', started_at) AS hour, 
        SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_count,
        SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_count
    FROM rides
    GROUP BY hour
    ORDER BY hour;
    """
    
    result = execute_query(query)
    
    hourly_counts = {}
    for row in result:
        hour = row[0]
        member_count = row[1]
        casual_count = row[2]
        hourly_counts[hour] = {
            'member': member_count,
            'casual': casual_count
        }
    
    return hourly_counts

def get_rides_by_day_of_week():
    rides_by_day = execute_query("""
        SELECT STRFTIME('%w', started_at) AS day_of_week, 
               member_casual, 
               COUNT(*) AS ride_count
        FROM rides
        GROUP BY day_of_week, member_casual
        ORDER BY day_of_week, member_casual;
    """)

    day_mapping = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    ride_counts = {day: {'members': 0, 'casual': 0} for day in day_mapping}

    for day, member_casual, count in rides_by_day:
        day_index = int(day)
        if member_casual == 'member':
            ride_counts[day_mapping[day_index]]['members'] = count
        elif member_casual == 'casual':
            ride_counts[day_mapping[day_index]]['casual'] = count

    return ride_counts

def get_rides_by_month():
    rides_by_month = execute_query("""
        SELECT 
            STRFTIME('%Y-%m', started_at) AS month,
            member_casual,
            COUNT(*) AS ride_count
        FROM rides
        WHERE started_at >= '2023-09-01' AND started_at < '2024-09-01'
        GROUP BY month, member_casual
        ORDER BY month, member_casual;
    """)

    result = {}
    for month, member_casual, count in rides_by_month:
        if month not in result:
            result[month] = {'member': 0, 'casual': 0}
        result[month][member_casual] += count

    return result

def get_rideable_type_by_user_type():
    rideable_counts = execute_query("""
        SELECT rideable_type, member_casual, COUNT(*) AS ride_count
        FROM rides
        GROUP BY rideable_type, member_casual
    """)
    result = {
        'classic_bike': {'member': 0, 'casual': 0},
        'electric_bike': {'member': 0, 'casual': 0},
    }
    for rideable_type, user_type, count in rideable_counts:
        if rideable_type in result:
            result[rideable_type][user_type] = count
    return result

def get_top_stations(limit=10):
    query = f"""
        SELECT 
            start_station_name, 
            start_lat,
            start_lng,
            COUNT(CASE WHEN member_casual = 'member' THEN 1 END) AS member_count,
            COUNT(CASE WHEN member_casual = 'casual' THEN 1 END) AS casual_count,
            COUNT(*) AS ride_count
        FROM rides
        WHERE start_station_name IS NOT NULL
        GROUP BY start_station_name, start_lat, start_lng
        ORDER BY ride_count DESC
        LIMIT {limit};
    """
    return execute_query(query)

def get_top_stations_with_member_casual_counts(limit=10):
    query = f"""
        SELECT 
            start_station_name, 
            start_lat,
            start_lng,
            COUNT(*) AS total_ride_count,
            SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_count,
            SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_count
        FROM rides
        WHERE start_station_name IS NOT NULL
        GROUP BY start_station_name, start_lat, start_lng
        ORDER BY total_ride_count DESC
        LIMIT {limit};
    """
    return execute_query(query)

def get_top_stations_with_coordinates(limit=10):
    query = f"""
        SELECT 
            start_station_name, 
            start_lat,
            start_lng,
            COUNT(*) AS ride_count
        FROM rides
        WHERE start_station_name IS NOT NULL
        GROUP BY start_station_name, start_lat, start_lng
        ORDER BY ride_count DESC
        LIMIT {limit};
    """
    return execute_query(query)

def get_ride_duration_distribution():
    query = """
        SELECT 
            FLOOR(DATEDIFF('second', started_at, ended_at) / 60.0 / 5) * 5 AS duration_range,
            member_casual,
            COUNT(*) AS ride_count
        FROM rides
        GROUP BY duration_range, member_casual
        ORDER BY duration_range, member_casual;
    """
    return execute_query(query)

