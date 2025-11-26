# config.py
import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("請在 .env 檔案中設定 OPENAI_API_KEY")
