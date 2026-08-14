import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///office_files.db")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
