from sentence_transformers import SentenceTransformer
from collections import OrderedDict
import time

class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self._model = None
        self._model_name = model_name
        self.cache = OrderedDict()
        self.cache_size = 128
        self.cache_ttl = 3600

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
            # Disable progress bar
            original = self._model.encode
            self._model.encode = lambda *a, **kw: original(*a, **{**kw, 'show_progress_bar': False})
        return self._model
        
    def generate(self, text):
        if not text: raise ValueError("Text cannot be empty")
        
        # Check cache
        if text in self.cache:
            embedding, timestamp = self.cache[text]
            if time.time() - timestamp < self.cache_ttl:
                self.cache.move_to_end(text)
                return embedding
        
        # Generate embedding
        embedding = self.model.encode([text], convert_to_numpy=True)[0].tolist()
        
        # Update cache
        self.cache[text] = (embedding, time.time())
        if len(self.cache) > self.cache_size:
            self.cache.popitem(False)
            
        return embedding