from flask import Flask, render_template, request
from weather import get_location_coords, get_weather

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    location_info = None
    
    if request.method == "POST":
        location_name = request.form.get("location")
        location_data = get_location_coords(location_name)
        
        if location_data:
            weather_data = get_weather(
                location_data["latitude"], 
                location_data["longitude"]
            )
            location_info = f"{location_data['country']}, {location_data['city']}"
        else:
            weather_data = "Invalid location. Please try again."
    
    return render_template("index.html", weather=weather_data, location=location_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
