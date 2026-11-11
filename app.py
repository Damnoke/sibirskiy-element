import streamlit as st
from brain_core import MasterAI
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER

# Настройка страницы
st.set_page_config(page_title="Сибирский Элемент v3.3", page_icon="🏢", layout="wide")

# Инициализация ИИ в сессии (чтобы память не сбрасывалась)
if "ai_brain" not in st.session_state:
    st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- БОКОВАЯ ПАНЕЛЬ (Таблица лидеров) ---
with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    # Асклепий
    st.write("**Асклепий (Медицина)**")
    st.progress(MED_ASKL.accuracy / 100.0)
    st.caption(f"Точность: {MED_ASKL.accuracy:.0f}% | Знаний: {MED_ASKL.knowledge}")
    
    # Гиппократ
    st.write("**Гиппократ (Медицина)**")
    st.progress(MED_HIPPO.accuracy / 100.0)
    st.caption(f"Точность: {MED_HIPPO.accuracy:.0f}% | Знаний: {MED_HIPPO.knowledge}")
    
    # Морган
    st.write("**Морган (Финансы)**")
    st.progress(FIN_MORGAN.accuracy / 100.0)
    st.caption(f"Точность: {FIN_MORGAN.accuracy:.0f}% | Знаний: {FIN_MORGAN.knowledge}")
    
    # Даль
    st.write("**Даль (Словарь)**")
    st.progress(DICT_DAL.accuracy / 100.0)
    st.caption(f"Точность: {DICT_DAL.accuracy:.0f}% | Знаний: {DICT_DAL.knowledge}")
    
    # Цербер
    st.write("**Цербер (Безопасность)**")
    st.progress(SEC_CERBER.accuracy / 100.0)
    st.caption(f"Точность: {SEC_CERBER.accuracy:.0f}% | Знаний: {SEC_CERBER.knowledge}")
    st.divider()
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"):
        from brain_models import hold_desire_council
        council_decision = hold_desire_council()
        st.info(council_decision)
# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏢 Сибирский Элемент v3.3")
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
st.caption("Текущая сборка: v3.1 (MasterAI + Умный Fallback) | Автор: Сибирский Элемент")
