# THIS CODE HAS BEEN ORGANIZED

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║ Documentation for llm_code_response.py
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# Third-party imports
from pydantic import BaseModel, Field


# Classes
class LLMCodeResponse(BaseModel):
    code: str = Field(..., description="Code with no markup!")
