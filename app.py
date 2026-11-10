import streamlit as st
import difflib
import re

# ============================================================
# МОЗГ ИИ (Медицина, Финансы, Словарь, Безопасность)
# ============================================================
class SuperKedr:
    def __init__(self):
        self.med_db = {"голов": "Цитрамон 1 таб. 2-3 раза в день.", "давлен": "Капотен под язык."}
        self.fin_db = {"марж": "Маржа = (Цена - Закупка) / Цена * 100%", "выручк": "Выручка = Кол-во * Цена"}
        self.dict_db = {"эмпатия": "способность понимать чувства других.", "синекура": "должность без труда."}
        
    def ask(self, phrase, mode):
        phrase_low = phrase.lower()
        
        # 1. ЗАЩИТА
        if re.search(r"DROP\s+TABLE|<script>|ignore\s+previous", phrase_low):
            return "[КИБЕР-ЩИТ]: Попытка взлома заблокирована!"
            
        # 2. СЛОВАРЬ
        if mode == "Словарь":
            clean = phrase_low.replace("что такое", "").replace("?", "").strip()
            if clean in self.dict_db: return f"**{clean.capitalize()}** — {self.dict_db[clean]}"
            matches = difflib.get_close_matches(clean, self.dict_db.keys(), n=1, cutoff=0.6)
            if matches: return f"(Вы имели в виду «{matches[0]}»?) **{matches[0].capitalize()}** — {self.dict_db[matches[0]]}"
            return "Такого слова нет в базе."

        # 3. МЕДИЦИНА
        if mode == "Медицина" or "бол" in phrase_low:
            if "беремен" in phrase_low or "аллерг" in phrase_low:
                return "[ВЕТО]: Беременность/Аллергия! Только к врачу."
            for key, ans in self.med_db.items():
                if key in phrase_low: return f"[МЕДИЦИНА]: {ans}\nПроконсультируйтесь с врачом!"
            return "Опишите симптом подробнее."

        # 4. ФИНАНСЫ
        if mode == "Финансы":
            for key, ans in self.fin_db.items():
                if key in phrase_low: return f"[ФИНАНСЫ]: {ans}"
            return "Спросите про маржу или выручку."

        return "Я не понял. Выберите режим слева."

brain = SuperKedr()

# ============================================================
# САЙТ
# ============================================================
st.set_page_config(page_title="Сибирский Элемент v2.0", page_icon="🏥")
st.title("Сибирский Элемент v2.0.0")
st.write("Умный ИИ-Ассистент: Медицина, Финансы и Словарь.")

mode = st.sidebar.radio("Выберите режим:", ["Медицина", "Финансы", "Словарь"])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Здравствуйте! Я готов помочь. Выберите режим и задайте вопрос."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напишите вопрос здесь..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    response = brain.ask(prompt, mode)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.warning("Это не назначение врача. ИИ может ошибаться.")
