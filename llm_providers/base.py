from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class LLMConfig:
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048
    api_key: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(self, messages: List[Dict], config: LLMConfig) -> str:
        pass
    
    @abstractmethod
    async def tool_call(self, messages: List[Dict], tools: List[Dict], config: LLMConfig) -> Dict:
        pass 