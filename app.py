import streamlit as st
import brain_models
import os
import json
import importlib
from brain_core import MasterAI
from meta_agent import MetaArchitect

st.set_page_config(page_title="Сибирский Элемент v3.8", page_icon="🏢", layout="wide")

if "ai_brain" not in st.session_state: st.session_state.ai_brain = MasterAI()
if "messages" not in st.session_state: st.session_state.messages = []
if "current_proposal" not in st.session_state: st.session_state.current_proposal = None
if "learn_msg" not in st.session_state: st.session_state.learn_msg = None

with st.sidebar:
    st.header("🏆 Таблица лидеров")
    
    # ПРИНУДИТЕЛЬНАЯ ПЕРЕЗАГРУЗКА МОДУЛЯ (чтобы сброс работал)
    importlib.reload(brain_models) 
    
    for agent in brain_models.ALL_AGENTS:
        st.write(f"**{agent.name}**")
        st.progress(min(1.0, agent.accuracy / 100.0))
        st.caption(f"Точность: {agent.accuracy:.1f}% | Знаний: {agent.knowledge}")
    
    st.divider()
    st.subheader("📚 Библиотека (Обучение)")
    
    if st.session_state.learn_msg:
        st.success(st.session_state.learn_msg)
        st.session_state.learn_msg = None

    agent_names = [a.name for a in brain_models.ALL_AGENTS]
    selected_agent = st.selectbox("Выберите агента:", agent_names)
    text_input = st.text_area("Вставьте текст (статью, книгу):", height=100)
    
    if st.button("📖 Прочитать и выучить"):
        if text_input.strip():
            agent = next(a for a in brain_models.ALL_AGENTS if a.name == selected_agent)
            result = agent.read_book(text_input)
            st.session_state.learn_msg = result 
            st.rerun() 
        else: st.warning("Вставьте текст!")
            
    st.divider()
    st.subheader("🗣️ Голос Агентов")
    if st.button("Созвать Совет"): st.info(brain_models.hold_desire_council())
    
    st.divider()
    st.subheader("🧬 Центр Эволюции")
    if st.button("🔍 Сканировать систему на застой"):
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
            else: st.error(msg)

    # ЖЕСТКИЙ СБРОС ПАМЯТИ
    st.divider()
    if st.button("🧹 Сбросить память ИИ (Hard Reset)"):
        with open("agents_db.json", "w", encoding="utf-8") as f:
            json.dump([], f) # Записываем пустой список
        st.session_state.learn_msg = "Память полностью очищена!"
        st.rerun()

st.title("🏢 Сибирский Элемент v3.8")
st.markdown("Умная память: кормите ИИ полными статьями, а не только началом!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

if prompt := st.chat_input("Напишите ваш вопрос..."):
    with st.chat_message("user"): 
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Генерирую..."):
            response = st.session_state.ai_brain.ask(prompt)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "🤖"})
    st.rerun()

st.divider()
st.caption("Текущая сборка: v3.8 (Умная память + Hard Reset) | Автор: Сибирский Элемент")
