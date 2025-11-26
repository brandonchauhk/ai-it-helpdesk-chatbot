# services/openai_client.py
from openai import OpenAI
from config import OPENAI_API_KEY

# 建立 OpenAI Client，使用我們在 config.py 讀到的 API Key
client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_llm(system_prompt: str, user_message: str) -> str:
    """
    與 LLM 對話的通用封裝。
    system_prompt：告訴 AI 要扮演什麼角色
    user_message：使用者的輸入內容
    """
    response = client.chat.completions.create(
        model="gpt-5-nano",   # 如有需要可改成你帳戶可用的其他模型
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content.strip()
