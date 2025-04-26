import os
from dotenv import load_dotenv

BOT_ID = '@chAI_news'
if os.path.isfile(".env"):
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
