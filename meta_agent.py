import random
from brain_models import ALL_AGENTS

class MetaArchitect:
    def analyze_system(self):
        stagnant_agents = [a for a in ALL_AGENTS if a.accuracy < 60.0]
        if not stagnant_agents: return "🟢 Все агенты развиваются нормально."
        worst_agent = min(stagnant_agents, key=lambda a: a.accuracy)
        names = ["Авиценна", "Парацельс", "Гален", "Флеминг", "Павлов"]
        new_name = random.choice(names)
        return {
            "target_agent": worst_agent.name,
            "new_agent_name": new_name,
            "category": worst_agent.category,
            "current_accuracy": worst_agent.accuracy,
            "message": f"{worst_agent.name} застрял на {worst_agent.accuracy:.1f}%. Предлагаю нанять '{new_name}' в отдел {worst_agent.category}!"
        }
