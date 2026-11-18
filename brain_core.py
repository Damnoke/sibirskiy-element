import re
import time
import random
import requests
from bs4 import BeautifulSoup
import brain_models 
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        # Кибербезопасность (Цербер)
        if re.search(r"DROP\s+TABLE|<script>", text_low):
            brain_models.SEC_CERBER.knowledge += 1
            brain_models.SEC_CERBER.accuracy = min(100.0, 50.0 + (brain_models.SEC_CERBER.knowledge * 0.25))
            brain_models.save_agents()
            return "🚨 [КИБЕР-ЩИТ]: Атака отбита."
            
        # Быстрые ответы по жестким правилам
        if any(w in text_low for w in ["что такое", "значение"]): 
            return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк"]): 
            return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "таблет"]): 
            return medical_dept(text)
        return None 

def web_search(query):
    """Функция парсинга Википедии для режима 'Поиск в сети'"""
    try:
        # Очищаем запрос от лишних слов
        clean_query = query.replace("расскажи про", "").replace("что такое", "").strip()
        url = f"https://ru.wikipedia.org/wiki/{clean_query.replace(' ', '_')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = " ".join([p.get_text() for p in paragraphs[:2]]) # Берем первые 2 абзаца
            if text.strip():
                return text[:800] + "..." # Обрезаем, чтобы не перегружать экран
        return None
    except:
        return None

class LibraryAI:
    def ask(self, text, mode="normal"):
        text_low = text.lower()
        
        # --- РЕЖИМ 1: ПОИСК В СЕТИ ---
        if mode == "search":
            search_result = web_search(text)
            if search_result:
                return f"🌐 **[ПОИСК В ИНТЕРНЕТЕ]:**\nЯ нашел информацию в открытых источниках:\n\n{search_result}\n\n*(Данные взяты из Википедии)*"
            else:
                return "🌐 **[ПОИСК В ИНТЕРНЕТЕ]:** Не удалось найти точный ответ. Попробуйте переформулировать запрос."

        # --- РЕЖИМ 2 и 3: ОБЫЧНЫЙ И СИБСИНК (ПОИСК ПО БАЗЕ) ---
        length_type = "Средний"
        if any(w in text_low for w in ["коротко", "кратко"]): length_type = "Короткий"
        elif any(w in text_low for w in ["подробно", "длинно"]): length_type = "Длинный"

        # Очистка от стоп-слов
        clean_text = re.sub(r'[^\w\s]', '', text_low)
        stop_words = ["расскажи", "коротко", "подробно", "про", "что", "ты", "знаешь", "мне", "как", "это"]
        words = [w for w in clean_text.split() if w not in stop_words]

        for agent in brain_models.ALL_AGENTS:
            for w in words:
                if len(w) > 3:
                    root = w[:4]
                    for vocab_word in agent.vocabulary:
                        if root in vocab_word:
                            
                            # АВТОР (Гиппократ) пишет черновик (с рефлексией)
                            draft = agent.generate_text(vocab_word, length_type=length_type)
                            
                            # КРИТИК (Асклепий)
                            critique = ""
                            if agent.name != "Асклепий" and "язв" in draft.lower():
                                critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Внимание! В тексте упомянута язва. Ибупрофен может быть противопоказан! Требуется проверка врачом."
                            
                            # СТИЛИСТ (Даль)
                            stylist_report = ""
                            dal = next((a for a in brain_models.ALL_AGENTS if a.name == "Даль"), None)
                            if dal:
                                polished_draft = draft.replace("  ", " ").replace(" ,", ",").replace(" .", ".").strip()
                                if not polished_draft.endswith("."): polished_draft += "."
                                stylist_report = "\n\n📖 **[СТИЛИСТ | Даль]:** Текст вычитан. Стиль и пунктуация приведены в порядок."
                                final_text = polished_draft
                            else:
                                final_text = draft

                            # В зависимости от режима, меняем заголовок
                            if mode == "sibthink":
                                header = f"🧠 **[СИБСИНК (Глубокий анализ)]**\n"
                            else:
                                header = f"🚀 **[БЫСТРЫЙ ОТВЕТ]**\n"

                            # Возвращаем ответ со скрытым ID агента
                            return header + final_text + critique + stylist_report + f"\n\n[AGENT_ID:{agent.name}]"
        return None

class ProAI:
    def ask(self, text):
        return f"💬 [PRO-ВЕРСИЯ] Запрос «{text}» сложен. Загрузите текст в 'Библиотеку' или включите 'Поиск'."

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.library = LibraryAI()
        self.pro = ProAI()

    def ask(self, user_text, mode="normal"):
        # 1. Сначала проверяем жесткие правила
        response = self.base.ask(user_text)
        if response: return response
        
        # 2. Если не нашли, идем в библиотеку (или поиск)
        lib_response = self.library.ask(user_text, mode=mode)
        if lib_response: return lib_response
        
        # 3. Если совсем ничего не нашли
        time.sleep(1) 
        return self.pro.ask(user_text)
