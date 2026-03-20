import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import io
import threading

# -----------------------------
# Weather assets (GIFs + backgrounds)
# -----------------------------

BG_IMAGES = {
    "clear": "https://i.imgur.com/7uZpQqH.jpg",
    "clouds": "https://i.imgur.com/6pQ0pQH.jpg",
    "rain": "https://i.imgur.com/1pQ0pQH.jpg",
    "snow": "https://i.imgur.com/5pQ0pQH.jpg",
    "fog": "https://i.imgur.com/6pQ0pQH.jpg",
    "storm": "https://i.imgur.com/4pQ0pQH.jpg",
}

ICON_GIFS = {
    "clear": "https://i.imgur.com/5Z3p0yP.gif",
    "clouds": "https://i.imgur.com/1Z3p0yP.gif",
    "rain": "https://i.imgur.com/2Z3p0yP.gif",
    "snow": "https://i.imgur.com/4Z3p0yP.gif",
    "fog": "https://i.imgur.com/1Z3p0yP.gif",
    "storm": "https://i.imgur.com/3Z3p0yP.gif",
}

# -----------------------------
# Weather code mapping
# -----------------------------

def map_weather_code(code: int):
    if code == 0:
        return "clear", "Clear sky"
    if code in (1, 2, 3):
        return "clouds", "Partly cloudy" if code in (1, 2) else "Overcast"
    if code in (45, 48):
        return "fog", "Foggy"
    if code in (51, 53, 55, 56, 57):
        return "rain", "Drizzle"
    if code in (61, 63, 65, 66, 67, 80, 81, 82):
        return "rain", "Rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "snow", "Snow"
    if code in (95, 96, 99):
        return "storm", "Thunderstorm"
    return "clouds", "Cloudy"

# -----------------------------
# Animated GIF loader
# -----------------------------

class AnimatedIcon:
    def __init__(self, label):
        self.label = label
        self.frames = []
        self.current = 0
        self.animating = False

    def load_from_url(self, url, size=(120, 120)):
        self.frames.clear()
        self.current = 0
        try:
            data = requests.get(url, timeout=10).content
            gif = Image.open(io.BytesIO(data))
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                frame = frame.resize(size, Image.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame))
        except Exception:
            self.frames = []

    def start(self, delay=120):
        if not self.frames:
            self.label.config(image="")
            return
        self.animating = True
        self._animate(delay)

    def stop(self):
        self.animating = False

    def _animate(self, delay):
        if not self.animating or not self.frames:
            return
        frame = self.frames[self.current]
        self.label.config(image=frame)
        self.label.image = frame
        self.current = (self.current + 1) % len(self.frames)
        self.label.after(delay, lambda: self._animate(delay))

# -----------------------------
# API calls (Open‑Meteo)
# -----------------------------

