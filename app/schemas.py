from typing import Annotated
from pydantic import BaseModel, Field


class DataCreate(BaseModel):
    user_id: Annotated[str, Field(min_length=1, max_length=64)]
    payload: Annotated[str, Field(min_length=1, max_length=1024)]


class DataResponse(BaseModel):
    id: int
    user_id: str
    payload: str

    class Config:
        from_attributes = True