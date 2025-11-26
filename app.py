import streamlit as st
from services.openai_client import chat_with_llm
from services.knowledge_base import search_faq

st.set_page_config(page_title="AI IT Helpdesk Chatbot", page_icon="💻")

st.title("💻 AI IT Helpdesk Chatbot")
st.caption("由傳統 IT Support 經驗延伸而成的 AI 助手 Demo（含 FAQ 知識庫 + 多種回應模式）")

st.markdown(
    """
這個 Demo 模擬企業內部的 IT Service Desk：

- 支援 **FAQ 知識庫查詢**
- 可切換 **三種回答模式**
- 回覆以繁體中文、條列式步驟呈現，方便員工跟隨操作
"""
)

with st.sidebar:
    st.header("關於這個 Demo")
    st.write(
        """
本系統示範：

- 如何將企業 IT FAQ 轉化為 AI 知識庫
- 結合 LLM 回覆實際 IT 問題
- 提供不同嚴謹程度的回答模式
"""
    )

    st.markdown("---")
    st.subheader("操作小提示")
    st.write(
        """
1. 先選擇回應模式  
2. 在下方輸入 IT 問題（例如 VPN、Outlook、印表機）  
3. 按「送出問題」，查看 AI 回覆
"""
    )

mode = st.selectbox(
    "選擇回應模式：",
    [
        "優先使用 FAQ + 再補充一般 IT 建議（建議）",
        "只使用 FAQ 知識庫作答（找不到就說不知道）",
        "一般 IT 顧問模式（不參考 FAQ）",
    ],
)
st.write("目前模式：", mode)

# 定義系統角色（之後可以依需求調整）
SYSTEM_PROMPT = """
你是一位友善、專業的企業 IT Helpdesk 專家，回答時請遵守以下原則：

1. 使用繁體中文。
2. 優先根據提供的 FAQ 知識庫內容作答，如 FAQ 足夠，就不要亂加不合理資訊。
3. 若 FAQ 沒有明確答案，再根據一般 IT 最佳實務補充建議。
4. 回答時請以「標題 + 條列式」整理：
   - 先給出簡短結論
   - 然後列出 3–7 個清晰步驟或檢查項目
5. 若使用者問題資訊不足，可以簡短詢問需要補充哪些資訊。
"""

# 使用 session_state 儲存對話紀錄
if "history" not in st.session_state:
    st.session_state.history = []

if "last_kb_context" not in st.session_state:
    st.session_state.last_kb_context = ""

# 使用者輸入區
user_input = st.text_area("請輸入你想問 AI 的問題：", height=100)

col1, col2 = st.columns(2)
with col1:
    send_clicked = st.button("送出問題")
with col2:
    clear_clicked = st.button("清除對話")

if clear_clicked:
    st.session_state.history = []

if send_clicked and user_input.strip():
    user_text = user_input.strip()

    # 先從 FAQ 知識庫搜尋相關內容
    kb_context = search_faq(user_text)

    # 記錄本次使用的 FAQ context，讓下方可選擇顯示
    st.session_state.last_kb_context = kb_context

    # 根據模式決定要給 LLM 的說明
    if mode.startswith("優先使用 FAQ"):
        full_prompt = f"""
以下是公司 IT FAQ 知識庫中與問題可能相關的內容：

{kb_context}

請你優先根據以上 FAQ 的內容提供解答。
如果 FAQ 中沒有合適答案，再根據一般 IT 最佳實務補充說明。

使用者的問題是：
{user_text}
"""
    elif mode.startswith("只使用 FAQ"):
        full_prompt = f"""
以下是公司 IT FAQ 知識庫中與問題可能相關的內容：

{kb_context}

請你「只」根據 FAQ 內容作答：
- 如果 FAQ 中已經有明確答案，請用條列方式整理給使用者。
- 如果 FAQ 中顯示「沒有相關 Q&A」或明顯找不到答案，請直接回答：
  「知識庫中暫時沒有這類問題的既定處理指引，請聯絡 IT 支援人員。」

使用者的問題是：
{user_text}
"""
    else:  # 一般 IT 顧問模式
        full_prompt = f"""
你現在不需要使用 FAQ 知識庫，而是以「一般企業 IT 顧問」身份作答。

請直接根據你的 IT 專業知識，用條列方式回答以下問題：

{user_text}
"""

    try:
        reply = chat_with_llm(SYSTEM_PROMPT, full_prompt)
    except Exception as e:
        # 顯示友善錯誤訊息給使用者
        st.error("呼叫 OpenAI API 時發生錯誤，請稍後再試，或聯絡系統管理員。")
        # 內部仍保留簡單錯誤內容（方便你自己 debug）
        st.write("（開發用訊息）錯誤內容：", e)
        reply = "抱歉，系統目前無法取得回應，請稍後再試。"

# 顯示對話紀錄
st.write("### 對話紀錄")
for role, msg in st.session_state.history:
    if role.startswith("👤"):
        st.markdown(f"**{role}：** {msg}")
    else:
        st.markdown(f"{role}：{msg}")

# 額外：可選擇查看本次回答所參考的 FAQ 內容
if st.session_state.last_kb_context:
    show_kb = st.checkbox("顯示本次回答所參考的 FAQ 內容", value=False)
    if show_kb:
        st.write("### 本次 FAQ 參考內容")
        st.code(st.session_state.last_kb_context)
