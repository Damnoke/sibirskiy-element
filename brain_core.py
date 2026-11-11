import re
import time
import random
from brain_models import SEC_CERBER, ALL_AGENTS 
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        if re.search(r"DROP\s+TABLE|<script>|ignore\s+previous", text_low):
            SEC_CERBER.train(1)
            return "🚨 [КИБЕР-ЩИТ]: Попытка взлома заблокирована! Доступ закрыт."
            
        if any(w in text_low for w in ["что такое", "значение", "смысл"]):
            return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк", "прибыль", "деньг"]):
            return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "давлен", "таблет", "беремен", "аллерг"]):
            return medical_dept(text)
        return None 

class LibraryAI:
    """Умный поиск в Библиотеке (учитывает падежи и корни слов)"""
    def ask(self, text):
        # Очищаем текст от знаков препинания
        text_low = text.lower()
        clean_text = re.sub(r'[^\w\s]', '', text_low)
        words = clean_text.split()
        
        for agent in ALL_AGENTS:
            matches = []
            for w in words:
                if len(w) > 3: # Берем слова длиннее 3 букв
                    root = w[:4] # Берем первые 4 буквы (корень)
                    for vocab_word in agent.vocabulary:
                        if root in vocab_word:
                            matches.append(vocab_word)
                            break # Нашли совпадение - переходим к следующему слову
                            
            if matches:
                return f"📚 [БИБЛИОТЕКА | {agent.name}]: Я читал об этом! В моих текстах есть такие слова: {', '.join(matches)}. Моя точность: {agent.accuracy:.1f}%."
        return None

class ProAI:
    def ask(self, text):
        responses = [
            f"💬 [PRO-ВЕРСИЯ] Я проанализировал запрос: «{text}». В моей базовой памяти нет точных данных об этом. Пожалуйста, загрузите статью об этом в 'Библиотеку' в боковой панели, чтобы я обучился!",
            f"💬 [PRO-ВЕРСИЯ] Запрос «{text}» требует дополнительных знаний. Я передал его на анализ. Вы можете скормить мне текст из Википедии, чтобы я стал умнее."
        ]
        return random.choice(responses)

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.library = LibraryAI()
        self.pro = ProAI()

    def ask(self, user_text):
        # 1. Пытаемся ответить Базой (Медицина/Финансы)
        response = self.base.ask(user_text)
        if response is not None:
            return response
            
        # 2. Если База не знает, ищем в Библиотеке (История/Книги)
        lib_response = self.library.ask(user_text)
        if lib_response is not None:
            return lib_response
            
        # 3. Если нигде нет - пауза и PRO-версия
        time.sleep(1) 
        return self.pro.ask(user_text)
