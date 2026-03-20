# 🌤️ Weather App — Animated, Modern, Beautiful

A fully modern Python weather application featuring:

- 🔥 **Animated weather icons (GIFs)**
- 🌗 **Dark / Light mode toggle**
- 🖼️ **Dynamic background images that change with the weather**
- 🎨 **Rounded, card‑style UI**
- ⚡ **Loading animation while fetching data**
- 🌍 **OpenWeatherMap API integration**
- 💻 **Cross‑platform (Linux, Windows, macOS)**

This app is designed to look clean, modern, and visually impressive while staying lightweight and easy to run.

---

## ✨ Features

- Enter any city and instantly get:
  - Temperature (°C)
  - Weather condition
  - Description
  - Feels like temperature
  - Humidity
  - Wind speed
- Animated icons for:
  - Clear sky
  - Clouds
  - Rain
  - Drizzle
  - Thunderstorm
  - Snow
  - Mist / Fog / Haze
- Background image changes based on weather
- Smooth loading indicator
- Dark and Light mode switch
- Rounded UI card for a modern look

---

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Dependencies:

```
requests
Pillow
```

---

## 🔑 API Key Setup

This app uses **OpenWeatherMap**.

1. Create a free account at:  
   https://openweathermap.org/

2. Go to **API Keys**

3. Copy your key

4. Open `main.py` and replace:

```python
API_KEY = "YOUR_API_KEY_HERE"
```

---

## 🚀 How to Run

```bash
git clone https://github.com/YOUR_USERNAME/Weather-app.git
cd Weather-app

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

---

## 📁 Project Structure

```
Weather-app/
├─ main.py
├─ requirements.txt
└─ README.md
```

---

## 🖼️ Screenshots (Optional)

You can add screenshots here later:

```
![Screenshot](images/screenshot1.png)
![Screenshot](images/screenshot2.png)
```

---

## 🧠 How It Works

- Fetches weather data from OpenWeatherMap’s `/weather` endpoint.
- Selects a matching animated GIF icon.
- Downloads a matching background image.
- Updates the UI with:
  - Temperature
  - Description
  - Extra details
- Animates GIF frames using PIL + Tkinter.
- Uses a canvas background + rounded card overlay.

---

## 🛠️ Customization

You can easily customize:

- Background images  
- Animated icons  
- Colors  
- Fonts  
- UI layout  
- Add forecast panels  
- Add location auto‑detect  

---

## 📜 License

This project is open-source and free to use.

---

## ❤️ Credits

- Weather data: **OpenWeatherMap**
- Background images: Stock photography
- Animated icons: Custom GIFs hosted on Imgur

---

Enjoy your beautiful animated weather app! 🌤️
