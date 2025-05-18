import os

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Configure the backend API URL
BACKEND_API_URL = os.environ.get("BACKEND_API_URL", "http://localhost:5000/api/weather")


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    location_info = None
    error_message = None

    if request.method == "POST":
        location_name = request.form.get("location")

        try:
            # Call the backend API
            response = requests.get(BACKEND_API_URL, params={"location": location_name})

            if response.status_code == 200:
                data = response.json()
                weather_data = [
                    {
                        "temperature": item["temperature"],
                        "humidity": item["humidity"],
                        "time": item["time"],
                    }
                    for item in data["weather"]
                ]
                location_info = (
                    f"{data['location']['city']}, {data['location']['country']}"
                )
            else:
                error_message = response.json().get(
                    "error", "An unknown error occurred"
                )
        except requests.RequestException:
            error_message = (
                "Could not connect to the weather service. Please try again later."
            )

    return render_template(
        "index.html", weather=weather_data, location=location_info, error=error_message
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
