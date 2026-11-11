import json
import os
import hashlib
import random

class Agent:
    def __init__(self, name, accuracy=50.0, knowledge=0):
        self.name = name
        self.accuracy = accuracy
        self.knowledge = knowledge
        self.hidden_memory = set() # Для ответов
        self.vocabulary = set()    # Для новых слов из книг

    def challenge_and_grow(self, response_text):
        response_hash = hashlib.md5(response_text.lower().encode()).hexdigest()
        if response_hash in self.hidden_memory:
            return False, "Ответ уже был в памяти. Развития нет (топчемся на месте)."
        self.hidden_memory.add(response_hash)
        self.knowledge += 1
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 2.5))
        if len(self.hidden_memory) > 100: self.hidden_memory.pop()
        save_agents()
        return True, f"✅ Новое знание внедрено! {self.name} стал умнее (+2.5%)."

    def teach(self, other_agent):
        if self.accuracy > other_agent.accuracy:
            other_agent.knowledge += 1
            other_agent.accuracy = min(100.0, 50.0 + (other_agent.knowledge * 2.5))
            save_agents()

    def read_book(self, text):
        """Библиотекарь: читает текст и учит новые слова"""
        # Разбиваем текст на уникальные слова
        words = set(text.lower().replace(".", "").replace(",", "").replace("!", "").replace("?", "").split())
        
        # Ищем те слова, которых агент еще не знает
        new_words = words - self.vocabulary
        
        if len(new_words) > 0:
            self.vocabulary.update(new_words)
            # Даем знания: за каждые 10 новых слов даем +1 к знаниям
            knowledge_gain = max(1, len(new_words) // 10)
            self.knowledge += knowledge_gain
            self.accuracy = min(100.0, 50.0 + (self.knowledge * 2.5))
            save_agents()
            return f"📖 {self.name} прочитал текст! Изучено новых слов: {len(new_words)}. Получено знаний: +{knowledge_gain}. Текущая точность: {self.accuracy:.1f}%"
        else:
            return f"⏸️ {self.name} уже знает все слова из этого текста. Новых знаний нет."

    def to_dict(self):
        return {
            "name": self.name, 
            "accuracy": self.accuracy, 
            "knowledge": self.knowledge,
            "vocabulary": list(self.vocabulary)
        }

# --- СИСТЕМА СОХРАНЕНИЯ ПАМЯТИ ---
DB_FILE = "agents_db.json"

def load_agents():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                agents = []
                for d in data:
                    agent = Agent(d["name"], d["accuracy"], d["knowledge"])
                    if "vocabulary" in d:
                        agent.vocabulary = set(d["vocabulary"])
                    agents.append(agent)
                return agents
        except:
            pass
    return [Agent("Асклепий"), Agent("Гиппократ"), Agent("Морган"), Agent("Даль"), Agent("Цербер")]

def save_agents():
    if 'ALL_AGENTS' in globals():
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in ALL_AGENTS], f, ensure_ascii=False, indent=4)

ALL_AGENTS = load_agents()

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
        if agent.name == name: return False, f"Агент с именем {name} уже существует."
    new_agent = Agent(name=name, accuracy=50.0, knowledge=0)
    ALL_AGENTS.append(new_agent)
    save_agents()
    return True, f"🎉 Агент {name} успешно нанят в отдел {category}!"
