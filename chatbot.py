from embeddings import EmbeddingGenerator
from memory import VectorMemory
from models import Memory, ChatbotResponse

class Chatbot:
    def __init__(self):
        self.embedding_gen = EmbeddingGenerator()
        self.memory = VectorMemory()
        self.last_response = None
        self.threshold = 0.5

    def set_similarity_threshold(self, threshold):
        if 0 <= threshold <= 1: self.threshold = threshold
        else: raise ValueError("Threshold must be between 0 and 1")

    def remember(self, text):
        if text := text.strip():
            embedding = self.embedding_gen.generate(text)
            self.memory.add_memory(Memory(text=text, embedding=embedding))
        else: raise ValueError("Cannot remember empty text")

    def forget(self, text=None):
        if text: return self.memory.forget_memory(text)
        return (self.last_response and self.last_response.confidence >= self.threshold 
                and self.memory.forget_memory(self.last_response.message))

    def respond(self, query):
        if not query.strip():
            self.last_response = ChatbotResponse("I don't have any relevant information.")
            return self.last_response
            
        try:
            results = self.memory.search(self.embedding_gen.generate(query), k=1)
            
            if not results or results[0][1] < self.threshold:
                conf = 0.0 if not results else results[0][1]
                self.last_response = ChatbotResponse("I don't have any relevant information.", conf)
            else:
                memory, similarity = results[0]
                self.last_response = ChatbotResponse(memory.text, similarity)
                
            return self.last_response
        except:
            return ChatbotResponse("Sorry, I encountered an error.")