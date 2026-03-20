import tkinter as tk
import requests

API_KEY = "YOUR_API_KEY_HERE"  # Replace with your WeatherAPI.com key

def get_weather():
    city = entry_city.get().strip()
    if not city:
        label_status.config(text="Please enter a city.")
        return

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        if "error" in data:
            label_status.config(text=f"Error: {data['error']['message']}")
            label_result.config(text="")
            return

        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]

        result_text = (
            f"{location}, {country}\n"
            f"Temperature: {temp_c} °C\n"
            f"Condition: {condition}\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind_kph} km/h"
        )

        label_result.config(text=result_text)
        label_status.config(text="Weather updated.")
    except Exception as e:
        label_status.config(text=f"Request failed: {e}")
        label_result.config(text="")

root = tk.Tk()
root.title("Weather App")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_title = tk.Label(frame, text="Weather App", font=("Arial", 16, "bold"))
label_title.pack(pady=(0, 10))

label_city = tk.Label(frame, text="Enter city:")
label_city.pack(anchor="w")

entry_city = tk.Entry(frame, width=30)
entry_city.pack(pady=(0, 10))

btn_get = tk.Button(frame, text="Get Weather", command=get_weather)
btn_get.pack(pady=(0, 10))

label_result = tk.Label(frame, text="", justify="left", font=("Consolas", 11))
label_result.pack(pady=(0, 10))

label_status = tk.Label(frame, text="", fg="gray")
label_status.pack(anchor="w")

root.mainloop()
