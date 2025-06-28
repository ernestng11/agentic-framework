from .base import BaseLLMProvider, LLMConfig
from typing import Dict, List, Optional
try:
    import openai
except ImportError:
    openai = None
import json

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.client: Optional[openai.AsyncOpenAI] = None
    
    def _initialize_client(self, api_key: Optional[str]):
        if self.client is None:
            if openai is None:
                raise ImportError("OpenAI package not installed. Please install with: pip install openai")
            if api_key is None:
                raise ValueError("OpenAI API key is required")
            self.client = openai.AsyncOpenAI(api_key=api_key)
    
    async def generate_response(self, messages: List[Dict], config: LLMConfig) -> str:
        """Generate response using OpenAI API"""
        self._initialize_client(config.api_key)
        
        try:
            response = await self.client.chat.completions.create(
                model=config.model_name,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                **(config.additional_params or {})
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def tool_call(self, messages: List[Dict], tools: List[Dict], config: LLMConfig) -> Dict:
        """Perform tool calling with OpenAI API"""
        self._initialize_client(config.api_key)
        
        try:
            response = await self.client.chat.completions.create(
                model=config.model_name,
                messages=messages,
                tools=tools,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                **(config.additional_params or {})
            )
            
            return {
                "message": response.choices[0].message,
                "tool_calls": response.choices[0].message.tool_calls if hasattr(response.choices[0].message, 'tool_calls') else None
            }
        except Exception as e:
            raise Exception(f"OpenAI tool call error: {str(e)}") 