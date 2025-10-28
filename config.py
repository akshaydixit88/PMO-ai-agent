from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
RECIPIENTS = [r.strip() for r in os.getenv("GMAIL_RECIPIENTS", "").split(",") if r]