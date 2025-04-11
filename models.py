from typing import List, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class Memory:
    text: str
    embedding: Optional[List[float]] = None

@dataclass(frozen=True)
class KnowledgeBaseResponse:
    message: str
    confidence: float = 0.0