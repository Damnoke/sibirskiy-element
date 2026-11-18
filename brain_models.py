import json
import os
import hashlib
import random
import re

class Agent:
    def __init__(self, name, category="Общее", accuracy=50.0, knowledge=0):
        self.name = name
        self.category = category # Отдел (Медицина, Финансы и т.д.)
        self.accuracy = accuracy
        self.knowledge = knowledge
        self.hidden_memory = set()
        self.vocabulary = set()
        self.chain = {} 

    def get_level(self):
        """Определяет уровень агента на основе его знаний"""
        if self.knowledge > 30:
            return "Большой (Large) 🦅"
        elif self.knowledge > 10:
            return "Средний (Medium) 🐺"
        else:
            return "Малый (Small) 🐣"

    def challenge_and_grow(self, response_text):
        response_hash = hashlib.md5(response_text.lower().encode()).hexdigest()
        if response_hash in self.hidden_memory:
            return False, "Ответ уже был в памяти. Развития нет."
        self.hidden_memory.add(response_hash)
        self.knowledge += 1
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 0.25))
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
            if word not in self.chain: 
                self.chain[word] = {}
            if next_word not in self.chain[word]:
                self.chain[word][next_word] = 0
            self.chain[word][next_word] += 1

        self.prune_memory()

        if new_words_count > 0:
            knowledge_gain = max(1, new_words_count // 10)
            self.knowledge += knowledge_gain
            self.accuracy = min(100.0, 50.0 + (self.knowledge * 0.25))
            
            # МЕХАНИЗМ ОБУЧЕНИЯ: Если агент стал Большим, он учит других
            if self.get_level() == "Большой (Large) 🦅":
                self.teach_others()

            save_agents()
            return f"📖 {self.name} ({self.get_level()}) изучил текст! Новых слов: {new_words_count}."
        return f"⏸️ {self.name} уже знает все слова из этого текста."

    def teach_others(self):
        """Большой агент передает знания Малым (внутри отдела и по мостам)"""
        global ALL_AGENTS
        
        # Твоя идея: Межотраслевые мосты
        bridge_topics = {
            "Финансы": ["Медицина"], 
            "Медицина": ["Финансы", "Безопасность"]
        }

        for agent in ALL_AGENTS:
            if agent.name == self.name: 
                continue 

            # 1. Обучение внутри отдела
            if agent.category == self.category and agent.get_level() == "Малый (Small) 🐣":
                agent.knowledge += 1
                agent.accuracy = min(100.0, 50.0 + (agent.knowledge * 0.25))

            # 2. Межотраслевое обучение (Мосты)
            elif self.category in bridge_topics:
                if agent.category in bridge_topics[self.category] and agent.get_level() != "Большой (Large) 🦅":
                    agent.knowledge += 1 
                    agent.accuracy = min(100.0, 50.0 + (agent.knowledge * 0.25))

    def prune_memory(self, max_connections=15):
        for word in self.chain:
            if len(self.chain[word]) > max_connections:
                sorted_connections = sorted(self.chain[word].items(), key=lambda item: item[1], reverse=True)[:max_connections]
                self.chain[word] = dict(sorted_connections)

    def _generate_single_draft(self, start_word, max_len):
        current_word = start_word
        result = [current_word.capitalize()]
        for _ in range(max_len):
            if current_word in self.chain and len(self.chain[current_word]) > 0:
                words_list = list(self.chain[current_word].keys())
                weights = list(self.chain[current_word].values())
                next_word = random.choices(words_list, weights=weights, k=1)[0]
                result.append(next_word)
                current_word = next_word
            else: break
        return " ".join(result).replace(" .", ".").replace(" ,", ",").capitalize()

    def generate_text(self, start_word, length_type="Средний"):
        if start_word not in self.vocabulary:
            return f"Я не нашел слово '{start_word}' в своих знаниях."
            
        if length_type == "Короткий": max_len = 15
        elif length_type == "Длинный": max_len = 80
        else: max_len = 40
        
        drafts = [self._generate_single_draft(start_word, max_len) for _ in range(3)]
        
        best_draft = ""
        best_score = -1
        
        for draft in drafts:
            words = draft.split()
            length_score = len(words)
            repeat_penalty = sum(2 for i in range(len(words)-1) if words[i].lower() == words[i+1].lower())
            score = length_score - repeat_penalty
            
            if score > best_score:
                best_score = score
                best_draft = draft

        if not best_draft.endswith("."): best_draft += "."
        return f"📝 [{self.name} ({self.get_level()})]:\n{best_draft}"

    def to_dict(self):
        return {"name": self.name, "category": self.category, "accuracy": self.accuracy, "knowledge": self.knowledge, "vocabulary": list(self.vocabulary), "chain": self.chain}

DB_FILE = "agents_db.json"

def load_agents():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not data: raise ValueError("Empty data")
                agents = []
                for d in data:
                    cat = d.get("category", "Общее") 
                    agent = Agent(d["name"], category=cat, accuracy=d["accuracy"], knowledge=d["knowledge"])
                    if "vocabulary" in d: agent.vocabulary = set(d["vocabulary"])
                    if "chain" in d: agent.chain = d["chain"]
                    agents.append(agent)
                return agents
        except: pass
    return [
        Agent("Асклепий", "Медицина"), 
        Agent("Гиппократ", "Медицина"), 
        Agent("Морган", "Финансы"), 
        Agent("Даль", "Словарь"), 
        Agent("Цербер", "Безопасность")
    ]

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
    return f"🗣️ **{top_agent.name}** [{top_agent.category}] ({top_agent.get_level()}) просит слова:\n*\"Я застрял на {top_agent.accuracy:.1f}%. Мне нужен новый материал!\"*"

def hire_new_agent(name, category):
    global ALL_AGENTS
    for agent in ALL_AGENTS:
        if agent.name == name: return False, f"Агент {name} уже есть."
    new_agent = Agent(name=name, category=category, accuracy=50.0, knowledge=0)
    ALL_AGENTS.append(new_agent)
    save_agents()
    return True, f"🎉 Агент {name} нанят в отдел {category}!"
