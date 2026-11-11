import difflib
import random
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL
from brain_library import load_knowledge

DEFAULT_MED = {"голов": "Цитрамон 1 таб.", "давлен": "Капотен."}
DEFAULT_FIN = {"марж": "Маржа = (Цена - Закупка) / Цена * 100%"}
DEFAULT_DICT = {"эмпатия": "способность понимать чувства.", "синекура": "должность без труда."}

MED_DB = load_knowledge("medicines.json", DEFAULT_MED)
FIN_DB = load_knowledge("finances.json", DEFAULT_FIN)
DICT_DB = load_knowledge("ozhegov.json", DEFAULT_DICT)

def medical_dept(text):
    text_low = text.lower()
    if "беремен" in text_low or "аллерг" in text_low:
        return "🚨 [ВЕТО]: Беременность/Аллергия! Только к врачу. Самолечение опасно."
        
    for k, v in MED_DB.items():
        if k in text_low:
            templates = [
                f"💊 [МЕДИЦИНА] Обычно в таких случаях помогает {v}. Обязательно проконсультируйтесь с врачом!",
                f"💊 [МЕДИЦИНА] По вашему симптому могу порекомендовать {v}. Но лучше обратиться к специалисту.",
                f"💊 [МЕДИЦИНА] В аптеке есть {v}. Пейте строго по инструкции и следите за реакцией организма."
            ]
            base_response = random.choice(templates)
            success, msg = MED_ASKL.challenge_and_grow(base_response)
            
            if success and MED_ASKL.knowledge % 5 == 0:
                MED_ASKL.teach(MED_HIPPO) 
                
            status = msg if success else f"⏸️ {msg}"
            return base_response + f"\n(MED_ASKL: {MED_ASKL.accuracy:.0f}% | {status})"
    return None 

def finance_dept(text):
    for k, v in FIN_DB.items():
        if k in text.lower():
            templates = [
                f"📈 [ФИНАНСЫ] Вот как это считается: {v}",
                f"📈 [ФИНАНСЫ] Формула проста: {v}",
                f"📈 [ФИНАНСЫ] Для точных расчетов используйте: {v}"
            ]
            base_response = random.choice(templates)
            success, msg = FIN_MORGAN.challenge_and_grow(base_response)
            
            status = msg if success else f"⏸️ {msg}"
            return base_response + f"\n(Морган: {FIN_MORGAN.accuracy:.0f}% | {status})"
    return None

def dict_dept(text):
    clean = text.lower().replace("что такое", "").replace("?", "").strip()
    if clean in DICT_DB:
        templates = [
            f"📖 [СЛОВАРЬ] {clean.capitalize()} — это {DICT_DB[clean]}",
            f"📖 [СЛОВАРЬ] Значение слова {clean}: {DICT_DB[clean]}",
            f"📖 [СЛОВАРЬ] {clean.capitalize()} означает {DICT_DB[clean]}"
        ]
        base_response = random.choice(templates)
        success, msg = DICT_DAL.challenge_and_grow(base_response)
        
        status = msg if success else f"⏸️ {msg}"
        return base_response + f"\n(Даль: {DICT_DAL.accuracy:.0f}% | {status})"
        
    matches = difflib.get_close_matches(clean, DICT_DB.keys(), n=1, cutoff=0.6)
    if matches:
        return f"📖 [СЛОВАРЬ] Вы имели в виду «{matches[0]}»? Это {DICT_DB[matches[0]]}"
    return None
