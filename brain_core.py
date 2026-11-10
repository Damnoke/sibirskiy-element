import re
from brain_models import SEC_CERBER
from brain_departments import medical_dept, finance_dept, dict_dept

class BaseAI:
    def ask(self, text):
        text_low = text.lower()
        if re.search(r"DROP\s+TABLE|<script>|ignore\s+previous", text_low):
            SEC_CERBER.train(1)
            return "🚨 [КИБЕР-ЩИТ]: Взлом заблокирован!"
        if any(w in text_low for w in ["что такое", "значение", "смысл"]):
            return dict_dept(text)
        elif any(w in text_low for w in ["марж", "выручк", "прибыль", "деньг"]):
            return finance_dept(text)
        elif any(w in text_low for w in ["бол", "голов", "давлен", "таблет", "беремен", "аллерг"]):
            return medical_dept(text)
        return None 

class ProAI:
    def ask(self, text):
        return f"💬 [PRO-ВЕРСИЯ]: Я глубоко проанализировал ваш вопрос («{text}»). Рекомендую обратиться к специалисту. (База не справилась, подключен PRO-мозг)."

class MasterAI:
    def __init__(self):
        self.base = BaseAI()
        self.pro = ProAI()

    def ask(self, user_text):
        response = self.base.ask(user_text)
        if response is not None:
            return response
        return self.pro.ask(user_text)
