from typing import Dict, Type, Optional, List
from sources.providers.base_provider import BaseProvider, ProviderConfig
from sources.providers.ollama_provider import OllamaProvider
from sources.providers.openrouter_provider import OpenRouterProvider
from sources.providers.huggingface_provider import HuggingFaceProvider
from sources.providers.openai_provider import OpenAIProvider
from sources.providers.gemini_provider import GeminiProvider
from sources.providers.groq_provider import GroqProvider
from sources.providers.anthropic_provider import AnthropicProvider
from sources.providers.deepseek_provider import DeepSeekProvider

class ProviderFactory:
    """Factory for creating LLM provider instances."""
    
    _providers: Dict[str, Type[BaseProvider]] = {
        "ollama": OllamaProvider,
        "openrouter": OpenRouterProvider,
        "huggingface": HuggingFaceProvider,
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
        "google": GeminiProvider,  # Alias
        "groq": GroqProvider,
        "anthropic": AnthropicProvider,
        "claude": AnthropicProvider,  # Alias
        "deepseek": DeepSeekProvider,
    }
    
    @classmethod
    def create(
        cls,
        provider_name: str,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ) -> BaseProvider:
        """
        Create provider instance.
        
        Args:
            provider_name: Name of the provider (ollama, openrouter, etc.)
            model: Model identifier
            api_key: Optional API key
            base_url: Optional base URL
            **kwargs: Additional provider-specific configuration
            
        Returns:
            BaseProvider instance
            
        Raises:
            ValueError: If provider_name is unknown
        """
        provider_name = provider_name.lower()
        provider_class = cls._providers.get(provider_name)
        
        if not provider_class:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider: '{provider_name}'. "
                f"Available providers: {available}"
            )
        
        config = ProviderConfig(
            model=model,
            api_key=api_key,
            base_url=base_url,
            extra=kwargs
        )
        
        provider = provider_class(config)
        provider.validate_config()
        
        return provider
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseProvider]):
        """
        Register a custom provider.
        
        Args:
            name: Provider name
            provider_class: Provider class (must inherit from BaseProvider)
        """
        if not issubclass(provider_class, BaseProvider):
            raise TypeError(
                f"Provider class must inherit from BaseProvider, "
                f"got {provider_class.__name__}"
            )
        
        cls._providers[name.lower()] = provider_class
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """Get list of registered providers."""
        return list(cls._providers.keys())
    
    @classmethod
    def get_provider_class(cls, name: str) -> Optional[Type[BaseProvider]]:
        """Get provider class by name."""
        return cls._providers.get(name.lower())
