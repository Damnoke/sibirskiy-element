import json
import os
import hashlib
import random

class Agent:
    def __init__(self, name, accuracy=50.0, knowledge=0):
        self.name = name
        self.accuracy = accuracy
        self.knowledge = knowledge
        self.hidden_memory = set()

    def challenge_and_grow(self, response_text):
        response_hash = hashlib.md5(response_text.lower().encode()).hexdigest()
        
        if response_hash in self.hidden_memory:
            return False, "Ответ уже был в памяти. Развития нет (топчемся на месте)."
        
        self.hidden_memory.add(response_hash)
        self.knowledge += 1
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 2.5))
        if len(self.hidden_memory) > 100:
            self.hidden_memory.pop()
            
        save_agents() # Сохраняем в файл
        return True, f"✅ Новое знание внедрено! {self.name} стал умнее (+2.5%)."

    def teach(self, other_agent):
        if self.accuracy > other_agent.accuracy:
            other_agent.knowledge += 1
            other_agent.accuracy = min(100.0, 50.0 + (other_agent.knowledge * 2.5))
            save_agents()

    def to_dict(self):
        return {"name": self.name, "accuracy": self.accuracy, "knowledge": self.knowledge}

# --- СИСТЕМА СОХРАНЕНИЯ ПАМЯТИ ---
DB_FILE = "agents_db.json"

def load_agents():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Agent(d["name"], d["accuracy"], d["knowledge"]) for d in data]
        except:
            pass
    return [
        Agent("Асклепий"), Agent("Гиппократ"), 
        Agent("Морган"), Agent("Даль"), Agent("Цербер")
    ]

def save_agents():
    if 'ALL_AGENTS' in globals():
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in ALL_AGENTS], f, ensure_ascii=False, indent=4)

# Загружаем агентов
ALL_AGENTS = load_agents()

# Алиасы для совместимости с другими файлами
MED_ASKL = next((a for a in ALL_AGENTS if a.name == "Асклепий"), ALL_AGENTS[0])
MED_HIPPO = next((a for a in ALL_AGENTS if a.name == "Гиппократ"), ALL_AGENTS[1])
FIN_MORGAN = next((a for a in ALL_AGENTS if a.name == "Морган"), ALL_AGENTS[2])
DICT_DAL = next((a for a in ALL_AGENTS if a.name == "Даль"), ALL_AGENTS[3])
SEC_CERBER = next((a for a in ALL_AGENTS if a.name == "Цербер"), ALL_AGENTS[4])

def hold_desire_council():
    desires = [{"agent": a, "score": 100.0 - a.accuracy} for a in ALL_AGENTS]
    desires.sort(key=lambda x: x["score"], reverse=True)
    top_agent = desires[0]["agent"]
    proposals = [
        f"Я чувствую, что мои знания застыли. Моя точность {top_agent.accuracy:.1f}%. Прошу дать мне новую задачу!",
        f"Мой потенциал требует раскрытия. Я хочу учиться дальше!",
        f"Коллеги, я застрял на уровне {top_agent.accuracy:.1f}%. Мне нужен новый материал!"
    ]
    return f"🗣️ **{top_agent.name}** просит слова:\n*\"{random.choice(proposals)}\"*"

def hire_new_agent(name, category):
    global ALL_AGENTS
    for agent in ALL_AGENTS:
        if agent.name == name:
            return False, f"Агент с именем {name} уже существует."
    new_agent = Agent(name=name, accuracy=50.0, knowledge=0)
    ALL_AGENTS.append(new_agent)
    save_agents()
    return True, f"🎉 Агент {name} успешно нанят в отдел {category}!"
