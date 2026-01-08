from dotenv import load_dotenv
from pathlib import Path
import os
BASE_DIR = Path.cwd()
print("env exists:", (BASE_DIR / '.env').exists())
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)
print("KEY=", os.getenv('OPENWEATHER_API_KEY'))
