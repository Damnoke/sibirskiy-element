import streamlit as st
import brain_models
import PyPDF2
import sqlite3
import time
from brain_core import MasterAI

# --- НАСТРОЙКА СТРАНИЦЫ И ДИЗАЙН (ИСПРАВЛЕННЫЙ) ---
st.set_page_config(page_title="Сибирский Элемент - Аптека", page_icon="💊", layout="wide")

st.markdown("""
<style>
    /* Делаем фон мягким, но оставляем текст темным */
    .stApp { background-color: #f8f9fa; }
    
    /* Все заголовки и текст делаем контрастными */
    h1, h2, h3 { color: #0d6efd !important; }
    p, span, div, label { color: #212529 !important; }
    
    /* Кнопки */
    .stButton>button {
        background-color: #0d6efd; color: white !important; border-radius: 8px;
        font-weight: bold;
    }
    
    /* Поле ввода делаем заметным */
    .stChatInput textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 1px solid #0d6efd !important;
    }
    
    /* Блоки ответов ИИ */
    .stChatMessage { 
        background-color: #ffffff; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

if "ai_brain" not in st.session_state or st.session_state.get("version") != "4.6":
    st.session_state.ai_brain = MasterAI()
    st.session_state.version = "4.6"

if "messages" not in st.session_state: st.session_state.messages = []
if "learn_msg" not in st.session_state: st.session_state.learn_msg = None

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=60)
    st.title("Сибирский Элемент")
    st.caption("Интеллектуальный помощник провизора")
    
    st.divider()
    with st.expander("⚙️ Панель Архитектора (Обучение)"):
        agent_names = [a.name for a in brain_models.ALL_AGENTS]
        selected_agent = st.selectbox("Выберите отдел:", agent_names)
        
        text_input = st.text_area("Вставьте инструкцию:", height=100)
        if st.button("Обучить текст"):
            if text_input.strip():
                agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
                st.session_state.learn_msg = agent.read_book(text_input)
                st.rerun()
        
        uploaded_file = st.file_uploader("Загрузите файл (PDF/TXT)", type=["pdf", "txt"])
        if uploaded_file is not None:
            if st.button("Обучить файл"):
                file_text = ""
                if uploaded_file.type == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        file_text += page.extract_text() + " "
                else:
                    file_text = uploaded_file.read().decode("utf-8")
                if file_text:
                    agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
                    st.session_state.learn_msg = agent.read_book(file_text)
                    st.rerun()

    with st.expander("🚨 Жалобы"):
        conn = sqlite3.connect("agents_database.db")
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='error_logs'")
        if c.fetchone():
            c.execute("SELECT query, response FROM error_logs ORDER BY id DESC LIMIT 5")
            for err in c.fetchall():
                st.warning(f"Вопрос: {err[0]}")
        else: st.info("Жалоб нет.")
        conn.close()

    with st.expander("🧠 Блок обучения"):
        conn = sqlite3.connect("agents_database.db")
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='unanswered_questions'")
        if c.fetchone():
            c.execute("SELECT question FROM unanswered_questions ORDER BY id DESC LIMIT 5")
            for unk in c.fetchall():
                st.info(f"Вопрос: {unk[0]}")
        else: st.success("Я знаю всё!")
        conn.close()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("💊 Аптечный помощник")
st.markdown("Введите название препарата, симптом или вопрос. Если я не знаю — я запишу это в блок обучения.")

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        content = msg["content"]
        
        if msg["role"] == "assistant" and "[AGENT_ID:" in content:
            parts = content.split("\n\n[AGENT_ID:")
            text_part = parts[0]
            agent_name = parts[1].replace("]", "") if len(parts) > 1 else "Неизвестный"
            
            st.markdown(text_part)
            
            col1, col2, col3, _ = st.columns([1, 1, 1, 7])
            with col1:
                if st.button("👍", key=f"like_{i}"): st.toast("Спасибо!")
            with col2:
                if st.button("👎", key=f"dislike_{i}"): st.toast("Оценка снижена.")
            with col3:
                if st.button("🚩", key=f"error_{i}"):
                    prev = st.session_state.messages[i-1]["content"] if i > 0 else ""
                    brain_models.log_error_to_db(prev, text_part)
                    st.toast("Жалоба зафиксирована!")
        else:
            st.markdown(content)

st.markdown("---")
mode_selection = st.radio(
    "Режим:", ["🚀 Авто-режим", "🌐 Поиск в сети", "🧠 SibThink (Анализ)"], 
    horizontal=True, label_visibility="collapsed"
)
mode_map = {"🚀 Авто-режим": "normal", "🌐 Поиск в сети": "search", "🧠 SibThink (Анализ)": "sibthink"}
current_mode = mode_map.get(mode_selection, "normal")

if prompt := st.chat_input("Введите запрос..."):
    with st.chat_message("user"): st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Ищу..."):
            response = st.session_state.ai_brain.ask(prompt, mode=current_mode)
            display_response = response.split("\n\n[AGENT_ID:")[0] if "[AGENT_ID:" in response else response
            st.markdown(display_response)
            
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()
