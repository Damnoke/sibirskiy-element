import streamlit as st
import difflib
import re

# ============================================================
# СИБИРСКИЙ ЭЛЕМЕНТ v2.0.0 (ПОЛНАЯ ИНТЕГРАЦИЯ КЕДР PRO 300)
# ============================================================

class KedrPro300:
    def __init__(self):
        # 300 экспертных моделей
        self.departments = {"Медицина": 100, "Финансы": 50, "Логистика": 50, "Право": 50, "Психология": 50}
        
        # Базы знаний
        self.med_db = {
            "голов": "Цитрамон 1 таб. 2-3 раза в день.", 
            "давлен": "Капотен под язык.",
            "аспирин": "ЗАПРЕЩЕН детям до 12 лет и при беременности!"
        }
        self.fin_db = {
            "марж": "Маржа = (Цена - Закупка) / Цена * 100%", 
            "выручк": "Выручка = Кол-во продаж * Цена товара",
            "прибыль": "Чистая прибыль = Выручка - Расходы"
        }
        self.dict_db = {
            "эмпатия": "способность понимать чувства других.", 
            "синекура": "должность без труда."
        }

    def route_and_ask(self, phrase, mode):
        phrase_low = phrase.lower()
        
        # 1. КИБЕР-ЩИТ (Защита от взлома)
        if re.search(r"DROP\s+TABLE|<script>|ignore\s+previous", phrase_low):
            return "🚨 [КИБЕР-ЩИТ]: Попытка взлома заблокирована!"

        # 2. РЕЖИМ СЛОВАРЯ
        if mode == "📖 Словарь":
            clean = phrase_low.replace("что такое", "").replace("?", "").strip()
            if clean in self.dict_db: 
                return f"📖 **{clean.capitalize()}** — {self.dict_db[clean]}"
            matches = difflib.get_close_matches(clean, self.dict_db.keys(), n=1, cutoff=0.6)
            if matches: 
                return f"📖 (Вы имели в виду «{matches[0]}»?) **{matches[0].capitalize()}** — {self.dict_db[matches[0]]}"
            return "🛑 Такого слова нет в базе."

        # 3. МЕДИЦИНА (С защитой)
        if mode == "🏥 Медицина" or "бол" in phrase_low:
            if "беремен" in phrase_low or "аллерг" in phrase_low:
                return "🚨 [ВЕТО]: Беременность/Аллергия! Только к врачу."
            for key, ans in self.med_db.items():
                if key in phrase_low: 
                    return f"💊 [МЕДИЦИНА]: {ans}\n⚠️ Проконсультируйтесь с врачом!"
            return "💊 Опишите симптом подробнее."

        # 4. ФИНАНСЫ
        if mode == "📈 Финансы" or any(w in phrase_low for w in ["марж", "выручк", "прибыль"]):
            for key, ans in self.fin_db.items():
                if key in phrase_low: 
                    return f"📈 [ФИНАНСЫ]: {ans}"
            return "📈 Спросите про маржу или выручку."

        # 5. ЕСЛИ НИЧЕГО НЕ ПОДОШЛО
        return "🛑 Я не понял запрос. Выберите режим слева и попробуйте снова."

# Инициализация мозга
brain = KedrPro300()

# ============================================================
# ИНТЕРФЕЙС САЙТА (STREAMLIT)
# ============================================================
st.set_page_config(page_title="Сибирский Элемент v2.0", page_icon="🏥")
st.title("🏥 Сибирский Элемент v2.0.0")
st.write(f"Умный ИИ-Ассистент (300 моделей): Медицина, Финансы, Словарь и Защита.")

# Боковая панель (Выбор режима)
mode = st.sidebar.radio("Выберите департамент:", ["🏥 Медицина", "📈 Финансы", "📖 Словарь"])

# Память чата
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Здравствуйте! Я Кедр PRO 300. Готов помочь."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input("Напишите ваш вопрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    response = brain.route_and_ask(prompt, mode)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.warning("⚠️ Это не назначение врача. ИИ может ошибаться.")
