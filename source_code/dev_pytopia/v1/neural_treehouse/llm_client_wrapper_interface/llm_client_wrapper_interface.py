from abc import abstractmethod
from typing import Any, ClassVar, Dict, Optional

from foundation.v1 import CustomLogger

from ..llm_thread import LLMThread

logger = CustomLogger(log_level="INFO")


class LLMClientWrapperInterface:
    MODEL_CONFIGURATIONS: ClassVar[Dict[str, Dict[str, Any]]] = {}

    @classmethod
    @abstractmethod
    def DEFAULT_CONFIG(cls) -> Dict[str, Any]:
        pass

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self) -> None:
        api_key = self._get_api_key_from_env()
        if not api_key:
            raise ValueError("API key must be provided or set in the appropriate environment variable.")

        self.client = self._initialize_client(api_key)

        self.configure()

    def configure(self, configuration_name: Optional[str] = None) -> None:
        if configuration_name:
            self.configuration = self.MODEL_CONFIGURATIONS[configuration_name]
        else:
            self.configuration = self.DEFAULT_CONFIG()

    @abstractmethod
    def _get_api_key_from_env(self) -> Optional[str]:
        pass

    @abstractmethod
    def _initialize_client(self, api_key: str) -> Any:
        pass

    @abstractmethod
    async def get_response(self, llm_thread: LLMThread, **kwargs) -> Any:
        raise NotImplementedError("Subclasses must implement a get_response method!")