def geocode_city(name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": name, "count": 1}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    results = data.get("results")
    if not results:
        return None
    res = results[0]
    return {
        "lat": res["latitude"],
        "lon": res["longitude"],
        "name": res["name"],
        "country": res.get("country", ""),
    }

def get_weather(city: str):
    geo = geocode_city(city)
    if not geo:
        return None

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": geo["lat"],
        "longitude": geo["lon"],
        "current_weather": True,
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    current = data.get("current_weather")
    if not current:
        return None

    code = int(current["weathercode"])
    cond_key, desc = map_weather_code(code)

    return {
        "city": geo["name"],
        "country": geo["country"],
        "temp": current["temperature"],
        "wind": current["windspeed"],
        "code": code,
        "condition_key": cond_key,
        "description": desc,
    }

# -----------------------------
# Image fetch helper
# -----------------------------

def fetch_image(url, size=None):
    try:
        data = requests.get(url, timeout=10).content
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

# -----------------------------
# Main UI class
# -----------------------------

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.dark_mode = True
        self.bg_image = None

        self.root.title("Weather App")
        self.root.geometry("480x640")
        self.root.resizable(False, False)

        # Colors
        self.dark_bg = "#101820"
        self.dark_card = "#182430"
        self.dark_fg = "#F5F5F5"
        self.light_bg = "#E6F0FF"
        self.light_card = "#FFFFFF"
        self.light_fg = "#101820"

        # Background canvas
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Rounded card
        self.card = tk.Frame(self.canvas, bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=520)

        # Widgets
        self.title_label = tk.Label(self.card, text="Weather", font=("Segoe UI", 22, "bold"))
        self.city_entry = ttk.Entry(self.card, font=("Segoe UI", 14))
        self.search_btn = ttk.Button(self.card, text="Get Weather", command=self.on_search)
        self.loading_label = tk.Label(self.card, text="", font=("Segoe UI", 10, "italic"))

        self.icon_label = tk.Label(self.card, bd=0)
        self.animated_icon = AnimatedIcon(self.icon_label)

        self.result_label = tk.Label(self.card, text="", font=("Segoe UI", 16), justify="center")
        self.extra_label = tk.Label(self.card, text="", font=("Segoe UI", 11), justify="center")

        self.theme_btn = ttk.Button(self.card, text="Dark / Light", command=self.toggle_theme)

        # Layout
        self.title_label.pack(pady=(20, 10))
        self.city_entry.pack(pady=5, ipadx=5, ipady=5)
        self.search_btn.pack(pady=5)
        self.loading_label.pack(pady=(0, 5))
        self.icon_label.pack(pady=10)
        self.result_label.pack(pady=5)
        self.extra_label.pack(pady=5)
        self.theme_btn.pack(side="bottom", pady=15)

        self.apply_theme()
        self.set_background("clear")

    # -----------------------------
    # Theme
    # -----------------------------

    def apply_theme(self):
        if self.dark_mode:
            bg, card, fg = self.dark_bg, self.dark_card, self.dark_fg
        else:
            bg, card, fg = self.light_bg, self.light_card, self.light_fg

        self.canvas.configure(bg=bg)
        self.card.configure(bg=card)

        for w in (self.title_label, self.loading_label, self.result_label, self.extra_label):
            w.configure(bg=card, fg=fg)

        self.icon_label.configure(bg=card)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TEntry", fieldbackground=card, background=card, foreground=fg)
        style.configure("TButton", background="#3A7BD5", foreground="white", padding=6, relief="flat")
        style.map("TButton", background=[("active", "#356AC3")])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    # -----------------------------
    # Background
    # -----------------------------

    def set_background(self, condition_key):
        url = BG_IMAGES.get(condition_key, BG_IMAGES["clouds"])
        img = fetch_image(url, size=(480, 640))
        if img:
            self.bg_image = img
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

    # -----------------------------
    # Loading state
    # -----------------------------

    def set_loading(self, is_loading):
        self.loading_label.config(text="Loading..." if is_loading else "")
        self.search_btn.config(state="disabled" if is_loading else "normal")

    # -----------------------------
    # Search
    # -----------------------------

    def on_search(self):
        city = self.city_entry.get().strip()
        if not city:
            self.result_label.config(text="Enter a city name.")
            return

        self.set_loading(True)
        self.animated_icon.stop()
        self.icon_label.config(image="")
        self.result_label.config(text="")
        self.extra_label.config(text="")

        threading.Thread(target=self.fetch_and_update, args=(city,), daemon=True).start()

    def fetch_and_update(self, city):
        try:
            data = get_weather(city)
        except Exception:
            data = None
        self.root.after(0, lambda: self.update_ui(data))

    # -----------------------------
    # UI update
    # -----------------------------

    def update_ui(self, data):
        self.set_loading(False)

        if not data:
            self.result_label.config(text="City not found or request failed.")
            self.extra_label.config(text="")
            return

        cond_key = data["condition_key"]
        self.set_background(cond_key)

        location = data["city"]
        if data["country"]:
            location += f", {data['country']}"

        self.result_label.config(
            text=f"{location}\n{data['temp']}°C\n{data['description']}"
        )
        self.extra_label.config(
            text=f"Wind: {data['wind']} km/h\nCode: {data['code']}"
        )

        gif_url = ICON_GIFS.get(cond_key, ICON_GIFS["clouds"])
        self.animated_icon.load_from_url(gif_url)
        self.animated_icon.start()

# -----------------------------
# Run app
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
