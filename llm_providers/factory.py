from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from typing import Dict, Optional

class LLMProviderFactory:
    def __init__(self):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._registered_providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider
        }
    
    def get_provider(self, provider_name: str) -> BaseLLMProvider:
        """Get or create LLM provider instance"""
        if provider_name not in self._providers:
            if provider_name not in self._registered_providers:
                raise ValueError(f"Unknown provider: {provider_name}")
            
            self._providers[provider_name] = self._registered_providers[provider_name]()
        
        return self._providers[provider_name]
    
    def register_provider(self, name: str, provider_class: type):
        """Register a new provider class"""
        self._registered_providers[name] = provider_class
    
    def list_providers(self) -> list:
        """List all available providers"""
        return list(self._registered_providers.keys()) 