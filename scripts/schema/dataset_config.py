from pydantic import BaseModel, Field

class ImageData(BaseModel):
    filename: str
    caption: str = Field(default=None, title="Image caption")


class DatasetConfig(BaseModel):
    images: list[ImageData]
    auto_generate_captions: bool = Field(
        default=False, title="Auto generate captions")
    resolution: int = Field(default=512, title="Image resolution")
