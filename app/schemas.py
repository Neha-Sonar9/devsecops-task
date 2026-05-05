from pydantic import BaseModel

class DataCreate(BaseModel):
    user_id: str
    payload: str

class DataResponse(BaseModel):
    id: int
    user_id: str
    payload: str

    class Config:
        from_attributes = True