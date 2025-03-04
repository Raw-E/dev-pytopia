# THIS CODE HAS BEEN ORGANIZED

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ Documentation for chat_gpt_client_wrapper.py
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Standard library imports
import asyncio
import os
from typing import Any, Dict, Optional

# Third-party imports
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Local development package imports
from foundation.v1 import CustomLogger

# Current project imports
from ..llm_client_wrapper_interface import LLMClientWrapperInterface
from ...llm_thread import LLMThread

# Configuration
logger = CustomLogger(log_level="INFO")
load_dotenv()


# Classes
class ChatGPTClientWrapper(LLMClientWrapperInterface):
    MODEL_CONFIGURATIONS = {
        "o3-mini-on-dmt": {
            "model": "o3-mini",
            "reasoning_effort": "high",
            "temperature": 1.0,
        },
        "o3-mini-on-alcohol": {
            "model": "o3-mini",
            "reasoning_effort": "low",
            "temperature": 1.0,
        },
        "o1": {
            "model": "o1",
            "temperature": 1.0,
        },
        "o1-preview": {
            "model": "o1-preview",
            "temperature": 1.0,
        },
        "o1-mini": {
            "model": "o1-mini",
            "temperature": 1.0,
        },
        "gpt-4o": {
            "model": "gpt-4o-2024-11-20",
            "temperature": 0.75,
            "max_completion_tokens": 16384,
        },
        "gpt-4.5-preview": {
            "model": "gpt-4.5-preview",
            "temperature": 0.75,
            "max_completion_tokens": 16384,
        },
    }

    @classmethod
    def DEFAULT_CONFIG(cls) -> Dict[str, Any]:
        return cls.MODEL_CONFIGURATIONS["gpt-4o"]

    def _initialize_client(self, api_key: str) -> Any:
        return AsyncOpenAI(api_key=api_key)

    def _get_api_key_from_env(self) -> Optional[str]:
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key

    def _prepare_api_arguments(self, llm_thread: LLMThread, **kwargs) -> Dict[str, Any]:
        api_arguments = self.configuration.copy()
        api_arguments["messages"] = llm_thread.messages
        api_arguments.update(kwargs)
        return api_arguments

    async def get_response(self, llm_thread: LLMThread, **kwargs) -> Any:
        api_arguments = self._prepare_api_arguments(llm_thread, **kwargs)
        max_retries = 3
        retry_delay = 10

        for attempt in range(max_retries):
            try:
                logging_task = None

                async def log_waiting_status():
                    wait_count = 0
                    while True:
                        await asyncio.sleep(30)
                        wait_count += 1
                        logger.info(f"Still waiting for OpenAI API response... ({wait_count * 30}s elapsed)")

                try:
                    logging_task = asyncio.create_task(log_waiting_status())

                    if "response_format" in api_arguments and isinstance(api_arguments["response_format"], type):
                        response = await self.client.beta.chat.completions.parse(**api_arguments)
                        parsed_response = response.choices[0].message.parsed
                        return parsed_response
                    else:
                        return await self.client.chat.completions.create(**api_arguments)
                finally:
                    if logging_task and not logging_task.done():
                        logging_task.cancel()
                        try:
                            await logging_task
                        except asyncio.CancelledError:
                            pass

            except Exception as error:
                error_message = str(error)
                if "rate_limit_exceeded" in error_message and attempt < max_retries - 1:
                    logger.error(
                        f"Rate limit reached. Waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}"
                    )
                    await asyncio.sleep(retry_delay)
                    continue

                logger.error(f"Error in OpenAI API call: {error_message}")
                raise
