# 💻 AI IT Helpdesk Chatbot

這是一個模擬企業內部 IT Service Desk 的 AI Chatbot Demo，由傳統 IT Support 經驗延伸而成。  
系統結合 **FAQ 知識庫** 與 **大型語言模型（LLM）**，協助員工以自然語言查詢 IT 問題。

---

## 🌟 功能簡介

- ✅ 支援 **企業 IT FAQ 知識庫**（以 CSV 管理）
- ✅ 能以繁體中文回答常見 IT 問題（VPN、Outlook、印表機、帳號密碼等）
- ✅ 提供 **三種回答模式**：
  1. 優先使用 FAQ + 再補充一般 IT 建議
  2. 僅根據 FAQ 回答（找不到就說不知道）
  3. 一般 IT 顧問模式（不參考 FAQ）
- ✅ 介面以 **Streamlit** 製作，適合 Demo 與內部 PoC（Proof of Concept）
- ✅ 可選擇顯示本次回答所參考的 FAQ 內容，方便 Debug 與解釋

---

## 🧱 技術架構

- 語言：Python 3.11
- 前端 / UI：Streamlit
- LLM：OpenAI Chat Completions API（可替換為 Azure OpenAI 等）
- 資料存放：CSV（`data/faq.csv`）
- 設定與機密：
  - `.env` 用於存放 `OPENAI_API_KEY`
  - `config.py` 負責載入環境變數

---

## 📂 專案結構

```text
helpdesk_chatbot/
├─ app.py                # Streamlit 主介面
├─ config.py             # 載入 .env 中的 OPENAI_API_KEY
├─ requirements.txt      # 專案相依套件
├─ data/
│  └─ faq.csv            # IT FAQ 知識庫（category, question, answer）
├─ services/
│  ├─ __init__.py
│  ├─ openai_client.py   # OpenAI API 封裝
│  └─ knowledge_base.py  # FAQ 讀取與關鍵字搜尋
└─ venv/                 # Python 虛擬環境（不需上版控）
```

## 🚀 安裝與執行方式, 建立虛擬環境

1️⃣ 建立虛擬環境
python -m venv venv
venv\Scripts\activate # Windows

# 或

source venv/bin/activate # macOS / Linux

2️⃣ 安裝相依套件
pip install -r requirements.txt

3️⃣ 建立 .env 並設定 OpenAI API Key
OPENAI_API_KEY=你的 API 金鑰
⚠️ 注意：.env 不應加入 Git 或公開儲存庫。

4️⃣ 準備 FAQ 資料
檔案位置：
data/faq.csv
範例格式（可自行擴充）：
category,question,answer
VPN,VPN 連接不到公司網絡,請確認網絡正常、帳號密碼正確，必要時重新啟動設備或聯絡 IT。

5️⃣ 啟動系統
streamlit run app.py
開啟網址（通常會自動開啟）：
http://localhost:8501

## 🧠 回應模式說明

系統內建三種模式：

優先使用 FAQ（預設）
先用 FAQ 回答
FAQ 不夠時由 LLM 補充 IT 最佳實務

僅使用 FAQ
完全依 FAQ 回答
找不到則提示「知識庫無相關內容」

一般 IT 顧問模式
不參考 FAQ
以一般 IT Support 的方式回覆

## 🔍 FAQ 知識庫與可解釋性

Chatbot 支援：
顯示「本次回覆所參考的 FAQ 內容」
透明化資料來源
協助 Debug 和協作

這能讓 IT 部門清楚知道：
AI 回答是否符合公司政策
哪些 FAQ 需要優化

## 📌 未來可延伸方向（Roadmap）

加入向量資料庫（如 Chroma、FAISS）
依員工角色自動調整回答
串接 ServiceNow / JIRA / Freshservice 工單系統
加入多語言支援
部署到企業內網伺服器或雲端（Azure / AWS）

## 👤 作者簡介

擁有 20+ 年企業 IT Support / Information Systems 經驗  
熟悉 AD、VPN、Outlook、Printer、帳號管理等企業日常支援流程  
2024–2025 期間完成多項 AI / LLM 相關課程（Coursera / Google 等）  
致力於將 AI 技術應用於企業 IT 支援、自動化與實務場景中
