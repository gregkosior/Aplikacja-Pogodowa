Aplikacja Pogodowa — prosty frontend do OpenWeatherMap (Flask)

Szybkie uruchomienie (PowerShell):
cd "Aplikacja Pogodowa"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
# ustaw .env z kluczem OPENWEATHER_API_KEY
python app.py

Uruchomienie z Docker:
docker build -t aplikacja-pogodowa Aplikacja\ Pogodowa
docker run --env-file Aplikacja\ Pogodowa/.env -p 5000:5000 aplikacja-pogodowa

Testy (lokalnie):
cd "Aplikacja Pogodowa"
pytest -q

CI:
Plik .github/workflows/ci.yml uruchamia testy przy push/pull requestach.
