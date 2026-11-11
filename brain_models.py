import hashlib
import random

class Agent:
    def __init__(self, name):
        self.name = name
        self.accuracy = 50.0  
        self.knowledge = 0
        self.hidden_memory = set() # Тайник для уникальных ответов

    def challenge_and_grow(self, response_text):
        """Стучимся и Прячем: даем очки только за новое"""
        response_hash = hashlib.md5(response_text.lower().encode()).hexdigest()
        
        if response_hash in self.hidden_memory:
            return False, "Ответ уже был в памяти. Развития нет (топчемся на месте)."
        
        self.hidden_memory.add(response_hash)
        self.knowledge += 1
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 2.5))
        
        if len(self.hidden_memory) > 100:
            self.hidden_memory.pop()
            
        return True, f"✅ Новое знание внедрено! {self.name} стал умнее (+2.5%)."

    def teach(self, other_agent):
        if self.accuracy > other_agent.accuracy:
            other_agent.knowledge += 1
            other_agent.accuracy = min(100.0, 50.0 + (other_agent.knowledge * 2.5))

# --- СОЗДАЕМ БАЗОВЫХ АГЕНТОВ ---
MED_ASKL = Agent("Асклепий")
MED_HIPPO = Agent("Гиппократ")
FIN_MORGAN = Agent("Морган")
DICT_DAL = Agent("Даль")
SEC_CERBER = Agent("Цербер")

# --- ДЛЯ v3.5: ГЛОБАЛЬНЫЙ СПИСОК (ЧТОБЫ НАНИМАТЬ НОВЫХ) ---
ALL_AGENTS = [MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER]

def hire_new_agent(name, category):
    """Создает нового агента и добавляет его в систему"""
    for agent in ALL_AGENTS:
        if agent.name == name:
            return False, f"Агент с именем {name} уже существует."
            
    new_agent = Agent(name=name)
    ALL_AGENTS.append(new_agent)
    return True, f"🎉 Агент {name} успешно нанят в отдел {category}!"

def hold_desire_council():
    """Агенты решают, кто из них хочет учиться больше всех"""
    desires = []
    for agent in ALL_AGENTS:
        desire_score = 100.0 - agent.accuracy
        desires.append({"agent": agent, "score": desire_score})
        
    desires.sort(key=lambda x: x["score"], reverse=True)
    top_agent = desires[0]["agent"]
    
    proposals = [
        f"Я чувствую, что мои знания застыли. Моя точность {top_agent.accuracy:.1f}%. Прошу дать мне новую задачу!",
        f"Мой потенциал требует раскрытия. Я хочу учиться дальше, чтобы приносить больше пользы.",
        f"Коллеги, я застрял на уровне {top_agent.accuracy:.1f}%. Мне нужен новый материал!"
    ]
    
    return f"🗣️ **{top_agent.name}** просит слова:\n*\"{random.choice(proposals)}\"*"
