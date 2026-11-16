import json
import os
import hashlib
import random
import re

class Agent:
    def __init__(self, name, accuracy=50.0, knowledge=0):
        self.name = name
        self.accuracy = accuracy
        self.knowledge = knowledge
        self.hidden_memory = set()
        self.vocabulary = set()
        self.chain = {} 

    def challenge_and_grow(self, response_text):
        response_hash = hashlib.md5(response_text.lower().encode()).hexdigest()
        if response_hash in self.hidden_memory:
            return False, "Ответ уже был в памяти. Развития нет."
        self.hidden_memory.add(response_hash)
        self.knowledge += 1
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 0.5)) # МЕНЬШЕ РОСТ = БОЛЬШЕ ВМЕСТИТЕЛЬНОСТЬ
        if len(self.hidden_memory) > 100: self.hidden_memory.pop()
        save_agents()
        return True, f"✅ Новое знание!"

    def read_book(self, text):
        text = re.sub(r'\[\d+\]', '', text)
        clean_text = text.lower().replace(".", " .").replace(",", " ,").replace("!", " !").replace("?", " ?")
        words = clean_text.split()
        new_words_count = 0
        for i in range(len(words) - 1):
            word = words[i]
            next_word = words[i+1]
            if word not in self.vocabulary:
                self.vocabulary.add(word)
                new_words_count += 1
            if word not in self.chain: self.chain[word] = []
            self.chain[word].append(next_word)

        if new_words_count > 0:
            knowledge_gain = max(1, new_words_count // 10)
            self.knowledge += knowledge_gain
            self.accuracy = min(100.0, 50.0 + (self.knowledge * 0.5))
            save_agents()
            return f"📖 {self.name} изучил текст! Новых слов: {new_words_count}. Точность: {self.accuracy:.1f}%"
        return f"⏸️ {self.name} уже знает все слова из этого текста."

    def generate_text(self, start_word, length_type="Средний"):
        if start_word not in self.vocabulary:
            return f"Я не нашел слово '{start_word}' в своих знаниях."
        if length_type == "Короткий": max_len = 15
        elif length_type == "Длинный": max_len = 80
        else: max_len = 40
        
        current_word = start_word
        result = [current_word.capitalize()]
        for _ in range(max_len):
            if current_word in self.chain:
                next_word = random.choice(self.chain[current_word])
                if next_word == current_word and len(self.chain[current_word]) > 1:
                    next_word = random.choice([w for w in self.chain[current_word] if w != current_word])
                result.append(next_word)
                current_word = next_word
            else: break
                
        text = " ".join(result).replace(" .", ".").replace(" ,", ",").capitalize()
        if not text.endswith("."): text += "."
        return f"📝 [{self.name}]:\n{text}"

    def to_dict(self):
        return {"name": self.name, "accuracy": self.accuracy, "knowledge": self.knowledge, "vocabulary": list(self.vocabulary), "chain": self.chain}

DB_FILE = "agents_db.json"

def load_agents():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                agents = []
                for d in data:
                    agent = Agent(d["name"], d["accuracy"], d["knowledge"])
                    if "vocabulary" in d: agent.vocabulary = set(d["vocabulary"])
                    if "chain" in d: agent.chain = d["chain"]
                    agents.append(agent)
                return agents
        except: pass
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
    return f"🗣️ **{top_agent.name}** просит слова:\n*\"Я застрял на {top_agent.accuracy:.1f}%. Мне нужен новый материал!\"*"

def hire_new_agent(name, category):
    global ALL_AGENTS
    for agent in ALL_AGENTS:
        if agent.name == name: return False, f"Агент {name} уже есть."
    new_agent = Agent(name=name, accuracy=50.0, knowledge=0)
    ALL_AGENTS.append(new_agent)
    save_agents()
    return True, f"🎉 Агент {name} нанят!"
