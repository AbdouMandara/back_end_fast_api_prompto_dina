from typing import List, Optional

from pydantic import BaseModel


class PromptRequest(BaseModel):
    idea: str
    objective: str
    role: str
    level: str
    responseFormat: str
    tone: str
    length: str
    constraints: str


class TestPromptRequest(BaseModel):
    prompt: str


class RefinePromptRequest(BaseModel):
    prompt: str
    action: str


class PromptResponse(BaseModel):
    prompt: str
    suggestions: Optional[List[str]] = None


class AIResponse(BaseModel):
    response: str
