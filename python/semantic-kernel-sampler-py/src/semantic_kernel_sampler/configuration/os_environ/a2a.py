from pydantic import BaseModel, Field


class A2ASettings(BaseModel):
    host: str = Field(default="0.0.0.0")

    port: int = Field(default=9999)

    url: str = Field(default="http://localhost:9999")
