import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import io
import threading

API_KEY = "YOUR_API_KEY_HERE"  # <--- PUT YOUR KEY HERE
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

BG_IMAGES = {
    "Clear": "https://i.imgur.com/7uZpQqH.jpg",
    "Clouds": "https://i.imgur.com/6pQ0pQH.jpg",
    "Rain": "https://i.imgur.com/1pQ0pQH.jpg",
    "Drizzle": "https://i.imgur.com/1pQ0pQH.jpg",
    "Thunderstorm": "https://i.imgur.com/4pQ0pQH.jpg",
    "Snow": "https://i.imgur.com/5pQ0pQH.jpg",
    "Mist": "https://i.imgur.com/6pQ0pQH.jpg",
    "Fog": "https://i.imgur.com/6pQ0pQH.jpg",
    "Haze": "https://i.imgur.com/6pQ0pQH.jpg",
}

ICON_GIFS = {
    "Clear": "https://i.imgur.com/5Z3p0yP.gif",
    "Clouds": "https://i.imgur.com/1Z3p0yP.gif",
    "Rain": "https://i.imgur.com/2Z3p0yP.gif",
    "Drizzle": "https://i.imgur.com/2Z3p0yP.gif",
    "Thunderstorm": "https://i.imgur.com/3Z3p0yP.gif",
    "Snow": "https://i.imgur.com/4Z3p0yP.gif",
    "Mist": "https://i.imgur.com/1Z3p0yP.gif",
    "Fog": "https://i.imgur.com/1Z3p0yP.gif",
    "Haze": "https://i.imgur.com/1Z3p0yP.gif",
}


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

    def start(self, delay=100):
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


def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params, timeout=10)
    data = resp.json()
    if data.get("cod") != 200:
        return None
    return {
        "temp": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"].title(),
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
    }


def fetch_image(url, size=None):
    try:
        data = requests.get(url, timeout=10).content
        img = Image.open(io.BytesIO(data)).convert("RGBA")
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.dark_mode = True
        self.bg_image = None

        self.root.title("Weather App")
        self.root.geometry("480x640")
        self.root.resizable(False, False)

        self.dark_bg = "#101820"
        self.dark_card = "#182430"
        self.dark_fg = "#F5F5F5"
        self.light_bg = "#E6F0FF"
        self.light_card = "#FFFFFF"
        self.light_fg = "#101820"

        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.card = tk.Frame(self.canvas, bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=520)

        self.title_label = tk.Label(self.card, text="Weather", font=("Segoe UI", 22, "bold"))
        self.city_entry = ttk.Entry(self.card, font=("Segoe UI", 14))
        self.search_btn = ttk.Button(self.card, text="Get Weather", command=self.on_search)
        self.loading_label = tk.Label(self.card, text="", font=("Segoe UI", 10, "italic"))

        self.icon_label = tk.Label(self.card, bd=0)
        self.animated_icon = AnimatedIcon(self.icon_label)

        self.result_label = tk.Label(self.card, text="", font=("Segoe UI", 16), justify="center")
        self.extra_label = tk.Label(self.card, text="", font=("Segoe UI", 11), justify="center")

        self.theme_btn = ttk.Button(self.card, text="Dark / Light", command=self.toggle_theme)

        self.title_label.pack(pady=(20, 10))
        self.city_entry.pack(pady=5, ipadx=5, ipady=5)
        self.search_btn.pack(pady=5)
        self.loading_label.pack(pady=(0, 5))
        self.icon_label.pack(pady=10)
        self.result_label.pack(pady=5)
        self.extra_label.pack(pady=5)
        self.theme_btn.pack(side="bottom", pady=15)

        self.apply_theme()
        self.set_background("Clear")

    def apply_theme(self):
        if self.dark_mode:
            bg, card, fg = self.dark_bg, self.dark_card, self.dark_fg
        else:
            bg, card, fg = self.light_bg, self.light_card, self.light_fg

        self.canvas.configure(bg=bg)
        self.card.configure(bg=card)
        for w in (self.title_label, self.loading_label, self.result_label, self.extra_label, self.icon_label):
            w.configure(bg=card, fg=fg if w is not self.icon_label else None)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TEntry", fieldbackground=card, background=card, foreground=fg)
        style.configure("TButton", background="#3A7BD5", foreground="white", padding=6, relief="flat")
        style.map("TButton", background=[("active", "#356AC3")])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def set_background(self, condition):
        url = BG_IMAGES.get(condition, BG_IMAGES["Clouds"])
        img = fetch_image(url, size=(480, 640))
        if img:
            self.bg_image = img
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        else:
            self.canvas.configure(bg=self.dark_bg if self.dark_mode else self.light_bg)

    def set_loading(self, is_loading):
        self.loading_label.config(text="Loading..." if is_loading else "")
        self.search_btn.config(state="disabled" if is_loading else "normal")

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
        self.root.after(0, lambda: self.update_ui(city, data))

    def update_ui(self, city, data):
        self.set_loading(False)

        if not data:
            self.result_label.config(text="City not found or request failed.")
            self.extra_label.config(text="")
            return

        condition = data["condition"]
        self.set_background(condition)

        self.result_label.config(
            text=f"{city.title()}\n{data['temp']}°C\n{data['description']}"
        )
        self.extra_label.config(
            text=f"Feels like: {data['feels_like']}°C\n"
                 f"Humidity: {data['humidity']}%\n"
                 f"Wind: {data['wind']} m/s"
        )

        gif_url = ICON_GIFS.get(condition, ICON_GIFS["Clouds"])
        self.animated_icon.load_from_url(gif_url)
        self.animated_icon.start(delay=120)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
