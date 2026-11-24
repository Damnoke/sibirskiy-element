import json
import os
import hashlib
import random
import re
import sqlite3
import csv 

class Agent:
    def __init__(self, name, category="Общее", accuracy=50.0, knowledge=0):
        self.name = name
        self.category = category 
        self.accuracy = accuracy
        self.knowledge = knowledge
        self.hidden_memory = set()
        self.vocabulary = set()
        self.chain = {} 

    def get_level(self):
        if self.knowledge > 30: return "Большой (Large) 🦅"
        elif self.knowledge > 10: return "Средний (Medium) 🐺"
        else: return "Малый (Small) 🐣"

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
            
            if self.get_level() == "Большой (Large) 🦅":
                self.teach_others()

            save_agents()
            return f"📖 {self.name} ({self.get_level()}) изучил текст! Новых слов: {new_words_count}."
        return f"⏸️ {self.name} уже знает все слова из этого текста."

    def teach_others(self):
        global ALL_AGENTS
        bridge_topics = {"Финансы": ["Медицина"], "Медицина": ["Финансы", "Безопасность"]}
        for agent in ALL_AGENTS:
            if agent.name == self.name: continue 
            if agent.category == self.category and agent.get_level() == "Малый (Small) 🐣":
                agent.knowledge += 1
                agent.accuracy = min(100.0, 50.0 + (agent.knowledge * 0.25))
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
        return " ".join(result).replace(" .", ".").replace(" ,", ",")

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
        best_draft = re.sub(r'\.\s*([а-яё])', lambda m: '. ' + m.group(1).upper(), best_draft)
        
        return f"📝 [{self.name} ({self.get_level()})]:\n{best_draft}"

    def to_dict(self):
        return {"name": self.name, "category": self.category, "accuracy": self.accuracy, "knowledge": self.knowledge, "vocabulary": list(self.vocabulary), "chain": self.chain}

DB_FILE = "agents_database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents
                 (name TEXT PRIMARY KEY, category TEXT, accuracy REAL, knowledge INTEGER, vocabulary TEXT, chain TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS medicines
                 (name TEXT PRIMARY KEY, is_prescription INTEGER, forms TEXT, analogs TEXT, dosage TEXT, description TEXT, indications TEXT)''')
    conn.commit()
    conn.close()

def load_medicines_from_csv():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # ПРИНУДИТЕЛЬНАЯ ЗАГРУЗКА: Всегда читаем CSV и обновляем базу
    if os.path.exists("medicines.csv"):
        try:
            with open("medicines.csv", "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    c.execute('''INSERT OR REPLACE INTO medicines (name, is_prescription, forms, analogs, dosage, description, indications) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                              (row["name"], int(row["is_prescription"]), row["forms"], row["analogs"], row["dosage"], row["description"], row.get("indications", "")))
            conn.commit()
            print("CSV успешно синхронизирован с базой!")
        except Exception as e:
            print(f"Ошибка чтения CSV: {e}")
    else:
        # Если файла нет, грузим базовые тестовые данные
        c.execute("SELECT COUNT(*) FROM medicines")
        if c.fetchone()[0] == 0:
            test_meds = [
                ("Ибупрофен", 0, "Таблетки, мазь, сироп", "Нурофен, Миг 400", "200-400 мг 3 раза в день", "НПВС, жаропонижающее", "Головная боль, температура, ОРВИ, зубная боль"),
                ("Парацетамол", 0, "Таблетки, свечи, сироп", "Панадол, Эффералган", "500-1000 мг до 4 раз в день", "Жаропонижающее", "Простуда, температура, ОРВИ"),
                ("Ксилометазолин", 0, "Спрей, капли", "Снуп, Тизин, Галазолин", "По 1 впрыску в каждый носовой ход", "Сосудосуживающее", "Насморк, заложенность носа"),
                ("Амоксициллин", 1, "Таблетки, порошок", "Амосин, Флемоксин Солютаб", "500 мг 3 раза в день", "Антибиотик (строго по рецепту!)", "Бактериальные инфекции, ангина"),
                ("Трамадол", 1, "Таблетки, раствор", "Трамал", "50-100 мг по назначению врача", "Опиоидный анальгетик (рецептурный)", "Сильная боль, травмы"),
            ]
            c.executemany("INSERT INTO medicines VALUES (?, ?, ?, ?, ?, ?, ?)", test_meds)
            conn.commit()
            
    conn.close()

def load_medicines():
    load_medicines_from_csv()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, is_prescription, forms, analogs, dosage, description, indications FROM medicines")
    rows = c.fetchall()
    conn.close()
    
    meds_dict = {}
    for row in rows:
        meds_dict[row[0].lower()] = {
            "name": row[0],
            "is_prescription": bool(row[1]),
            "forms": row[2],
            "analogs": row[3],
            "dosage": row[4],
            "description": row[5],
            "indications": row[6]
        }
    return meds_dict

MEDICINES_REGISTRY = load_medicines()

def load_agents():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, category, accuracy, knowledge, vocabulary, chain FROM agents")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        agents = [Agent("Асклепий", "Медицина"), Agent("Гиппократ", "Медицина"), Agent("Морган", "Финансы"), Agent("Даль", "Словарь"), Agent("Цербер", "Безопасность")]
        save_agents(agents)
        return agents
        
    agents = []
    for row in rows:
        name, category, accuracy, knowledge, vocab_str, chain_str = row
        agent = Agent(name, category, accuracy, knowledge)
        if vocab_str: agent.vocabulary = set(json.loads(vocab_str))
        if chain_str: agent.chain = json.loads(chain_str)
        agents.append(agent)
    return agents

def save_agents(agents_list=None):
    if agents_list is None:
        if 'ALL_AGENTS' in globals(): agents_list = ALL_AGENTS
        else: return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for a in agents_list:
        vocab_str = json.dumps(list(a.vocabulary), ensure_ascii=False)
        chain_str = json.dumps(a.chain, ensure_ascii=False)
        c.execute('''INSERT OR REPLACE INTO agents (name, category, accuracy, knowledge, vocabulary, chain) VALUES (?, ?, ?, ?, ?, ?)''', (a.name, a.category, a.accuracy, a.knowledge, vocab_str, chain_str))
    conn.commit()
    conn.close()

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
