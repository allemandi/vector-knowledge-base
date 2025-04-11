import faiss, numpy as np, sqlite3, orjson
from typing import List, Tuple
from models import Memory

class VectorMemory:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.memories = []
        self.db = sqlite3.connect("chatbot_memory.db")
        self._setup_db()
        self._load_memories()
        
    def _setup_db(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL UNIQUE,
            embedding BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        self.db.commit()
        
    def _load_memories(self):
        memories_data = self.db.execute("SELECT text, embedding FROM memories").fetchall()
        if memories_data:
            embeddings = []
            for text, embedding_blob in memories_data:
                embedding = orjson.loads(embedding_blob)
                self.memories.append(Memory(text=text, embedding=embedding))
                embeddings.append(embedding)
                
            if embeddings:
                self.index.add(np.array(embeddings, dtype=np.float32))

    def add_memory(self, memory):
        if not memory.embedding: raise ValueError("Memory must have an embedding")
        self.db.execute(
            "INSERT INTO memories (text, embedding) VALUES (?, ?)",
            (memory.text, orjson.dumps(memory.embedding))
        )
        self.db.commit()
        self.memories.append(memory)
        self.index.add(np.array([memory.embedding], dtype=np.float32))

    def forget_memory(self, text):
        for idx, memory in enumerate(self.memories):
            if memory.text.lower() == text.lower():
                self.db.execute("DELETE FROM memories WHERE text = ?", (memory.text,))
                self.db.commit()
                self.memories.pop(idx)
                self._rebuild_index()
                return True
        return False

    def _rebuild_index(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        if self.memories:
            embeddings = np.array([m.embedding for m in self.memories], dtype=np.float32)
            self.index.add(embeddings)

    def search(self, query_embedding, k=1):
        if not self.memories: return []
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            min(k, len(self.memories))
        )
        return [(self.memories[idx], float(dist)) 
               for dist, idx in zip(distances[0], indices[0])
               if idx != -1]