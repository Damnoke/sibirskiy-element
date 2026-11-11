import streamlit as st
import brain_models  # Импортируем весь модуль целиком!
from brain_core import MasterAI
from meta_agent import MetaArchitect

# Настройка страницы
st.set_page_config(page_title="Сибирский Элемент v3.5", page_icon="🏢", layout="wide")

# Инициализация
if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_proposal" not in st.session_state:
    st.session_state.current_proposal = None

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    # ВАЖНО: Обращаемся напрямую к brain_models.ALL_AGENTS
    for agent in brain_models.ALL_AGENTS:
        st.write(f"**{agent.name}**")
        st.progress(min(1.0, agent.accuracy / 100.0))
        st.caption(f"Точность: {agent.accuracy:.1f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"):
        council_decision = brain_models.hold_desire_council()
        st.info(council_decision)

    st.divider()
    st.subheader("🧬 Центр Эволюции")
    
    if st.button("🔍 Сканировать систему на застой"):
        architect = MetaArchitect()
        proposal = architect.analyze_system()
        
        if isinstance(proposal, dict):
            st.session_state.current_proposal = proposal 
        else:
            st.session_state.current_proposal = None
            st.success(proposal)

    if st.session_state.current_proposal:
        prop = st.session_state.current_proposal
        st.warning(f"⚠️ **Запрос на патч от {prop['target_agent']}!**")
        st.write(f"Текущая точность: {prop['current_accuracy']:.1f}%")
        st.info(f"💡 **Предложение ИИ:** {prop['message']}")
        
        if st.button("✅ Нанять агента"):
            # ВАЖНО: Вызываем функцию найма из brain_models
            success, msg = brain_models.hire_new_agent(prop['new_agent_name'], prop['category'])
            if success:
                st.success(msg)
                st.session_state.current_proposal = None
                st.rerun() 
            else:
                st.error(msg)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏢 Сибирский Элемент v3.5")
st.markdown("Генератор отделов: ИИ сам предлагает нанять новых сотрудников.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напишите ваш вопрос..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Анализирую..."):
            response = st.session_state.ai_brain.ask(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()

st.divider()
st.caption("Текущая сборка: v3.5 (Генератор Отделов) | Автор: Сибирский Элемент")
