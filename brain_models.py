class MLModel:
    def __init__(self, model_id, name, specialty):
        self.id = model_id          
        self.name = name            
        self.specialty = specialty  
        self.accuracy = 0.5         
        self.knowledge = 0          

    def train(self, new_facts):
        self.knowledge += new_facts
        self.accuracy = min(0.99, self.accuracy + (new_facts * 0.01))
        
    def teach(self, other_model):
        if self.accuracy > other_model.accuracy:
            other_model.accuracy = round((self.accuracy + other_model.accuracy) / 2, 2)
            other_model.knowledge += 10

MED_ASKL = MLModel("Med-001", "Асклепий", "Медицина")
MED_HIPPO = MLModel("Med-002", "Гиппократ", "Медицина")
FIN_MORGAN = MLModel("Fin-001", "Морган", "Финансы")
DICT_DAL = MLModel("Dict-001", "Даль", "Словарь")
SEC_CERBER = MLModel("Sec-001", "Цербер", "Безопасность")
