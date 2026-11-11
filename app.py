import streamlit as st
from brain_core import MasterAI
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER, hold_desire_council
from meta_agent import MetaArchitect

# Настройка страницы
st.set_page_config(page_title="Сибирский Элемент v3.4", page_icon="🏢", layout="wide")

# Инициализация ИИ в сессии (чтобы память не сбрасывалась)
if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ (Таблица лидеров) ---
with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    # Список агентов для вывода
    agents = [
        (MED_ASKL, "Медицина"),
        (MED_HIPPO, "Медицина"),
        (FIN_MORGAN, "Финансы"),
        (DICT_DAL, "Словарь"),
        (SEC_CERBER, "Безопасность")
    ]
    
    for agent, category in agents:
        st.write(f"**{agent.name} ({category})**")
        # Ограничиваем прогресс-бар, чтобы он не улетел за 100%
        st.progress(min(1.0, agent.accuracy / 100.0))
        st.caption(f"Точность: {agent.accuracy:.0f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    
    # --- v3.3 Совет Желаний ---
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"):
        council_decision = hold_desire_council()
        st.info(council_decision)

    st.divider()
    
    # --- v3.4 Мета-Архитектор ---
    st.subheader("🧬 Центр Эволюции")
    if st.button("🔍 Сканировать систему на застой"):
        architect = MetaArchitect()
        proposal = architect.analyze_system()
        
        if isinstance(proposal, dict):
            st.warning(f"⚠️ **Запрос на патч от {proposal['target_agent']}!**")
            st.write(f"Текущая точность: {proposal['current_accuracy']:.1f}%")
            st.info(f"💡 **Предложение ИИ:** {proposal['patch_suggestion']}")
        else:
            st.success(proposal)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏢 Сибирский Элемент v3.4")
st.markdown("Умный Fallback: Сначала База, если не поняла — подключается PRO.")

# Отображение истории сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# Поле ввода
if prompt := st.chat_input("Напишите ваш вопрос..."):
    # 1. Показываем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Получаем ответ от ИИ
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Анализирую..."):
            response = st.session_state.ai_brain.ask(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    
    # МАГИЯ: Перезапускаем страницу, чтобы боковая панель подтянула новые проценты
    st.rerun()

# Подвал
st.divider()
st.caption("Текущая сборка: v3.4 (MetaArchitect + Desire Council) | Автор: Сибирский Элемент")
