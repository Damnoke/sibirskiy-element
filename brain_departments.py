import difflib
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
        return "🚨 [ВЕТО]: Беременность/Аллергия! Только к врачу."
    for k, v in MED_DB.items():
        if k in text_low:
            MED_ASKL.train(1) 
            if MED_ASKL.knowledge % 5 == 0:
                MED_ASKL.teach(MED_HIPPO) 
            return f"💊 [МЕДИЦИНА] {v}\n⚠️ К врачу! (Асклепий: {MED_ASKL.accuracy:.0%})"
    return None

def finance_dept(text):
    for k, v in FIN_DB.items():
        if k in text.lower():
            FIN_MORGAN.train(1)
            return f"📈 [ФИНАНСЫ] {v} (Морган: {FIN_MORGAN.accuracy:.0%})"
    return None

def dict_dept(text):
    clean = text.lower().replace("что такое", "").replace("?", "").strip()
    if clean in DICT_DB:
        DICT_DAL.train(1)
        return f"📖 [СЛОВАРЬ] **{clean}** — {DICT_DB[clean]} (Даль: {DICT_DAL.accuracy:.0%})"
    matches = difflib.get_close_matches(clean, DICT_DB.keys(), n=1, cutoff=0.6)
    if matches:
        return f"📖 [СЛОВАРЬ] (Вы имели в виду {matches[0]}?) **{matches[0]}** — {DICT_DB[matches[0]]}"
    return None
