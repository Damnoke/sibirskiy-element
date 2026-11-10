import streamlit as st
from brain_core import MasterAI
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER

st.set_page_config(page_title="Сибирский Элемент v3.0", page_icon="🏥")
st.title("🏥 Сибирский Элемент v3.0")
st.write("Умный Fallback: Сначала База, если не поняла — подключается PRO.")

brain = MasterAI() 

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Здравствуйте! Я — Кедр v3.0. Напишите вопрос."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напишите ваш вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    response = brain.ask(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.header("🏆 Таблица лидеров")
all_models = [MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER]
all_models.sort(key=lambda x: x.accuracy, reverse=True)

for m in all_models:
    st.sidebar.markdown(f"**{m.name}** ({m.specialty})")
    st.sidebar.progress(m.accuracy)
    st.sidebar.caption(f"Точность: {m.accuracy:.0%} | Знаний: {m.knowledge}")

st.sidebar.warning("⚠️ Это не назначение врача.")

st.markdown(
    "<div style='text-align: center; color: gray; font-size: 14px; margin-top: 50px;'>"
    "Текущая сборка: v3.0 (MasterAI + Умный Fallback) | Автор: Сибирский Элемент"
    "</div>", 
    unsafe_allow_html=True
)
