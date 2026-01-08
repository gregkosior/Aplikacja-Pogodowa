import os
import time
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
app = Flask(__name__)

# cache: {q: (timestamp, data)}
CACHE = {}
CACHE_TTL = 600  # 10 minutes

def get_icon_url(icon_code):
    if not icon_code:
        return None
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def fetch_weather_city(city):
    city = city.strip()
    if not city:
        return {"error": "Podaj nazwę miasta."}
    now = time.time()
    key = city.lower()
    cached = CACHE.get(key)
    if cached and now - cached[0] < CACHE_TTL:
        return cached[1]
    if not API_KEY:
        return {"error": "Brak klucza API. Ustaw OPENWEATHER_API_KEY w .env"}
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "pl"}
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data.get("cod") not in (200, "200"):
            return {"error": data.get("message", "Błąd API")}
        # enrich with icon url
        weather = data.get("weather")
        if weather and isinstance(weather, list) and weather:
            data["icon_url"] = get_icon_url(weather[0].get("icon"))
        else:
            data["icon_url"] = None
        CACHE[key] = (now, data)
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Błąd połączenia z API: {e}"}

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("city", "").strip()
    weather = None
    if q:
        weather = fetch_weather_city(q)
    return render_template("index.html", weather=weather, query=q)

@app.route("/_health")
def health():
    key = os.getenv("OPENWEATHER_API_KEY")
    masked = None
    if key:
        masked = key[:4] + "..." + key[-4:]
    return jsonify(status="ok", api_key_present=bool(key), api_key_masked=masked)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
