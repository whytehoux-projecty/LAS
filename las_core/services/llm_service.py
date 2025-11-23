from config.settings import settings
from sources.llm_provider import Provider
from sources.logger import Logger

logger = Logger("llm_service.log")

class LLMService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.provider = Provider(
            provider_name=settings.provider_name,
            model=settings.provider_model,
            server_address=settings.provider_server_address,
            is_local=settings.is_local
        )
        logger.info(f"LLM Service initialized with provider: {self.provider.provider_name}")

    def get_provider(self):
        return self.provider

def get_llm_service():
    return LLMService()
