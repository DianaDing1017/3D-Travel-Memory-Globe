from flask import Flask, render_template, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# 初始化地理编码器
geolocator = Nominatim(user_agent="my_earth_app")

def get_coordinates(city):
    try:
        location = geolocator.geocode(city)
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "name": city
            }
        return None
    except GeocoderTimedOut:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/location/<city>')
def get_location(city):
    coordinates = get_coordinates(city)
    if coordinates:
        return jsonify(coordinates)
    return jsonify({"error": "Location not found"}), 404

if __name__ == '__main__':
    app.run(debug=True) 