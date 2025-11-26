# services/knowledge_base.py
import pandas as pd
from pathlib import Path

# 設定 FAQ 檔案路徑
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "faq.csv"

def load_faq() -> pd.DataFrame:
    """載入 FAQ CSV，欄位：category, question, answer。"""
    df = pd.read_csv(DATA_PATH)
    return df

def search_faq(user_query: str, k: int = 5) -> str:
    """
    先檢查：FAQ 的問題文字是否出現在使用者的提問中（適合中文問句加「怎麼辦」、「如何處理」等）
    若沒有，再用簡單的部分關鍵字搜尋。
    """
    df = load_faq()

    # 1️⃣ 第一層：檢查「FAQ 問題」是否是「使用者問題」的一部分
    # 例如：FAQ = "VPN 連接不到公司網絡"
    # 使用者 = "VPN 連接不到公司網絡怎麼辦？" → 會 match
    mask_exact = df["question"].apply(
        lambda q: isinstance(q, str) and q.strip() != "" and q in user_query
    )

    if mask_exact.any():
        selected = df[mask_exact].head(k)
    else:
        # 2️⃣ 第二層：用較短的關鍵字做模糊搜尋（避免整句太長）
        # 取使用者問題前 6 個字作為簡易關鍵字（你之後可再調）
        keyword = user_query[:6]

        mask_fuzzy = df["question"].str.contains(keyword, case=False, na=False) | \
                     df["answer"].str.contains(keyword, case=False, na=False)

        selected = df[mask_fuzzy].head(k)

    if selected.empty:
        return "（知識庫中沒有直接相關的 Q&A。）"

    context_lines = []
    for _, row in selected.iterrows():
        context_lines.append(f"Q: {row['question']}\nA: {row['answer']}")
    return "\n\n".join(context_lines)
