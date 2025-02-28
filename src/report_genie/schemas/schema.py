from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class ChatInput(BaseModel):
    prompt: str = Field(
        ..., min_length=5, max_length=1000, description="The text prompt for the chat"
    )
    format: Optional[str] = Field(
        None, description="The format of the response, e.g., text, markdown"
    )
    tone: Optional[str] = Field(
        None, description="The tone of the response, e.g., formal, informal"
    )
    target_audience: Optional[str] = Field(
        None, description="The target audience for the response"
    )


class ChatOutput(BaseModel):
    result: str = Field(..., description="The transformed text response")
