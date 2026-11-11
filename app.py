import streamlit as st
from brain_core import MasterAI
from brain_models import ALL_AGENTS, hold_desire_council, hire_new_agent
from meta_agent import MetaArchitect

# Настройка страницы
st.set_page_config(page_title="Сибирский Элемент v3.5", page_icon="🏢", layout="wide")

# Инициализация ИИ и памяти
if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_proposal" not in st.session_state:
    st.session_state.current_proposal = None

# --- БОКОВАЯ ПАНЕЛЬ (Таблица лидеров) ---
with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    # ДИНАМИЧЕСКИЙ ВЫВОД: Таблица берет всех, кто есть в ALL_AGENTS
    for agent in ALL_AGENTS:
        st.write(f"**{agent.name}**")
        st.progress(min(1.0, agent.accuracy / 100.0))
        st.caption(f"Точность: {agent.accuracy:.1f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    
    # --- v3.3 Совет Желаний ---
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"):
        council_decision = hold_desire_council()
        st.info(council_decision)

    st.divider()
    
    # --- v3.5 Мета-Архитектор + Найм ---
    st.subheader("🧬 Центр Эволюции")
    if st.button("🔍 Сканировать систему на застой"):
        architect = MetaArchitect()
        proposal = architect.analyze_system()
        
        if isinstance(proposal, dict):
            st.session_state.current_proposal = proposal # ЗАПОМИНАЕМ ПРЕДЛОЖЕНИЕ
        else:
            st.session_state.current_proposal = None
            st.success(proposal)

    # ВЫВОДИМ ПРЕДЛОЖЕНИЕ (если оно есть в памяти)
    if st.session_state.current_proposal:
        prop = st.session_state.current_proposal
        st.warning(f"⚠️ **Запрос на патч от {prop['target_agent']}!**")
        st.write(f"Текущая точность: {prop['current_accuracy']:.1f}%")
        st.info(f"💡 **Предложение ИИ:** {prop['message']}")
        
        # КНОПКА НАЙМА АГЕНТА (Теперь она работает отдельно)
        if st.button("✅ Нанять агента"):
            success, msg = hire_new_agent(prop['new_agent_name'], prop['category'])
            if success:
                st.success(msg)
                st.session_state.current_proposal = None # Очищаем память после найма
                st.rerun() # Перезагружаем, чтобы новый агент появился в таблице
            else:
                st.error(msg)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏢 Сибирский Элемент v3.5")
st.markdown("Генератор Отделов: ИИ сам предлагает нанять новых агентов.")

# Отображение истории
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# Поле ввода
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
st.caption("Текущая сборка: v3.5 (MetaArchitect + Hire) | Автор: Сибирский Элемент")
