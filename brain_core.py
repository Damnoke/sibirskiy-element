import re
import time
import random
import requests
from bs4 import BeautifulSoup
import brain_models 
from brain_departments import medical_dept, finance_dept, dict_dept
import urllib.parse

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        if re.search(r"DROP\s+TABLE|<script>", text_low):
            brain_models.SEC_CERBER.knowledge += 1
            brain_models.SEC_CERBER.accuracy = min(100.0, 50.0 + (brain_models.SEC_CERBER.knowledge * 0.25))
            brain_models.save_agents()
            return "🚨 [КИБЕР-ЩИТ]: Атака отбита."
            
        if any(w in text_low for w in ["что такое", "значение"]): 
            return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк"]): 
            return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "таблет"]): 
            return medical_dept(text)
        return None 

def web_search(query):
    try:
        clean_query = query.replace("расскажи про", "").replace("что такое", "").strip()
        # КОДИРУЕМ ЗАПРОС (чтобы русские буквы правильно передавались в API)
        encoded_query = urllib.parse.quote(clean_query)
        
        search_url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&utf8=&format=json"
        headers = {'User-Agent': 'SibirskiyElement/3.9 (test@example.com)'}
        res = requests.get(search_url, headers=headers, timeout=5).json()
        
        if not res['query']['search']:
            return None
            
        page_title = res['query']['search'][0]['title']
        encoded_title = urllib.parse.quote(page_title)
        
        page_url = f"https://ru.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={encoded_title}&format=json"
        page_res = requests.get(page_url, headers=headers, timeout=5).json()
        pages = page_res['query']['pages']
        extract = list(pages.values())[0].get('extract', '')
        
        if not extract:
            return f"Нашел статью «{page_title}», но не смог извлечь текст."
            
        return extract[:800] + "..."
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return None

class LibraryAI:
    def ask(self, text, mode="normal"):
        text_low = text.lower()
        
        if mode == "search":
            search_result = web_search(text)
            if search_result:
                # ДОБАВЛЯЕМ [AGENT_ID:Цербер], чтобы появились кнопки
                return f"🌐 **[SEARCH]:**\nЯ нашел информацию в Википедии:\n\n{search_result}\n\n[AGENT_ID:Цербер]"
            else:
                return "🌐 **[SEARCH]:** Не удалось найти точный ответ. Попробуйте написать короче (например, просто 'Наполеон').\n\n[AGENT_ID:Цербер]"

        length_type = "Средний"
        if any(w in text_low for w in ["коротко", "кратко"]): length_type = "Короткий"
        elif any(w in text_low for w in ["подробно", "длинно"]): length_type = "Длинный"

        clean_text = re.sub(r'[^\w\s]', '', text_low)
        stop_words = ["расскажи", "коротко", "подробно", "про", "что", "ты", "знаешь", "мне", "как", "это"]
        words = [w for w in clean_text.split() if w not in stop_words]

        for agent in brain_models.ALL_AGENTS:
            for w in words:
                if len(w) > 3:
                    root = w[:4]
                    for vocab_word in agent.vocabulary:
                        if root in vocab_word:
                            
                            draft = agent.generate_text(vocab_word, length_type=length_type)
                            
                            critique = ""
                            if agent.name != "Асклепий" and "язв" in draft.lower():
                                critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Внимание! В тексте упомянута язва. Требуется проверка врачом."
                            
                            stylist_report = ""
                            dal = next((a for a in brain_models.ALL_AGENTS if a.name == "Даль"), None)
                            if dal:
                                polished_draft = draft.replace("  ", " ").replace(" ,", ",").replace(" .", ".").strip()
                                if not polished_draft.endswith("."): polished_draft += "."
                                stylist_report = "\n\n📖 **[СТИЛИСТ | Даль]:** Текст вычитан."
                                final_text = polished_draft
                            else:
                                final_text = draft

                            header = "🧠 **[SIBTHINK]:**\n" if mode == "sibthink" else "🚀 **[CHAT]:**\n"

                            return header + final_text + critique + stylist_report + f"\n\n[AGENT_ID:{agent.name}]"
        return None

class ProAI:
    def ask(self, text):
        return f"💬 [PRO-ВЕРСИЯ] Запрос «{text}» сложен. Загрузите текст в 'Библиотеку' или включите 'Search'.\n\n[AGENT_ID:Цербер]"

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.library = LibraryAI()
        self.pro = ProAI()

    def ask(self, user_text, mode="normal", **kwargs):
        response = self.base.ask(user_text)
        if response: return response
        
        lib_response = self.library.ask(user_text, mode=mode)
        if lib_response: return lib_response
        
        time.sleep(1) 
        return self.pro.ask(user_text)
