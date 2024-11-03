import streamlit as st
import pymysql
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")  # Set layout to wide

# Load environment variables
load_dotenv()
mysql_host = os.getenv("MYSQL_HOST")
mysql_username = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_port = os.getenv("MYSQL_PORT")
mysql_database = os.getenv("MYSQL_DATABASE")

# Set up a connection to the MySQL database
def create_connection():
    return pymysql.connect(
        host=mysql_host,
        user=mysql_username,
        password=mysql_password,
        database=mysql_database
    )

# Fetch distinct routes from the database
def fetch_routes():
    conn = create_connection()
    query = "SELECT DISTINCT route_name FROM redbus_data"
    routes = pd.read_sql(query, conn)
    conn.close()
    return routes['route_name'].tolist()

# Fetch maximum price for dynamic slider range
def fetch_max_price():
    conn = create_connection()
    query = "SELECT MAX(price) as max_price FROM redbus_data"
    max_price = pd.read_sql(query, conn).iloc[0]["max_price"]
    conn.close()
    return max_price

def format_timedelta(td):
    if pd.isnull(td):
        return ""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

# Fetch data from the database based on filters
def fetch_data(bus_route=None, departing_time=None, min_rating=None, min_price=None, max_price=None, min_duration=None,
               max_duration=None):
    conn = create_connection()
    query = "SELECT DISTINCT * FROM redbus_data WHERE 1=1"

    # Apply filters based on user selections
    if bus_route and bus_route != "All":
        query += f" AND route_name = '{bus_route}'"
    if departing_time:
        query += f" AND departing_time >= '{departing_time}'"
    if min_rating is not None:
        query += f" AND star_rating >= {min_rating}"
    if min_price is not None:
        query += f" AND price >= {min_price}"
    if max_price is not None:
        query += f" AND price <= {max_price}"
    if min_duration is not None:
        query += f" AND duration >= '{min_duration}'"
    if max_duration is not None:
        query += f" AND duration <= '{max_duration}'"

    # Retrieve data
    data = pd.read_sql(query, conn)
    conn.close()

    # Convert time columns to a readable format
    if 'departing_time' in data.columns:
        data['departing_time'] = data['departing_time'].apply(format_timedelta)
    if 'reaching_time' in data.columns:
        data['reaching_time'] = data['reaching_time'].apply(format_timedelta)

    return data

# Streamlit App
st.title("Bus Ticket Finder")

# Sidebar filters
st.sidebar.header("Filters")

# Dynamically fetch and display unique routes in the dropdown
routes = fetch_routes()
selected_route = st.sidebar.selectbox("Select Route", options=["All"] + routes, help="Select a route.")

# Filter by Departing Time
departing_time = st.sidebar.time_input("Departing After", value=None,
                                       help="Select the earliest time you want to depart.")

# Filter by Star Rating
star_rating = st.sidebar.slider("Minimum Star Rating", 0.0, 5.0, 3.0,
                                help="Select the minimum star rating for your bus.")

# Fetch maximum price and set price range slider dynamically
max_price_value = fetch_max_price()
price_range = st.sidebar.slider("Price Range", 0, int(max_price_value), (100, int(max_price_value)),
                                help="Select the price range for your ticket.")

# Improved Duration Filter: Two sliders for min and max duration
min_duration = st.sidebar.slider("Minimum Duration (in hours)", 0.0, 24.0, 1.0,
                                 help="Select the minimum duration for your trip.")
max_duration = st.sidebar.slider("Maximum Duration (in hours)", 0.0, 24.0, 12.0,
                                 help="Select the maximum duration for your trip.")
min_duration_str, max_duration_str = [f"{int (d):02}:00:00" for d in [min_duration, max_duration]]

# Fetch and display data
data = fetch_data(
    bus_route=selected_route if selected_route != "All" else None,  # Correct variable name
    departing_time=departing_time,
    min_rating=star_rating,
    min_price=price_range[0],
    max_price=price_range[1],
    min_duration=min_duration_str,
    max_duration=max_duration_str
)

# Display results in the app
st.write("### Available Bus Tickets")

if not data.empty:
    # Increase table width to fit the page, minimizing horizontal scroll
    data.set_index('id', inplace=True)
    st.dataframe(data)
else:
    st.write("No buses found with the selected filters.")