import os
from dotenv import load_dotenv

load_dotenv()

class AppConfigs:

    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    CRON_SECRET = os.getenv("CRON_SECRET")
    DEBUG_VAR = os.getenv("DEBUG", "False").lower() == "true"