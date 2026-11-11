import random
from brain_models import MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER

class MetaArchitect:
    def __init__(self):
        pass

    def analyze_system(self):
        """Сканирует всех агентов и ищет застой"""
        agents = [MED_ASKL, MED_HIPPO, FIN_MORGAN, DICT_DAL, SEC_CERBER]
        
        # Ищем агентов с низкой точностью (меньше 60%)
        stagnant_agents = [a for a in agents if a.accuracy < 60.0]
        
        if not stagnant_agents:
            return "🟢 [СИСТЕМА]: Все агенты развиваются нормально. Патчи не требуются."

        # Выбираем самого застойного
        worst_agent = min(stagnant_agents, key=lambda a: a.accuracy)
        
        # Генерируем предложение по обновлению
        patch_types = [
            f"Добавить модуль веб-скрапинга (парсинга), чтобы {worst_agent.name} мог сам искать статьи по теме '{worst_agent.name}'.",
            f"Расширить базу знаний для отдела '{worst_agent.name}'. {worst_agent.name} жалуется на нехватку данных (точность {worst_agent.accuracy:.1f}%).",
            f"Обновить математическую модель генерации текста, чтобы {worst_agent.name} выдавал более связные ответы.",
            f"Создать суб-агента для '{worst_agent.name}'. Текущий {worst_agent.name} перегружен."
        ]
        
        proposal = random.choice(patch_types)
        
        return {
            "target_agent": worst_agent.name,
            "current_accuracy": worst_agent.accuracy,
            "patch_suggestion": proposal
        }
