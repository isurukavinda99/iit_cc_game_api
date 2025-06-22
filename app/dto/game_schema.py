from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class GameCreate(BaseModel):
    name: str = Field(..., max_length=255, example="Call of Duty")
    category_id: int = Field(..., description="ID of the associated Game Category")
    active: Optional[bool] = True
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class GameResponse(BaseModel):
    id: int
    name: str
    category_id: int
    active: bool
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True