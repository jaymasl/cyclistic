from flask import Flask, render_template
from flask_caching import Cache
import get_data
import create_graph
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
application = app

app.config.update(
    CACHE_TYPE='simple',
    CACHE_DEFAULT_TIMEOUT=3600,
    CACHE_KEY_PREFIX='myapp_',
    CACHE_THRESHOLD=500
)

cache = Cache(app)

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

@cache.memoize(timeout=3600)
def get_cached_top_stations(limit):
    logger.info(f"Fetching top {limit} stations from database")
    return get_data.get_top_stations(limit=limit)

@cache.memoize(timeout=3600)
def get_cached_user_ride_counts():
    logger.info("Fetching user ride counts from database")
    return get_data.get_user_ride_counts()

@cache.memoize(timeout=3600)
def create_cached_graphs(total_members, total_casual, top_stations):
    logger.info("Creating cached graphs")
    return {
        'ride_count': create_graph.create_ride_count_graph(total_members, total_casual),
        'average_duration': create_graph.create_average_duration_graph(),
        'rides_by_day': create_graph.create_rides_by_day_graph(),
        'rides_by_month': create_graph.create_rides_by_month_graph(),
        'rideable_type': create_graph.create_rideable_type_graph(),
        'rides_by_hour': create_graph.create_hourly_rides_graph(),
        'station_usage': create_graph.create_member_casual_top_stations_graph(top_stations),
        'ride_duration': create_graph.create_ride_duration_histogram()
    }

@cache.memoize(timeout=3600)
def create_cached_station_map():
    logger.info("Creating station map")
    return create_graph.create_station_map()

@app.route('/')
def index():
    return render_template('base.jinja')

@app.route('/summary')
@cache.cached(timeout=3600)
def summary():
    top_stations = get_cached_top_stations(limit=10)
    return render_template('summary.jinja', top_stations=top_stations)

@app.route('/data')
@cache.cached(timeout=3600)
def data():
    total_members, total_casual = get_cached_user_ride_counts()
    top_stations = get_cached_top_stations(limit=10)
    graphs = create_cached_graphs(total_members, total_casual, top_stations)
    return render_template('data.jinja', **graphs)

@app.route('/map')
@cache.cached(timeout=3600)
def map_view():
    fig = create_cached_station_map()
    map_html = fig.to_html(full_html=False)
    return render_template('map.jinja', map_html=map_html)

@app.route('/recommend')
def recommend():
    return render_template('recommend.jinja')

@app.errorhandler(500)
def handle_500(error):
    cache.clear()
    logger.info("Cache cleared due to internal server error")
    return "Internal Server Error", 500

def update_cache():
    logger.info("Updating cache...")
    try:
        top_stations = get_cached_top_stations(limit=10)
        total_members, total_casual = get_cached_user_ride_counts()
        create_cached_graphs(total_members, total_casual, top_stations)
        create_cached_station_map()
        logger.info("Cache update completed successfully")
    except Exception as e:
        logger.error(f"Cache update failed: {str(e)}")
        cache.clear()

with app.app_context():
    update_cache()

if __name__ == '__main__':
    app.run(debug=False)
