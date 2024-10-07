import get_data
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

GRAPH_WIDTH = 400
GRAPH_HEIGHT = 400

MEMBER_COLOR = '#007BFF'
CASUAL_COLOR = '#FFA500'
BG_COLOR = '#1E1E1E'

def create_top_stations_table():
    return get_data.get_top_5_stations()

def create_ride_count_graph(total_members, total_casual):
    fig = go.Figure(data=[
        go.Bar(name='Member', x=['Member'], y=[total_members], marker_color=MEMBER_COLOR),
        go.Bar(name='Casual', x=['Casual'], y=[total_casual], marker_color=CASUAL_COLOR)
    ])
    
    fig.update_layout(
        barmode='group', 
        title='Total Rides', 
        title_font_color='white',
        yaxis_title='Number of Rides',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
        showlegend=False
    )
    
    return fig.to_html(full_html=False)

def create_average_duration_graph():
    average_durations = get_data.get_average_duration_by_user_type()
    if isinstance(average_durations, dict) and 'member' in average_durations and 'casual' in average_durations:
        fig = go.Figure(data=[
            go.Bar(name='Member', x=['Member'], y=[average_durations['member']], marker_color=MEMBER_COLOR),
            go.Bar(name='Casual', x=['Casual'], y=[average_durations['casual']], marker_color=CASUAL_COLOR)
        ])
        
        fig.update_layout(
            barmode='group', 
            title='Average Duration Per Ride', 
            title_font_color='white',
            yaxis_title='Average Duration (minutes)',
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=BG_COLOR,
            font=dict(color='white'),
            width=GRAPH_WIDTH,
            height=GRAPH_HEIGHT,
            showlegend=False
        )
        
        return fig.to_html(full_html=False)

def create_rideable_type_graph():
    rideable_counts = get_data.get_rideable_type_by_user_type()
    
    electric_member = rideable_counts['electric_bike']['member']
    electric_casual = rideable_counts['electric_bike']['casual']
    classic_member = rideable_counts['classic_bike']['member']
    classic_casual = rideable_counts['classic_bike']['casual']

    fig = go.Figure(data=[
        go.Bar(name='Electric Member', x=['Electric Member'], y=[electric_member], marker_color=MEMBER_COLOR),
        go.Bar(name='Classic Member', x=['Classic Member'], y=[classic_member], marker_color='#003D7A'),
        go.Bar(name='Electric Casual', x=['Electric Casual'], y=[electric_casual], marker_color=CASUAL_COLOR),
        go.Bar(name='Classic Casual', x=['Classic Casual'], y=[classic_casual], marker_color='#CC7A00')
    ])
    
    fig.update_layout(
        barmode='group', 
        title='Rideable Type', 
        title_font_color='white',
        yaxis_title='Number of Rides',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        width=GRAPH_WIDTH,
        height=GRAPH_HEIGHT,
        showlegend=False
    )
    
    return fig.to_html(full_html=False)

def create_hourly_rides_graph():
    active_hours = get_data.get_hourly_ride_counts()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(active_hours.keys()),
        y=[active_hours[hour]['member'] for hour in active_hours.keys()],
        name='Member',
        marker_color=MEMBER_COLOR
    ))

    fig.add_trace(go.Bar(
        x=list(active_hours.keys()),
        y=[active_hours[hour]['casual'] for hour in active_hours.keys()],
        name='Casual',
        marker_color=CASUAL_COLOR
    ))

    fig.update_layout(
        title='Rides by Hour',
        xaxis_title='Hour of the Day',
        yaxis_title='Number of Rides',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        barmode='group',
        autosize=True,
        legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center', yanchor='bottom')
    )

    fig.update_yaxes(range=[0, 420000])

    return fig.to_html(full_html=False)

def create_rides_by_day_graph():
    ride_counts = get_data.get_rides_by_day_of_week()

    member_counts = [ride['members'] for ride in ride_counts.values()]
    casual_counts = [ride['casual'] for ride in ride_counts.values()]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(ride_counts.keys()),
        y=member_counts,
        name='Member',
        marker_color=MEMBER_COLOR
    ))

    fig.add_trace(go.Bar(
        x=list(ride_counts.keys()),
        y=casual_counts,
        name='Casual',
        marker_color=CASUAL_COLOR
    ))

    fig.update_layout(
        title='Rides by Week Day',
        xaxis_title='Day of the Week',
        yaxis_title='Number of Rides',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        barmode='group',
        autosize=True,
        legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center', yanchor='bottom')
    )

    return fig.to_html(full_html=False)

