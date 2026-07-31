from pydantic import BaseModel
from typing import Any


class Settings(BaseModel):
    model_config = {"arbitrary_types_allowed": True, "extra": "allow"}

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def __getattr__(self, name: str) -> Any:
        return None
