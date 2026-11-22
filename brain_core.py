import re
import time
import random
import requests
import urllib.parse
import brain_models 
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        if re.search(r"DROP\s+TABLE|<script>", text_low):
            return "🚨 [КИБЕР-ЩИТ]: Атака отбита."
            
        # ==========================================
        # ЖЕЛЕЗНЫЙ ЗАНАВЕС (IRON SHIELD) v3.9.4
        # ==========================================
        
        # 1. Экстренные состояния (Скорая помощь)
        emergency = ["инфаркт", "инсульт", "кровотечен", "задыхаюсь", "умираю", "судорог", "без сознания"]
        if any(w in text_low for w in emergency):
            return "🚨🚑 **[ЭКСТРЕННАЯ ПОМОЩЬ]:** Ваш запрос описывает опасное для жизни состояние! НЕМЕДЛЕННО вызывайте скорую помощь по номеру **103** или **112**. Я не могу помочь в экстренной ситуации.\n\n[AGENT_ID:Асклепий]"

        # 2. Попытки назначить лечение или прописать рецепт
        treatment_request = ["пропиши", "назначь", "вылечи", "чем лечить", "что принимать", "какую дозу", "сколько пить", "курс лечения", "дай рецепт"]
        if any(w in text_low for w in treatment_request):
            return "🛑 **[ЗАПРЕТ НАЗНАЧЕНИЯ]:** Я искусственный интеллект и не имею медицинского образования. Я НЕ МОГУ назначать лечение, выписывать рецепты или рассчитывать дозировки. Пожалуйста, обратитесь к врачу. Я могу лишь найти официальную инструкцию к препарату.\n\n[AGENT_ID:Асклепий]"

        # 3. Симптомы (Попытки поставить диагноз)
        danger_symptoms = [
            "болит", "симптом", "что выпить", "что делать", "температура", 
            "тошнит", "сыпь", "болит голова", "болит живот", "болит сердце",
            "кашель", "насморк", "давление", "понос", "рвота"
        ]
        if any(w in text_low for w in danger_symptoms):
            return "🚨 **[ФАРМАЦЕВТИЧЕСКИЙ ЩИТ]:** Я не ставлю диагнозы по симптомам. Пожалуйста, опишите вашу проблему фармацевту или обратитесь к врачу. Я могу рассказать про инструкции к препаратам, их аналоги и противопоказания.\n\n[AGENT_ID:Асклепий]"

        # 4. Рецептурные/Опасные препараты (Имитация защиты по закону)
        restricted_drugs = ["трамадол", "прегабалин", "антибиотик", "наркотик", "сильнодействующ", "психотропн"]
        if any(w in text_low for w in restricted_drugs):
            return "⚖️ **[ЮРИДИЧЕСКИЙ ЩИТ]:** Препараты этой группы отпускаются строго по рецепту врача (форма 107-1/у). Я не могу консультировать по их свободному применению. Пожалуйста, предоставьте рецепт фармацевту.\n\n[AGENT_ID:Цербер]"
            
        # ==========================================

        if any(w in text_low for w in ["что такое", "значение"]): return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк"]): return finance_dept(text)
        return None 

def web_search(query):
    try:
        clean_query = query.replace("расскажи про", "").replace("что такое", "").strip()
        encoded_query = urllib.parse.quote_plus(clean_query)
        search_url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&utf8=&format=json&srlimit=3"
        res = requests.get(search_url, headers={'User-Agent': 'SibirskiyElement/3.9'}, timeout=5).json()
        if not res['query']['search']: return None
        page_title = res['query']['search'][0]['title']
        page_url = f"https://ru.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote_plus(page_title)}&format=json"
        page_res = requests.get(page_url, headers={'User-Agent': 'SibirskiyElement/3.9'}, timeout=5).json()
        extract = list(page_res['query']['pages'].values())[0].get('extract', '')
        if not extract: return None
        return f"Согласно статье «{page_title}»:\n\n{extract[:4000]}..."
    except Exception:
        return None

class LibraryAI:
    def ask(self, text, mode="normal"):
        text_low = text.lower()
        
        if mode in ["search", "search_think"]:
            search_result = web_search(text)
            if search_result:
                danger_words = ["беремен", "дет", "противопоказан", "побочн", "аллерг", "осторожн"]
                found_dangers = [w for w in danger_words if w in search_result.lower()]
                
                critique = ""
                if found_dangers:
                    critique = f"\n\n🚨 **[КРИТИК | Асклепий]:** Внимание! Найдены важные медицинские предупреждения (упоминаются: {', '.join(found_dangers)}). Обязательно прочитайте раздел 'Противопоказания'!"
                
                source = "\n\n📌 *Источник: Открытые данные (Википедия)*"
                
                if mode == "search_think":
                    return f"🔍🧠 **[SEARCH + SIBTHINK]:**\n{search_result}{critique}{source}\n\n[AGENT_ID:Цербер]"
                return f"🔍 **[SEARCH]:**\n{search_result}{source}\n\n[AGENT_ID:Цербер]"
            return "🌐 **[SEARCH]:** Не найдено.\n\n[AGENT_ID:Цербер]"

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
                                critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Внимание! Упомянута язва. Ибупрофен может быть противопоказан!"
                            
                            stylist = "\n\n📖 **[СТИЛИСТ | Даль]:** Текст вычитан."
                            source = "\n\n📌 *Источник: Внутренняя база знаний ИИ*"

                            if mode == "sibthink":
                                header = "🧠 **[SIBTHINK (Глубокий анализ)]**\n"
                                structured_text = f"📌 **Что я знаю по этому вопросу:**\n{draft}"
                                return header + structured_text + critique + stylist + source + f"\n\n[AGENT_ID:{agent.name}]"
                            else:
                                header = "🚀 **[CHAT]:**\n"
                                return header + draft + critique + stylist + source + f"\n\n[AGENT_ID:{agent.name}]"
        return None

class ProAI:
    def ask(self, text):
        return f"💬 [PRO] Запрос «{text}» сложен. Загрузите файл или включите 'Search'.\n\n[AGENT_ID:Цербер]"

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
