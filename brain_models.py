class Agent:
    def __init__(self, name):
        self.name = name
        self.accuracy = 50.0  # Начинаем с 50%
        self.knowledge = 0

    def train(self, amount):
        self.knowledge += amount
        # Формула роста: чем больше знаний, тем выше точность (но не больше 100)
        self.accuracy = min(100.0, 50.0 + (self.knowledge * 2.5))

    def teach(self, other_agent):
        # Сильный учит слабого
        if self.accuracy > other_agent.accuracy:
            other_agent.knowledge += 1
            other_agent.accuracy = min(100.0, 50.0 + (other_agent.knowledge * 2.5))

# Создаем наших агентов
MED_ASKL = Agent("Асклепий")
MED_HIPPO = Agent("Гиппократ")
FIN_MORGAN = Agent("Морган")
DICT_DAL = Agent("Даль")
SEC_CERBER = Agent("Цербер")
