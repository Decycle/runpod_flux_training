from pydantic import BaseModel, Field
from .dataset_config import DatasetConfig


class AppConfig(BaseModel):
    username: str
    lora_name: str
    class_tokens: str
    dataset_config: DatasetConfig
    sample_prompt: str = Field(default=None, title="Sample prompt")
