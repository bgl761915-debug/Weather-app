# 🌤️ Weather App — Modern, No Login Needed

A clean and modern Python weather application powered by **Open‑Meteo**, a free weather service that requires:

- **No login**
- **No account**
- **No API key**
- **No rate limits for normal use**

This app is designed to be simple, fast, and easy to run.

---

## ✨ Features

- 🌗 **Dark / Light mode toggle**
- 🎨 **Rounded, card‑style UI**
- 🌍 **City search with automatic geocoding**
- 📡 **Live weather from Open‑Meteo**
- 🧭 **No login or API key required**

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:

```
requests
Pillow
```

---

## 🚀 How to Run

```bash
git clone https://github.com/bgl761915-debug/Weather-app.git
cd Weather-app

python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

A window will open.  
Type a city (e.g., **Brisbane**) → click **Get Weather** → weather info appears.

---

## 🧠 How It Works

This app uses two Open‑Meteo endpoints:

### 1. **Geocoding API**
Converts a city name into latitude & longitude:

```
https://geocoding-api.open-meteo.com/v1/search?name=Brisbane&count=1
```

### 2. **Forecast API**
Fetches current weather:

```
https://api.open-meteo.com/v1/forecast?latitude=-27.47&longitude=153.02&current_weather=true
```

The API returns:

- Temperature  
- Wind speed  
- Weather code  
- Time  

The app maps the **weather code** to a human‑readable description.

---

## 📁 Project Structure

```
Weather-app/
├─ main.py
├─ requirements.txt
└─ README.md
```

---

## 🎨 UI Features

- **Rounded card layout** for a modern look  
- **Dark/Light mode** toggle  
- **Threaded network requests** so the UI never freezes  

---

## 🛠️ Customization

You can easily modify:

- Colors, fonts, and layout  
- Weather code descriptions  
- Add hourly or daily forecast panels  
- Add location auto‑detect  

---

## 📜 License

This project is open-source and free to use.

---

Enjoy your modern, no‑login weather app! 🌤️
