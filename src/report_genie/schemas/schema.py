from pydantic import BaseModel
from pydantic.fields import Field

class GetCityInfoInput(BaseModel):
    """Input schema for MyCustomTool."""
    city: str = Field(..., description="City name")
    industry: str = Field(..., description="Industry name")
