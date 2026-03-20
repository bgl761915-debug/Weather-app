import tkinter as tk
import requests

def get_weather():
    city = entry_city.get().strip()
    if not city:
        label_status.config(text="Please enter a city.")
        return

    url = f"https://wttr.in/{city}?format=j1"

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        area = data["nearest_area"][0]["areaName"][0]["value"]
        region = data["nearest_area"][0]["region"][0]["value"]
        country = data["nearest_area"][0]["country"][0]["value"]

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        condition = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_kph = current["windspeedKmph"]

        result_text = (
            f"{area}, {region}, {country}\n"
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
root.title("Weather App (No API Key Needed)")

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
