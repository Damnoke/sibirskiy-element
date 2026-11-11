import re
import time
import random
from brain_models import SEC_CERBER, ALL_AGENTS # Берем всех агентов
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
    """НОВЫЙ МОЗГ: Ищет ответы в том, что агенты прочитали в Библиотеке"""
    def ask(self, text):
        text_low = text.lower()
        words = text_low.replace("?", "").replace("!", "").replace(".", "").split()
        
        # Ищем агента, который знает эти слова
        for agent in ALL_AGENTS:
            # Проверяем, есть ли слова из вопроса в словаре агента (длиной больше 3 букв)
            matches = [w for w in words if w in agent.vocabulary and len(w) > 3]
            
            if matches:
                # Если агент нашел знакомые слова - он отвечает!
                return f"📚 [БИБЛИОТЕКА | {agent.name}]: Я читал об этом! В моих текстах есть такие слова: {', '.join(matches)}. Моя точность по этим данным составляет {agent.accuracy:.1f}%."
        return None

class ProAI:
    def ask(self, text):
        # Убираем тупую медицинскую заглушку, делаем умнее
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
