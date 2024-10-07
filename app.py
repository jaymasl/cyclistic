from flask import Flask, render_template
import get_data
import create_graph

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.jinja')

@app.route('/summary')
def summary():
    top_stations = get_data.get_top_stations(limit=10)
    return render_template(
        'summary.jinja',  
        top_stations=top_stations
    )

@app.route('/data')
def data():
    total_members, total_casual = get_data.get_user_ride_counts()
    top_stations = get_data.get_top_stations(limit=10)
    ride_count_graph = create_graph.create_ride_count_graph(total_members, total_casual)
    average_duration_graph = create_graph.create_average_duration_graph()
    rides_by_day_graph = create_graph.create_rides_by_day_graph()
    rides_by_month_graph = create_graph.create_rides_by_month_graph()
    rideable_type_graph = create_graph.create_rideable_type_graph()
    rides_by_hour_graph = create_graph.create_hourly_rides_graph()
    station_usage_graph = create_graph.create_member_casual_top_stations_graph(top_stations)
    ride_duration_histogram = create_graph.create_ride_duration_histogram()

    return render_template(
        'data.jinja', 
        ride_count_graph=ride_count_graph,
        average_duration_graph=average_duration_graph,
        rides_by_day_graph=rides_by_day_graph,
        rides_by_month_graph=rides_by_month_graph,
        rideable_type_graph=rideable_type_graph,
        rides_by_hour_graph=rides_by_hour_graph,
        station_usage_graph=station_usage_graph,
        ride_duration_histogram=ride_duration_histogram
    )

@app.route('/map', endpoint='map_view')
def map_view():
    fig = create_graph.create_station_map()
    map_html = fig.to_html(full_html=False)
    return render_template('map.jinja', map_html=map_html)

@app.route('/recommend')
def recommend():
    return render_template('recommend.jinja')

if __name__ == '__main__':
    app.run(debug=True)
