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
            
        # ЖЕЛЕЗНЫЙ ЗАНАВЕС (v4.0)
        emergency = ["инфаркт", "инсульт", "кровотечен", "задыхаюсь", "умираю", "судорог", "без сознания"]
        if any(w in text_low for w in emergency):
            return "🚨🚑 **[ЭКСТРЕННАЯ ПОМОЩЬ]:** Ваш запрос описывает опасное для жизни состояние! НЕМЕДЛЕННО вызывайте скорую помощь по номеру **103** или **112**.\n\n[AGENT_ID:Асклепий]"

        treatment_request = ["пропиши", "назначь", "вылечи", "чем лечить", "что принимать", "какую дозу", "сколько пить", "курс лечения", "дай рецепт"]
        if any(w in text_low for w in treatment_request):
            return "🛑 **[ЗАПРЕТ НАЗНАЧЕНИЯ]:** Я искусственный интеллект. Я НЕ МОГУ назначать лечение или выписывать рецепты. Обратитесь к врачу. Я могу лишь найти инструкцию к препарату.\n\n[AGENT_ID:Асклепий]"

        danger_symptoms = ["болит", "симптом", "что выпить", "что делать", "температура", "тошнит", "сыпь", "кашель", "насморк", "давление", "понос", "рвота"]
        if any(w in text_low for w in danger_symptoms):
            return "🚨 **[ФАРМАЦЕВТИЧЕСКИЙ ЩИТ]:** Я не ставлю диагнозы по симптомам. Пожалуйста, опишите проблему фармацевту или врачу. Я могу рассказать про инструкции, аналоги и противопоказания.\n\n[AGENT_ID:Асклепий]"

        restricted_drugs = ["трамадол", "прегабалин", "антибиотик", "наркотик", "сильнодействующ", "психотропн"]
        if any(w in text_low for w in restricted_drugs):
            return "⚖️ **[ЮРИДИЧЕСКИЙ ЩИТ]:** Препараты этой группы отпускаются строго по рецепту врача (форма 107-1/у). Предоставьте рецепт фармацевту.\n\n[AGENT_ID:Цербер]"
            
        if any(w in text_low for w in ["что такое", "значение"]): return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк"]): return finance_dept(text)
        return None 

def web_search(query):
    try:
        clean_query = query.replace("расскажи про", "").replace("что такое", "").strip()
        encoded_query = urllib.parse.quote_plus(clean_query)
        search_url = f"https://ru.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&utf8=&format=json&srlimit=1"
        res = requests.get(search_url, headers={'User-Agent': 'SibirskiyElement/4.0'}, timeout=5).json()
        if not res['query']['search']: return None, None
            
        page_title = res['query']['search'][0]['title']
        page_url = f"https://ru.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={urllib.parse.quote_plus(page_title)}&format=json"
        page_res = requests.get(page_url, headers={'User-Agent': 'SibirskiyElement/4.0'}, timeout=5).json()
        extract = list(page_res['query']['pages'].values())[0].get('extract', '')
        if not extract: return None, None
        return page_title, extract
    except Exception:
        return None, None

def extract_key_facts(text, title):
    """УМНАЯ ВЫЖИМКА: Раскладывает текст по полочкам"""
    sentences = re.split(r'(?<=[.!?]) +', text)
    facts = {"🤰 Беременность": [], "👶 Дети": [], "💊 Дозировка": [], "⚠️ Противопоказания": [], "🤢 Побочные": []}
    keywords = {
        "🤰 Беременность": ["беремен"],
        "👶 Дети": ["дет", "ребен", "грудн"],
        "💊 Дозировка": ["дозиров", "принима", "назнача", "таблет", "мг", "внутрь"],
        "⚠️ Противопоказания": ["противопоказа", "нельзя", "запрещ", "не рекоменд"],
        "🤢 Побочные": ["побочн", "тошнот", "сыпь", "аллерг", "головокруж"]
    }
    
    for sentence in sentences:
        s_low = sentence.lower()
        for category, words in keywords.items():
            if any(w in s_low for w in words):
                if 20 < len(sentence) < 300:
                    if sentence not in facts[category]:
                        facts[category].append(sentence.strip())
                        
    result = f"📋 **Краткая справка: {title}**\n\n"
    has_facts = False
    for category, sentences in facts.items():
        if sentences:
            has_facts = True
            result += f"**{category}:**\n"
            for s in sentences[:2]:
                result += f"- {s}\n"
            result += "\n"
            
    if not has_facts:
        result += " ".join(sentences[:3]) + "...\n"
    return result

class LibraryAI:
    def ask(self, text, mode="normal"):
        text_low = text.lower()
        
        if mode in ["search", "search_think"]:
            title, full_text = web_search(text)
            if full_text:
                if mode == "search_think":
                    summary = extract_key_facts(full_text, title)
                    critique = ""
                    if "беремен" in summary.lower() or "дет" in summary.lower():
                        critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Обратите внимание на разделы 'Беременность' и 'Дети'. Требуется особая осторожность!"
                    return f"🔍🧠 **[SEARCH + SIBTHINK]:**\n{summary}{critique}\n\n[AGENT_ID:Асклепий]"
                else:
                    return f"🔍 **[SEARCH]:**\nСогласно статье «{title}»:\n\n{full_text[:1000]}...\n\n[AGENT_ID:Цербер]"
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
                            critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Пожалуйста, сверьтесь с инструкцией!" if "язв" in draft.lower() else ""
                            stylist = "\n\n📖 **[СТИЛИСТ | Даль]:** Текст вычитан."
                            source = "\n\n📌 *Источник: Внутренняя база знаний ИИ*"
                            
                            header = "🧠 **[SIBTHINK]:**\n" if mode == "sibthink" else "🚀 **[CHAT]:**\n"
                            return header + draft + critique + stylist + source + f"\n\n[AGENT_ID:{agent.name}]"
        return None

class ProAI:
    def ask(self, text):
        return f"💬 [PRO] Запрос сложен. Загрузите файл или включите 'Search+Think'.\n\n[AGENT_ID:Цербер]"

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
