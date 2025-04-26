import os
from dotenv import load_dotenv

BOT_ID = '@chAI_news'
if os.path.isfile(".env"):
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
    gpt_model = os.getenv("gpt_model")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
