import random
from brain_models import ALL_AGENTS, hire_new_agent

class MetaArchitect:
    def analyze_system(self):
        """Сканирует всех агентов и ищет застой"""
        stagnant_agents = [a for a in ALL_AGENTS if a.accuracy < 60.0]
        
        if not stagnant_agents:
            return "🟢 [СИСТЕМА]: Все агенты развиваются нормально. Патчи не требуются."

        worst_agent = min(stagnant_agents, key=lambda a: a.accuracy)
        
        # Предлагаем нанять помощника для застойного агента
        names = ["Авиценна", "Парацельс", "Гиппократ Мл.", "Гален", "Эскулап", "Флеминг", "Павлов"]
        new_name = random.choice(names)
        
        return {
            "target_agent": worst_agent.name,
            "new_agent_name": new_name,
            "category": worst_agent.name, # Упрощенно берем имя как категорию
            "current_accuracy": worst_agent.accuracy,
            "message": f"Я проанализировал систему. {worst_agent.name} застрял на {worst_agent.accuracy:.1f}%. Предлагаю нанять ему в помощь агента '{new_name}'!"
        }
