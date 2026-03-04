import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")
RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)
RABBIT_VHOST = os.getenv("RABBIT_VHOST")

QUEUE_NAME = os.getenv("QUEUE_NAME")

MAX_TOKEN = os.getenv("MAX_TOKEN")
API_KEY = os.getenv("API_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")

RABBIT_URL= f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/{RABBIT_VHOST}'