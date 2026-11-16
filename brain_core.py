class LibraryAI:
    def ask(self, text):
        text_low = text.lower()
        
        # МАГИЯ: ИИ сам определяет длину ответа по твоему запросу!
        length_type = "Средний"
        if any(w in text_low for w in ["коротко", "кратко", "быстро"]):
            length_type = "Короткий"
        elif any(w in text_low for w in ["подробно", "длинно", "всё", "полностью"]):
            length_type = "Длинный"

        clean_text = re.sub(r'[^\w\s]', '', text_low)
        words = clean_text.split()
        
        for agent in ALL_AGENTS:
            for w in words:
                if len(w) > 3:
                    root = w[:4]
                    for vocab_word in agent.vocabulary:
                        if root in vocab_word:
                            # Генерируем текст с выбранной длиной
                            generated = agent.generate_text(vocab_word, length_type=length_type)
                            return generated
        return None
