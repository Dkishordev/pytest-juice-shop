import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    BASE_URL = os.getenv(
        "BASE_URL",
        "http://127.0.0.1:3000"
    )

    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "http://127.0.0.1:3000"
    )

    TEST_EMAIL = os.getenv(
        "TEST_EMAIL",
        "automation@example.com"
    )

    TEST_PASSWORD = os.getenv(
        "TEST_PASSWORD",
        "TestPassword123!"
    )

    DB_PATH = os.getenv(
        "DB_PATH",
        str(ROOT_DIR / "data" / "juiceshop.sqlite")
    )
    
    HEADLESS = os.getenv(
        "HEADLESS", 
        "false").lower() == "false"
    
    BROWSER = os.getenv(
    "BROWSER", "chromium"
    )  

    DEFAULT_TIMEOUT_MS = int(os.getenv(
        "DEFAULT_TIMEOUT_MS", "10000")
    )


settings = Settings()