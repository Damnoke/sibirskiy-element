import difflib
import random
import brain_models
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL

DEFAULT_MED = {"голов": "Цитрамон 1 таб.", "давлен": "Капотен."}
DEFAULT_FIN = {"марж": "Маржа = (Цена - Закупка) / Цена * 100%"}
DEFAULT_DICT = {"эмпатия": "способность понимать чувства."}

def medical_dept(text):
    text_low = text.lower()
    if "беремен" in text_low or "аллерг" in text_low:
        return "🚨 [ВЕТО]: Беременность/Аллергия! Только к врачу."
        
    for k, v in DEFAULT_MED.items():
        if k in text_low:
            MED_ASKL.knowledge += 1
            MED_ASKL.accuracy = min(100.0, 50.0 + (MED_ASKL.knowledge * 2.5))
            brain_models.save_agents()
            return f"💊 [МЕДИЦИНА] {v}\n⚠️ К врачу! (Асклепий: {MED_ASKL.accuracy:.0f}%)"
    return None

def finance_dept(text):
    for k, v in DEFAULT_FIN.items():
        if k in text.lower():
            FIN_MORGAN.knowledge += 1
            FIN_MORGAN.accuracy = min(100.0, 50.0 + (FIN_MORGAN.knowledge * 2.5))
            brain_models.save_agents()
            return f"📈 [ФИНАНСЫ] {v} (Морган: {FIN_MORGAN.accuracy:.0f}%)"
    return None

def dict_dept(text):
    clean = text.lower().replace("что такое", "").replace("?", "").strip()
    if clean in DEFAULT_DICT:
        DICT_DAL.knowledge += 1
        DICT_DAL.accuracy = min(100.0, 50.0 + (DICT_DAL.knowledge * 2.5))
        brain_models.save_agents()
        return f"📖 [СЛОВАРЬ] {clean.capitalize()} — это {DEFAULT_DICT[clean]} (Даль: {DICT_DAL.accuracy:.0f}%)"
    return None
