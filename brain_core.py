import re
import time
import random
import brain_models 
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        if re.search(r"DROP\s+TABLE|<script>", text_low):
            brain_models.SEC_CERBER.knowledge += 1
            brain_models.SEC_CERBER.accuracy = min(100.0, 50.0 + (brain_models.SEC_CERBER.knowledge * 0.25))
            brain_models.save_agents()
            return "🚨 [КИБЕР-ЩИТ]: Атака отбита."
            
        if any(w in text_low for w in ["что такое", "значение"]): return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк"]): return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "таблет"]): return medical_dept(text)
        return None 

class LibraryAI:
    def ask(self, text):
        text_low = text.lower()
        
        length_type = "Средний"
        if any(w in text_low for w in ["коротко", "кратко", "быстро"]): length_type = "Короткий"
        elif any(w in text_low for w in ["подробно", "длинно", "всё", "полностью"]): length_type = "Длинный"

        clean_text = re.sub(r'[^\w\s]', '', text_low)
        stop_words = ["расскажи", "коротко", "подробно", "про", "что", "ты", "знаешь", "мне", "как", "это"]
        words = [w for w in clean_text.split() if w not in stop_words]

        for agent in brain_models.ALL_AGENTS:
            for w in words:
                if len(w) > 3:
                    root = w[:4]
                    for vocab_word in agent.vocabulary:
                        if root in vocab_word:
                            
                            # --- СОВЕТ АГЕНТОВ НАЧИНАЕТ РАБОТУ ---
                            
                            # 1. АВТОР (Гиппократ) пишет черновик (с рефлексией)
                            draft = agent.generate_text(vocab_word, length_type=length_type)
                            
                            # 2. КРИТИК (Асклепий) проверяет черновик
                            critique = ""
                            if agent.name != "Асклепий" and "Асклепий" in [a.name for a in brain_models.ALL_AGENTS]:
                                if "язв" in draft.lower():
                                    critique = "\n\n🚨 **[КРИТИК | Асклепий]:** Внимание! В тексте упомянута язва. Ибупрофен может быть противопоказан при язвенной болезни! Требуется проверка врачом."
                            
                            # 3. СТИЛИСТ (Даль) причесывает текст
                            stylist_report = ""
                            dal = next((a for a in brain_models.ALL_AGENTS if a.name == "Даль"), None)
                            if dal:
                                # Даль делает базовую чистку: убирает двойные пробелы и ставит точки
                                polished_draft = draft.replace("  ", " ").replace(" ,", ",").replace(" .", ".").strip()
                                if not polished_draft.endswith("."):
                                    polished_draft += "."
                                stylist_report = "\n\n📖 **[СТИЛИСТ | Даль]:** Текст вычитан. Стиль и пунктуация приведены в порядок."
                                final_text = polished_draft
                            else:
                                final_text = draft

                            return final_text + critique + stylist_report
        return None

class ProAI:
    def ask(self, text):
        return f"💬 [PRO-ВЕРСИЯ] Запрос «{text}» сложен. Загрузите текст в 'Библиотеку', чтобы я обучился."

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.library = LibraryAI()
        self.pro = ProAI()

    def ask(self, user_text):
        response = self.base.ask(user_text)
        if response: return response
        
        lib_response = self.library.ask(user_text)
        if lib_response: return lib_response
        
        time.sleep(1) 
        return self.pro.ask(user_text)
