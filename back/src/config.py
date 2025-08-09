import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel

load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")
PORT = os.environ.get("MAIL_PORT", 465)
API_KEY = os.environ.get("API_KEY")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str