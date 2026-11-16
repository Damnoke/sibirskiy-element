import streamlit as st
import brain_models
from brain_core import MasterAI
from meta_agent import MetaArchitect

# Настройка страницы
st.set_page_config(page_title="Сибирский Элемент v3.7", page_icon="🏢", layout="wide")

# Инициализация сессий
if "ai_brain" not in st.session_state: st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state: st.session_state.messages = []
if "current_proposal" not in st.session_state: st.session_state.current_proposal = None

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    for agent in brain_models.ALL_AGENTS:
        st.write(f"**{agent.name}**")
        st.progress(min(1.0, agent.accuracy / 100.0))
        st.caption(f"Точность: {agent.accuracy:.1f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    
    # БЛОК ОБУЧЕНИЯ
    st.subheader("📚 Библиотека (Обучение)")
    agent_names = [a.name for a in brain_models.ALL_AGENTS]
    selected_agent = st.selectbox("Выберите агента:", agent_names)
    
    text_input = st.text_area("Вставьте текст (статью, книгу):", height=100)
    
    if st.button("📖 Прочитать и выучить"):
        if text_input.strip():
            agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
            result = agent.read_book(text_input)
            st.success(result)
        else:
            st.warning("Вставьте текст!")
            
    st.divider()
    
    # БЛОК ГЕНЕРАЦИИ (v3.7)
    st.subheader("🗣️ Генератор текста")
    start_word = st.text_input("С какого слова начать? (например, 'парацетамол'):")
    length_choice = st.selectbox("Размер текста:", ["Короткий", "Средний", "Длинный"])
    
    if st.button("📝 Сгенерировать"):
        if start_word.strip():
            agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
            result = agent.generate_text(start_word.lower(), length_choice)
            st.info(result)
        else:
            st.warning("Введите стартовое слово!")
    
    st.divider()

    # БЛОК ГОЛОСА АГЕНТОВ (Тот, который я пропустил!)
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"):
        council_decision = brain_models.hold_desire_council()
        st.info(council_decision)
    
    st.divider()
    
    # ЦЕНТР ЭВОЛЮЦИИ
    st.subheader("🧬 Центр Эволюции")
    if st.button("🔍 Сканировать систему на застой"):
        proposal = MetaArchitect().analyze_system()
        if isinstance(proposal, dict): 
            st.session_state.current_proposal = proposal 
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
            else: 
                st.error(msg)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏢 Сибирский Элемент v3.7")
st.markdown("Фарма-Генератор: Обучите агента тексту, а затем сгенерируйте свою статью!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напишите ваш вопрос..."):
    with st.chat_message("user"): 
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Думаю..."):
            response = st.session_state.ai_brain.ask(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    
    st.rerun()

st.divider()
st.caption("Текущая сборка: v3.7 (Фарма-Генератор) | Автор: Сибирский Элемент")
