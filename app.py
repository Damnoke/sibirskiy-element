import streamlit as st
import brain_models
import importlib
import PyPDF2
import sqlite3
import time
from brain_core import MasterAI
from meta_agent import MetaArchitect

st.set_page_config(page_title="Сибирский Элемент v3.9.3", page_icon="🏢", layout="wide")

if "ai_brain" not in st.session_state or st.session_state.get("version") != "3.9.3":
    st.session_state.ai_brain = MasterAI()
    st.session_state.version = "3.9.3"

if "messages" not in st.session_state: st.session_state.messages = []
if "current_proposal" not in st.session_state: st.session_state.current_proposal = None
if "learn_msg" not in st.session_state: st.session_state.learn_msg = None

# Функция логирования ошибок для аптек
def log_error_to_db(query, response):
    conn = sqlite3.connect("agents_database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS error_logs
                 (id INTEGER PRIMARY KEY, query TEXT, response TEXT, timestamp TEXT)''')
    c.execute("INSERT INTO error_logs (query, response, timestamp) VALUES (?, ?, ?)", 
              (query, response, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

with st.sidebar:
    st.header("🏆 Таблица лидеров")
    importlib.reload(brain_models) 
    
    for agent in brain_models.ALL_AGENTS:
        st.write(f"**{agent.name}** [{agent.category}] — {agent.get_level()}")
        st.progress(min(1.0, max(0.0, agent.accuracy / 100.0)))
        st.caption(f"Точность: {agent.accuracy:.1f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    st.subheader("📚 Библиотека")
    
    if st.session_state.learn_msg:
        st.success(st.session_state.learn_msg)
        st.session_state.learn_msg = None

    agent_names = [a.name for a in brain_models.ALL_AGENTS]
    selected_agent = st.selectbox("Выберите агента:", agent_names)
    
    tab1, tab2 = st.tabs(["📝 Текст", "📎 Файл (PDF/TXT)"])
    
    with tab1:
        text_input = st.text_area("Вставьте текст:", height=100)
        if st.button("Прочитать текст"):
            if text_input.strip():
                agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
                st.session_state.learn_msg = agent.read_book(text_input)
                st.rerun()
                
    with tab2:
        uploaded_file = st.file_uploader("Загрузите PDF или TXT", type=["pdf", "txt"])
        if uploaded_file is not None:
            if st.button("Прочитать файл"):
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
                else:
                    st.error("Не удалось прочитать файл.")
            
    st.divider()
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"): st.info(brain_models.hold_desire_council())
    
    st.divider()
    st.subheader("🧬 Центр Эволюции")
    if st.button("🔍 Сканировать систему"):
        proposal = MetaArchitect().analyze_system()
        if isinstance(proposal, dict): st.session_state.current_proposal = proposal 
        else:
            st.session_state.current_proposal = None
            st.success(proposal)

    if st.session_state.current_proposal:
        prop = st.session_state.current_proposal
        st.warning(f"⚠️ **Патч от {prop['target_agent']}!**")
        st.info(f"💡 {prop['message']}")
        if st.button("✅ Нанять агента"):
            success, msg = brain_models.hire_new_agent(prop['new_agent_name'], prop['category'])
            if success:
                st.success(msg)
                st.session_state.current_proposal = None
                st.rerun() 

st.title("🏢 Сибирский Элемент v3.9.3")
st.markdown("Аптечный протокол: Фильтр симптомов и ссылки на источники!")

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        content = msg["content"]
        
        if msg["role"] == "assistant" and "[AGENT_ID:" in content:
            parts = content.split("\n\n[AGENT_ID:")
            text_part = parts[0]
            agent_name = parts[1].replace("]", "") if len(parts) > 1 else "Неизвестный"
            
            st.markdown(text_part)
            
            # Кнопки: Лайк, Дизлайк, Ошибка
            col1, col2, col3, _ = st.columns([1, 1, 1, 7])
            with col1:
                if st.button("👍", key=f"like_{i}"):
                    agent = next((a for a in brain_models.ALL_AGENTS if a.name == agent_name), None)
                    if agent:
                        agent.accuracy = min(100.0, agent.accuracy + 1.5)
                        brain_models.save_agents()
                        st.toast(f"Агент {agent_name} доволен! (+1.5%)")
                        st.rerun()
            with col2:
                if st.button("👎", key=f"dislike_{i}"):
                    agent = next((a for a in brain_models.ALL_AGENTS if a.name == agent_name), None)
                    if agent:
                        agent.accuracy = max(0.0, agent.accuracy - 1.5)
                        brain_models.save_agents()
                        st.toast(f"Агент {agent_name} получил наказание! (-1.5%)")
                        st.rerun()
            with col3:
                if st.button("🚩", key=f"error_{i}"):
                    previous_msg = st.session_state.messages[i-1]["content"] if i > 0 else ""
                    log_error_to_db(previous_msg, text_part)
                    st.toast("Ошибка зафиксирована в базе! (На дообучение)")
        else:
            st.markdown(content)

st.markdown("---")
mode_selection = st.radio(
    "Режим:", 
    ["🚀 Chat", "🌐 Search", "🔍🧠 Search+Think", "🧠 SibThink"], 
    horizontal=True, 
    label_visibility="collapsed"
)
mode_map = {
    "🚀 Chat": "normal", 
    "🌐 Search": "search", 
    "🔍🧠 Search+Think": "search_think", 
    "🧠 SibThink": "sibthink"
}
current_mode = mode_map[mode_selection]

if prompt := st.chat_input("Напишите ваш вопрос..."):
    with st.chat_message("user"): 
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner(f"Режим: {mode_selection}. Думаю..."):
            response = st.session_state.ai_brain.ask(prompt, mode=current_mode)
            display_response = response.split("\n\n[AGENT_ID:")[0] if "[AGENT_ID:" in response else response
            st.markdown(display_response)
            
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()

st.caption("Текущая сборка: v3.9.3 (Аптечный протокол) | Автор: Сибирский Элемент")
