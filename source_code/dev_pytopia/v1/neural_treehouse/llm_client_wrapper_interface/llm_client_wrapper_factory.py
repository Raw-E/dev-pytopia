from typing import Dict, Type

# Local application imports
from .llm_client_wrapper_interface import LLMClientWrapperInterface
from .wrappers.chatgpt_client_wrapper import ChatGPTClientWrapper


class LLMClientWrapperFactory:
    _clients: Dict[str, Type[LLMClientWrapperInterface]] = {"ChatGPT": ChatGPTClientWrapper}

    @classmethod
    def get_client(cls, client_type: str, configuration: str | None = None) -> LLMClientWrapperInterface:
        if client_type not in cls._clients:
            raise ValueError(f"Unsupported LLM client type: {client_type}")

        client_instance = cls._clients[client_type]()

        if configuration is not None:
            client_instance.configure(configuration)

        return client_instance
