import re
import time
import random
from brain_models import SEC_CERBER
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        # Защита Цербера
        if re.search(r"DROP\s+TABLE|<script>|ignore\s+previous", text_low):
            SEC_CERBER.train(1)
            return "🚨 [КИБЕР-ЩИТ]: Попытка взлома заблокирована! Доступ закрыт."
            
        # Маршрутизация по отделам
        if any(w in text_low for w in ["что такое", "значение", "смысл"]):
            return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк", "прибыль", "деньг"]):
            return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "давлен", "таблет", "беремен", "аллерг"]):
            return medical_dept(text)
        return None 

class ProAI:
    def ask(self, text):
        # Имитация глубокого анализа для непонятных запросов
        responses = [
            f"💬 [PRO-ВЕРСИЯ] Я проанализировал ваш запрос: «{text}». Это довольно сложный случай. Рекомендую не заниматься самолечением, а обратиться к профильному специалисту.",
            f"💬 [PRO-ВЕРСИЯ] Мой базовый модуль не нашел точного ответа на вопрос «{text}». Я подключил глубокий анализ. Пожалуйста, уточните детали или проконсультируйтесь с врачом.",
            f"💬 [PRO-ВЕРСИЯ] Запрос «{text}» требует более детального изучения. Я передал его на анализ. Рекомендую обратиться в ближайшую аптеку для консультации с провизором."
        ]
        return random.choice(responses)

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.pro = ProAI()

    def ask(self, user_text):
        # 1. Пытаемся ответить Базой (быстро и по факту)
        response = self.base.ask(user_text)
        
        # 2. Если База знает ответ — выдаем
        if response is not None:
            return response
            
        # 3. Если База не знает — пауза 1 сек (эффект "думания") и зовем PRO
        time.sleep(1) 
        return self.pro.ask(user_text)