def create_rides_by_month_graph():
    rides_by_month = get_data.get_rides_by_month()

    months = list(rides_by_month.keys())
    member_counts = [rides_by_month[month]['member'] for month in months]
    casual_counts = [rides_by_month[month]['casual'] for month in months]

    fig = go.Figure(data=[
        go.Bar(name='Member', x=months, y=member_counts, marker_color=MEMBER_COLOR),
        go.Bar(name='Casual', x=months, y=casual_counts, marker_color=CASUAL_COLOR)
    ])

    fig.update_layout(
        title='Rides by Month', 
        title_font_color='white',
        xaxis_title='Month', 
        yaxis_title='Number of Rides',
        barmode='group',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        autosize=True,
        xaxis=dict(
            tickmode='array',
            tickvals=months,
            ticktext=months
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig.to_html(full_html=False)

def create_member_casual_top_stations_graph(top_stations):
    station_names = [station[0] for station in top_stations]
    member_counts = [station[3] for station in top_stations]
    casual_counts = [station[4] for station in top_stations]

    fig = go.Figure(data=[
        go.Bar(name='Member', x=station_names, y=member_counts, marker_color=MEMBER_COLOR),
        go.Bar(name='Casual', x=station_names, y=casual_counts, marker_color=CASUAL_COLOR)
    ])
    
    fig.update_layout(
        barmode='group', 
        title='Rides by Top 10 Stations with Comparison',
        yaxis_title='Number of Rides',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig.to_html(full_html=False)

def create_ride_duration_histogram():
    data = get_data.get_ride_duration_distribution()
    
    member_counts = {}
    casual_counts = {}

    for row in data:
        if row[0] < 70:
            duration_range_start = int(row[0] // 5 * 5)
            duration_range_label = f"{duration_range_start} - {duration_range_start + 5} mins"
            if row[1] == 'member':
                member_counts[duration_range_label] = member_counts.get(duration_range_label, 0) + row[2]
            elif row[1] == 'casual':
                casual_counts[duration_range_label] = casual_counts.get(duration_range_label, 0) + row[2]

    duration_ranges = sorted(set(member_counts.keys()).union(casual_counts.keys()))
    duration_ranges.sort(key=lambda x: int(x.split()[0]))

    member_counts_list = [member_counts.get(range, 0) for range in duration_ranges]
    casual_counts_list = [casual_counts.get(range, 0) for range in duration_ranges]

    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=duration_ranges, y=member_counts_list, name='Member', marker_color=MEMBER_COLOR, width=0.4))
    fig.add_trace(go.Bar(x=duration_ranges, y=casual_counts_list, name='Casual', marker_color=CASUAL_COLOR, width=0.4))

    fig.update_layout(
        title='Ride Duration Distribution',
        xaxis_title='Duration Ranges (in minutes)',
        yaxis_title='Number of Rides',
        barmode='group',
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        font=dict(color='white'),
        xaxis=dict(tickmode='array', tickvals=duration_ranges, ticktext=duration_ranges, title_standoff=15),
        legend=dict(orientation='h', x=0.5, y=1.1, xanchor='center', yanchor='bottom')
    )
    
    return fig.to_html(full_html=False)

def create_station_map():
    top_stations = get_data.get_top_stations_with_member_casual_counts(limit=10)

    station_names = [station[0] for station in top_stations]
    latitudes = [station[1] for station in top_stations]
    longitudes = [station[2] for station in top_stations]
    total_ride_counts = [station[3] for station in top_stations]
    member_counts = [station[4] for station in top_stations]
    casual_counts = [station[5] for station in top_stations]

    min_size, max_size = 3, 80
    scaled_sizes = np.sqrt(total_ride_counts)

    scaled_sizes = min_size + (scaled_sizes - min(scaled_sizes)) / (max(scaled_sizes) - min(scaled_sizes)) * (max_size - min_size)

    fig = px.scatter_mapbox(
        lat=latitudes,
        lon=longitudes,
        hover_name=station_names,
        color=total_ride_counts,
        color_continuous_scale=[
        (0, 'yellow'),
        (0.5, 'red'),
        (1, 'purple')
        ],
        size=scaled_sizes,
        size_max=max_size,
        mapbox_style="open-street-map",
        title='Map of the Top 10 Cyclistic Stations in Chicago',
        zoom=11,
        opacity=0.8
    )
    
    fig.update_layout(
        height=800,
        autosize=True,
        showlegend=False,
        mapbox=dict(
            zoom=12.5,
            center=dict(lat=latitudes[0] + 0.01, lon=longitudes[0] - 0.01)
        ),
        paper_bgcolor='rgba(0, 0, 0, 1)', 
        plot_bgcolor='rgba(0, 0, 0, 1)',
        title_font=dict(color='white'),
        title={
        'text': 'Map of the Top 10 Cyclistic Stations in Chicago',
        'font': {'size': 24},
        'x': 0.50,
        'xanchor': 'center'
        }
    )

    hover_text = [
        f"Station: {name}<br>Total Rides: {total}<br>Members: {member}<br>Casual: {casual}"
        for name, total, member, casual in zip(station_names, total_ride_counts, member_counts, casual_counts)
    ]

    fig.update_traces(hovertemplate="%{text}<extra></extra>", text=hover_text)

    fig.add_trace(go.Scattermapbox(
        lat=latitudes,
        lon=longitudes,
        mode='markers',
        marker=dict(size=8, color='black', opacity=1),
        hoverinfo='none'
    ))

    return fig
