# config.py
import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    "use_openai": True,
    "api_key_openai": os.getenv("OPENAI_API_KEY"),
    "use_huggingface": False,
    "api_key_huggingface": os.getenv("HUGGINGFACE_API_KEY"),
}
