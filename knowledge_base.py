from embeddings import EmbeddingGenerator
from memory import VectorMemory
from models import Memory, KnowledgeBaseResponse

class KnowledgeBase:
    def __init__(self):
        self.embedding_gen = EmbeddingGenerator()
        self.memory = VectorMemory()
        self.last_response = None
        self.threshold = 0.3

    def set_similarity_threshold(self, threshold):
        if 0 <= threshold <= 1:
            self.threshold = threshold
        else:
            raise ValueError("Threshold must be between 0 and 1")

    def remember(self, text):
        if text := text.strip():
            embedding = self.embedding_gen.generate(text)
            self.memory.add_memory(Memory(text=text, embedding=embedding))
        else:
            raise ValueError("Cannot remember empty text")

    def forget(self, text=None):
        if text:
            return self.memory.forget_memory(text)
            
        return (self.last_response and 
                self.last_response.confidence >= self.threshold and 
                self.memory.forget_memory(self.last_response.message))

    def respond(self, query):
        if not query.strip():
            self.last_response = KnowledgeBaseResponse("No relevant information found.")
            return self.last_response
            
        try:
            results = self.memory.search(self.embedding_gen.generate(query), k=1)
            
            if not results:
                self.last_response = KnowledgeBaseResponse("No information in knowledge base yet.")
                return self.last_response
                
            memory, similarity = results[0]
            
            if similarity < self.threshold:
                message = (
                    f"No relevant information found.\n"
                    f"Nearest match similarity: {similarity:.3f}\n"
                    f"Current threshold: {self.threshold:.3f}"
                )
                self.last_response = KnowledgeBaseResponse(message, similarity)
            else:
                self.last_response = KnowledgeBaseResponse(memory.text, similarity)
                
            return self.last_response
            
        except:
            return KnowledgeBaseResponse("Error retrieving information.") 